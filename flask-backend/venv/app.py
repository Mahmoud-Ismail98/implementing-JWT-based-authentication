from flask import Flask, request, jsonify
from flask_jwt_extended import verify_jwt_in_request,JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from flask_cors import CORS
from functools import wraps

app = Flask(__name__)

CORS(app)
app.config['JWT_SECRET_KEY'] = 'e90de758e6dcda0d18db033ec3b38fa2f0774fe73307ec9ab22dd9edf8a0c0c4'  # Replace with a secure key
app.config['MONGO_URI'] = "mongodb://localhost:27017/AUTH"  # Replace with your MongoDB URI
jwt = JWTManager(app)
mongo = PyMongo(app)

def role_required(required_role):
    def wrapper(fn):
        @wraps(fn)
        def decorated(*args, **kwargs):
            verify_jwt_in_request()
            user = get_jwt_identity()
            if user['role'] != required_role:
                return jsonify(msg="Access denied! Role not sufficient"), 403
            return fn(*args, **kwargs)
        return decorated
    return wrapper

#Authorize Based on Roles:
@app.route('/admin-only', methods=['GET'])
@jwt_required()
@role_required('admin')
def admin_only():
    return jsonify(msg="Welcome, Admin!")

#Attribute-Based Access Control (ABAC)
def department_required(department):
    def wrapper(fn):
        @wraps(fn)
        def decorated(*args, **kwargs):
            verify_jwt_in_request()
            user = get_jwt_identity()
            if user['department'] != department:
                return jsonify(msg="Access denied! Department not authorized"), 403
            return fn(*args, **kwargs)
        return decorated
    return wrapper

@app.route('/research-only', methods=['GET'])
@jwt_required()
@department_required('R&D')
def research_only():
    return jsonify(msg="Welcome to R&D!")


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    role = data.get('role', 'user')  # Assign a default role if not provided
    department = data.get('department', 'general')  # Assign a default role if not provided

    if mongo.db.users.find_one({'username': username}):
        return jsonify({"msg": "User already exists"}), 409

    hashed_password = generate_password_hash(password)
    mongo.db.users.insert_one(
        {'username': username, 
         'password': hashed_password,
         'role':role,
         'department':department,
         })
    return jsonify({"msg": "User created successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = mongo.db.users.find_one({'username': username})
    if user and check_password_hash(user['password'], password):
        # Include role and department in the JWT token
        access_token = create_access_token(
            identity={'username': username, 'role': user['role'], 'department': user['department']},
            expires_delta=datetime.timedelta(hours=1)
        )
        return jsonify(access_token=access_token)
    return jsonify({"msg": "Invalid credentials"}), 401

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

if __name__ == '__main__':
    app.run(debug=True)
