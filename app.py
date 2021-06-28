# We will make an app via Python and Flask.
# Hence, we will need to run code on the terminal, not in Jupyter Notebook.

# We'll start with importing the appropriate dependencies.
# We'll debut some new dependencies: render_template, redirect, url_for, PyMongo, and scraping.
from flask import Flask, render_template, redirect, url_for 
from flask_pymongo import PyMongo
import scraping

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection 
# Presumably, we have to flip the switch for our mongo program.
# app.config will be the link between our Flask app and Mongo.
# Btw, "URI" stands for "universal resource identifier". I suppose it's like a path that applies to just about every personal computer.
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Time to define the pages of our main "domain" website. 
# First we start with the home page that has no extra parameters.
@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)

# Second we define our /scrape webpage.
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update({}, mars_data, upsert=True)
   return redirect('/', code=302)

# With the below if conditional, we specify Flask the condition by which we run our app.
if __name__ == "__main__":
   app.run()
