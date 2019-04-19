# import necessary libraries
from flask import Flask, render_template, redirect
# import pymongo as mongo
from flask_pymongo import PyMongo
import scrape_mars



# create instance of Flask app

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")

# drop collection if it exists
mongo.db.mars_facts.drop()

# Conn = "mongodb://localhost:27017"
# client = mongo.MongoClient(Conn)
# db = client.mars_db

# Create route that renders index.html template and finds documents from mongo
@app.route("/")
def echo(): 

  # Find data

    # news_content = mongo.db.news_content.find()
    mars_db_data = mongo.db.mars_facts.find_one()

    # return template and data

    return render_template("index.html", mars_info = mars_db_data)

# Route that will trigger scrape function
@app.route("/scrape")
def scrape(): 
   # Run scraping function
    # news = scrape_mars.scrape()

    # Store results into a dictionary

# Run scrapped functions
    #mars_info = mongo.mars_facts.mars_info
    mars_data = scrape_mars.scrape_mars_news()
    mars_data = scrape_mars.scrape_mars_image()
    mars_data = scrape_mars.scrape_mars_facts()
    mars_data = scrape_mars.scrape_mars_weather()
    mars_data = scrape_mars.scrape_mars_hemispheres()
    #mars_info.update({}, mars_data, upsert=True)
    mongo.db.mars_facts.insert_one(mars_data)

    return redirect("/", code=302)

if __name__ == "__main__": 
    app.run(debug= True)

