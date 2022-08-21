from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__, template_folder='templates')

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route("/")

def home():

    # Find one record of data from the mongo database
    mars_info = mongo.db.collection.find_one()

    # Return template and data
    return render_template("index.html", collection= mars_info)

    # Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    collection = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    # mongo.db.collection.update_one({}, {"$set": collection}, upsert=True)
    mongo.db.collection.update({}, collection, upsert=True)


    # Redirect back to home page
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)