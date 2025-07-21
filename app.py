from flask import Flask, render_template, request, redirect
import json
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb+srv://gowthamjuttiga:gowtham@123@cluster0.nkoo2nz.mongodb.net/")
db = client["readtrack_db"]
collection = db["content"]

# Ensure static/book_covers directory exists
covers_dir = os.path.join(os.path.dirname(__file__), 'static', 'book_covers')
os.makedirs(covers_dir, exist_ok=True)

@app.route("/")
def home():
    data_path = os.path.join(os.path.dirname(__file__), "data.json")
    with open(data_path, "r", encoding="utf-8") as f:
        books = json.load(f)
    return render_template("index.html", books=books)

@app.route("/add", methods=["GET", "POST"])
def add_content():
    if request.method == "POST":
        title = request.form["title"]
        collection.insert_one({"title": title, "progress": 0})
        return redirect("/")
    return render_template("add_content.html")

@app.route("/log", methods=["GET", "POST"])
def log_progress():
    contents = list(collection.find())
    if request.method == "POST":
        content_id = request.form["content_id"]
        progress = int(request.form["progress"])
        collection.update_one({"_id": ObjectId(content_id)}, {"$set": {"progress": progress}})
        return redirect("/")
    return render_template("log_progress.html", contents=contents)

@app.route("/dashboard")
def dashboard():
    contents = list(collection.find())
    return render_template("dashboard.html", contents=contents)

if __name__ == "__main__":
    app.run(debug=True)
