from datetime import date
import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from typing import List

from models.article import Article

app = Flask(__name__)
CORS(app)
DATA_FILE = "articles.json"

def load_data() -> List[dict]:
    with open(DATA_FILE, "r") as f:
        return json.load(f)
    
def save_data(data: List[dict]):
    for article in data:
        if isinstance(article["release_date"], date):
            article["release_date"] = article["release_date"].isoformat()
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

@app.route("/api/articles", methods=["POST"])
def create_articles():
    try:
        print("Received data:", request.json)
        data = request.json

        if not all(k in data for k in ("title", "content", "release_date")):
            return jsonify({"error": "Missing required fields"}), 400

        articles = load_data()

        new_id = max([a["id"] for a in articles], default=0) + 1
        print(f"ID: {new_id}")

        new_article = Article(id=new_id, **data) 

        articles.append(new_article.model_dump())
        save_data(articles)

        return jsonify({"message": "Article created successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/articles", methods=["GET"])
def read_articles():
    year = request.args.get("year")
    articles = load_data()

    if year:
        articles = [a for a in articles if a["release_date"].startswith(year)]

    return jsonify(articles), 200

@app.route("/api/articles/<int:article_id>", methods=["PUT"])
def update_articles(article_id: int):
    data = request.json
    articles = load_data()

    for article in articles:
        if article["id"] == article_id:
            article.update(data)
            save_data(articles)
            return jsonify({"message": "Article updated successfully!"}), 200
        
    return jsonify({"error": "Article not found!"}), 404

@app.route("/api/articles/<int:article_id>", methods=["DELETE"])
def delete_articles(article_id: int):
    articles = load_data()
    articles = [a for a in articles if a["id"] != article_id]
    save_data(articles)
    return jsonify({"message": "Article deleted successfully"}), 200

if __name__ == "__main__":
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump([], f) 

    app.run(debug=True)