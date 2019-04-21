from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    queried_values = mongo.db.mars_data.find_one()
    return render_template("index.html", listings = queried_values)

@app.route("/scrape")
def scraper():
    # create the database collection and collection object 
    mars_data_collection = mongo.db.mars_data
    
    # store the latest URL data into the d
    data_list = scrape_mars.scrape()
    
    # update the database
    mars_data_collection.update({}, data_list, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)