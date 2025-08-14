from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_cors import CORS
from models import db, User
import jwt
from datetime import datetime, timedelta
from flask_bcrypt import Bcrypt
from auth import jwt_required
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from email_validator import validate_email, EmailNotValidError

# Initialize the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-very-strong-secret-key'  # Change this in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
CORS(app)
bcrypt = Bcrypt(app)
limiter = Limiter(key_func=get_remote_address, app=app)

# Create the database tables on startup
with app.app_context():
    db.create_all()

# Thay thế các routes trong app.py của bạn bằng những routes này:

@app.route('/')
def home():
    """Renders the homepage."""
    return render_template('index.html')

@app.route('/login')  # Đổi từ '/login-page' thành '/login'
def login_page():
    """Renders the login page."""
    return render_template('login.html')

@app.route('/register')  # Đổi từ '/register-page' thành '/register'
def register_page():
    """Renders the registration page."""
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    """Renders the user dashboard page."""
    return render_template('dashboard.html')

@app.route('/api/register', methods=['POST'])
@limiter.limit("5 per minute")
def register():
    """API endpoint for user registration."""
    data = request.get_json()
    if not data or not all(k in data for k in ('email', 'password', 'confirm_password', 'full_name')):
        return jsonify({'error': 'Missing data'}), 400

    email = data['email']
    password = data['password']
    confirm_password = data['confirm_password']
    full_name = data['full_name']

    # Server-side validation
    try:
        validate_email(email)
    except EmailNotValidError:
        return jsonify({'error': 'Invalid email format'}), 400

    if len(password) < 8:
        return jsonify({'error': 'Password must be at least 8 characters long'}), 400

    if password != confirm_password:
        return jsonify({'error': 'Passwords do not match'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 409

    # Hash the password and save the new user
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(email=email, password_hash=hashed_password, full_name=full_name)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201

@app.route('/api/login', methods=['POST'])
@limiter.limit("10 per hour")
def login():
    """API endpoint for user login."""
    data = request.get_json()
    if not data or not all(k in data for k in ('email', 'password')):
        return jsonify({'error': 'Missing data'}), 400

    user = User.query.filter_by(email=data['email']).first()
    if not user or not bcrypt.check_password_hash(user.password_hash, data['password']):
        return jsonify({'error': 'Invalid email or password'}), 401

    # Generate the JWT token
    remember_me = data.get('remember_me', False)
    expires_delta = timedelta(hours=24) if remember_me else timedelta(hours=1)
    payload = {
        'user_id': user.id,
        'exp': datetime.utcnow() + expires_delta
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

    # Update last login time
    user.last_login = datetime.utcnow()
    db.session.commit()

    return jsonify({'message': 'Login successful', 'token': token})

@app.route('/api/dashboard', methods=['GET'])
@jwt_required()
def get_dashboard_info(current_user):
    """Protected API endpoint to get user info for the dashboard."""
    return jsonify({
        'message': f'Welcome to your dashboard, {current_user.full_name}!',
        'email': current_user.email,
        'full_name': current_user.full_name,
        'last_login': current_user.last_login.strftime('%Y-%m-%d %H:%M:%S') if current_user.last_login else 'N/A'
    })

@app.route('/api/change_password', methods=['POST'])
@jwt_required()
def change_password(current_user):
    """Protected API endpoint for changing password."""
    data = request.get_json()
    if not data or not all(k in data for k in ('old_password', 'new_password', 'confirm_new_password')):
        return jsonify({'error': 'Missing data'}), 400

    old_password = data['old_password']
    new_password = data['new_password']
    confirm_new_password = data['confirm_new_password']

    # Verify old password
    if not bcrypt.check_password_hash(current_user.password_hash, old_password):
        return jsonify({'error': 'Mật khẩu cũ không chính xác'}), 401

    # Validate new password
    if len(new_password) < 8:
        return jsonify({'error': 'Mật khẩu mới phải có ít nhất 8 ký tự'}), 400

    if new_password != confirm_new_password:
        return jsonify({'error': 'Mật khẩu mới và xác nhận mật khẩu không khớp'}), 400

    # Hash the new password and update
    current_user.password_hash = bcrypt.generate_password_hash(new_password).decode('utf-8')
    db.session.commit()

    return jsonify({'message': 'Đổi mật khẩu thành công'}), 200

# Bonus: Simulate password reset via a simple request
@app.route('/api/forgot_password', methods=['POST'])
def forgot_password():
    """Simulates a password reset request."""
    email = request.get_json().get('email')
    user = User.query.filter_by(email=email).first()

    if user:
        # In a real app, you would generate a secure token and email it to the user.
        # For this demo, we just simulate the success message.
        return jsonify({'message': 'If an account with that email exists, a password reset link has been sent.'}), 200
    else:
        return jsonify({'message': 'If an account with that email exists, a password reset link has been sent.'}), 200

# Main entry point
if __name__ == '__main__':
    app.run(debug=True)

