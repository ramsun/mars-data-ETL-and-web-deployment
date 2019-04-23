# Import dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Initialize flask app
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Will render a page from the index.html template
@app.route("/")
def index():
    # query for data from the mongo collection
    queried_data = mongo.db.mars_data.find_one()
    return render_template("index.html", data = queried_data)

# Will scrape the latest mars data from Nasa's website and load it into
# the MongoDB collection.
@app.route("/scrape")
def scraper():
    # Create the database collection and collection object 
    mars_data_collection = mongo.db.mars_data
    
    # Empty the contents of the database to prevent duplicate data
    mongo.db.drop_collection(mars_data_collection)

    # Store the latest URL data into the dict
    data_dict = scrape_mars.scrape()
    
    # Update the database
    mars_data_collection.insert(data_dict)
    return redirect("/", code=302)

# Main
if __name__ == "__main__":
    app.run(debug=True)