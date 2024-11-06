from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from flask_cors import CORS

app = Flask(__name__)

CORS(app)
app.config['JWT_SECRET_KEY'] = 'e90de758e6dcda0d18db033ec3b38fa2f0774fe73307ec9ab22dd9edf8a0c0c4'  # Replace with a secure key
app.config['MONGO_URI'] = "mongodb://localhost:27017/AUTH"  # Replace with your MongoDB URI
jwt = JWTManager(app)
mongo = PyMongo(app)

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if mongo.db.users.find_one({'username': username}):
        return jsonify({"msg": "User already exists"}), 409

    hashed_password = generate_password_hash(password)
    mongo.db.users.insert_one({'username': username, 'password': hashed_password})
    return jsonify({"msg": "User created successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = mongo.db.users.find_one({'username': username})
    if user and check_password_hash(user['password'], password):
        access_token = create_access_token(identity={'username': username}, expires_delta=datetime.timedelta(hours=1))
        return jsonify(access_token=access_token)
    return jsonify({"msg": "Invalid credentials"}), 401

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

if __name__ == '__main__':
    app.run(debug=True)
