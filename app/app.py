import os

import pymongo
from flask import Flask, jsonify, abort, request

client = pymongo.MongoClient(os.getenv("MONGODB_URI", "mongodb://127.0.0.1:27017/database"))
db = client.get_database()

app = Flask(__name__)

def remove_id(pymongo_dict):
    return {key: str(pymongo_dict[key]) for key in pymongo_dict.keys()}

@app.errorhandler(404)
def resource_not_found(exception):
    """Returns exceptions as part of a json."""
    return jsonify(error=str(exception)), 404

@app.route("/")
def main():
    return "App is up!"

@app.route("/new_post", methods=["POST"])
def new_post():
    new_post = request.json
    post_id = db.posts.insert_one(new_post).inserted_id
    return jsonify({
        "id": str(post_id)
    })

@app.route("/get_posts")
def get_posts():
    posts_list = db.posts.find()
    try:
        if posts_list:
            return jsonify([remove_id(post) for post in posts_list])
        else:
            raise Exception("There are no posts in the database!")
    except Exception as exception:
        abort(404, exception)