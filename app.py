from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
import os

app = Flask(__name__)

# MongoDB connection from Render environment variable
MONGO_URI = os.environ.get("MONGO_URI")
client = MongoClient(MONGO_URI)

db = client.expenseDB
collection = db.expenses


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        title = request.form["title"]
        amount = float(request.form["amount"])

        collection.insert_one({
            "title": title,
            "amount": amount
        })

        return redirect("/")

    expenses = list(collection.find())
    total = sum(e["amount"] for e in expenses)

    return render_template(
        "index.html",
        expenses=expenses,
        total=total
    )


if __name__ == "__main__":
    app.run()
