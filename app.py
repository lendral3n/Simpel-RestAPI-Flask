# Importing necessary libraries
from flask import Flask, jsonify, request, json
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from flask_marshmallow import Marshmallow

# Creating an instance of the Flask class
app = Flask(__name__)

# Initializing SQLAlchemy, Marshmallow, and MySQL
db = SQLAlchemy()
ma = Marshmallow()
mysql = MySQL(app)

# Defining the User model with its fields
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(15), nullable=False)

    # Constructor to initialize the User object
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

# Defining the User schema for serialization
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'password')

# Creating instances of the UserSchema
user_schema = UserSchema()
users_schema = UserSchema(many=True)

# Configuring the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/user'

# Initializing the app with the database settings
db.init_app(app)

# Creating the database tables within the application context
with app.app_context():
    db.create_all()
    
# CRUD operations for the User model

# Create a new user
@app.route('/users', methods=['POST'])
def add_user():
    _json = request.json
    name = _json['name']
    email = _json['email']
    password = _json['password']
    new_user = User(name=name, email=email
                    , password=password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message":"Success Create User"})

# Get All User
@app.route('/users', methods=['GET'])
def get_user():
    all_user = User.query.all()
    result = users_schema.dump(all_user)
    return jsonify({"message":"Success Get User"}, result)

# Get User By Id
@app.route('/users/<id>', methods=['GET'])
def get_user_by_id(id):
    user = User.query.get(id)
    if user is None:
        return jsonify ({"error": "the user doesn't exist"})
    else: 
        idresult = users_schema.dump(user, many=False)
        return jsonify({"message":"Success Get User By Id"}, idresult) 
        
# Update User By Id
@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)
    if user is None:
        return jsonify ({"error": "the user doesn't exist"})
    _json = request.json
    user.name = _json['name']
    user.email = _json['email']
    user.password = _json['password']
    db.session.commit()
    return jsonify({"message":"Success Update User"})

# Delete User By Id
@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if user is None:
        return jsonify ({"error": "the user doesn't exist"})
    else:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "Success Delete User"})


if __name__ == "__main__":
    app.run(debug=True, port=8080)