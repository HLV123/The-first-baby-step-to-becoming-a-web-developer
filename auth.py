import jwt
from functools import wraps
from flask import request, jsonify, current_app
from models import User, db

def jwt_required():
    """
    Decorator to protect routes that require a valid JWT token.
    The token is expected in the 'Authorization' header as 'Bearer <token>'.
    """
    def wrapper(fn):
        @wraps(fn)
        def decorated_function(*args, **kwargs):
            token = None
            if 'Authorization' in request.headers:
                token = request.headers['Authorization'].split(' ')[1]

            if not token:
                return jsonify({'error': 'Token is missing!'}), 401

            try:
                # Decode the token using the secret key
                data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
                current_user = User.query.filter_by(id=data['user_id']).first()
                if current_user is None:
                    return jsonify({'error': 'Invalid token!'}), 401
            except jwt.ExpiredSignatureError:
                return jsonify({'error': 'Token has expired!'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'error': 'Invalid token!'}), 401
            except Exception as e:
                return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500

            # Pass the current user object to the decorated function
            return fn(current_user, *args, **kwargs)
        return decorated_function
    return wrapper

