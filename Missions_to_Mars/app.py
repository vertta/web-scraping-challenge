from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# use flask pymongo to set up the connection to the database
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_data_db"

mongo  = PyMongo(app)   # set varible monogo to call PyMongo application
@app.route("/")     # start at the root of the application

def index():
    # access information for the database
    mars_data= mongo.db.marsData.find_one()
    #print(mars_data)

    return render_template("index.html", mars=mars_data)

@app.route("/scrape")   # call scrape function
def scrape_all():
   # reference to the database collection (table)
    marsTable = mongo.db.marsData

   # drop the table if it exists 
    mongo.db.marsData.drop()
    
    # call scape script
    mars_data = scrape_mars.scrape_all()
    #print(mars_data)  # print dicitionary that is returned from all  uncomment for troubleshooting
    
    # take the dictionary and load into MongoDb
    marsTable.insert_one(mars_data)
    return redirect("/")

if __name__ == "__main__":
    app.run()