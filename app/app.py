"""This is the Flask App."""

# pylint: disable=broad-except

import os

import pymongo
from flask import Flask, jsonify, abort, request

client = pymongo.MongoClient(
    os.getenv("MONGODB_URI", "mongodb://127.0.0.1:27017/database")
)
db = client.get_database()

app = Flask(__name__)


def stringify_id(pymongo_dict):
    """Converts the bson.objectid.ObjectId to a string,
    to allow for JSON serialization.
    """
    return {key: str(pymongo_dict[key]) for key in pymongo_dict.keys()}


@app.errorhandler(404)
def resource_not_found(exception):
    """Returns exceptions as part of a JSON."""
    return jsonify(error=str(exception)), 404


@app.route("/")
def main():
    """Show the status of the app."""
    return "App is up!"


@app.route("/new_post", methods=["POST"])
def create_new_post():
    """Takes a blog post via a POST request and inserts it into the database."""
    new_post = request.json
    post_id = db.posts.insert_one(new_post).inserted_id
    return jsonify({"id": str(post_id)})


@app.route("/get_posts")
def get_posts():
    """Gets all blog posts form the database."""
    posts_list = db.posts.find()
    try:
        if not posts_list:
            raise Exception("There are no posts in the database!")
        return jsonify([stringify_id(post) for post in posts_list])

    except Exception as exception:
        abort(404, exception)
