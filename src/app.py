from bson import json_util
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask import Flask, jsonify, request, jsonify, Response
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["MONGO_URI"]="mongodb://localhost/pythonapi"
mongo = PyMongo(app)

@app.route("/users", methods=["POST"])
def create_user():
  #Reciving data
  username = request.json["username"]
  password = request.json["password"]
  email = request.json["email"]

  if username and password and email:
    hashed_password = generate_password_hash(password)
    id = mongo.db.users.insert_one(
      {"username": username, "password": hashed_password, "email": email}
    )
    response = {
      "id": str(id),
      "username": username,
      "password": hashed_password,
      "email": email
    }
    return response
  else:
    return not_found()

  return{"message": "OK!!"}

@app.route("/users", methods=["GET"])
def get_users():
  users = mongo.db.users.find()
  response = json_util.dumps(users)
  return Response(response, mimetype="application/json")

@app.route("/users/<id>", methods=["GET"])
def get_user(id):
  user = mongo.db.users.find_one({"_id": ObjectId(id)})
  response = json_util.dumps(user)
  return Response(response, mimetype="application/json")

@app.route("/users/<id>", methods=["DELETE"])
def delete_user(id):
  mongo.db.users.delete_one({"_id": ObjectId(id)})
  response = jsonify({"message": "User Delete"})
  return response

@app.route("/users/<id>", methods=["PUT"])
def update_user(id):
  username = request.json["username"]
  password = request.json["password"]
  email = request.json["email"]

  if username and password and email:
    hashed_passsword = generate_password_hash(password)
    mongo.db.users.update_one({"_id": ObjectId(id)}, {"$set": {
      "username": username,
      "password": hashed_passsword,
      "email": email
    }})
    response = jsonify({"message": "User " + username + " update"})
    return response

@app.errorhandler(404)
def not_found(error=None):
  response = jsonify({
    "message": "Resource Not Found: " + request.url,
    "status": 404
  })
  response.status_code = 404
  return response

if __name__ == "__main__":
  app.run(debug=True)