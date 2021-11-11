import re
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

client = MongoClient()
db = client.Contractor
donations = db.donations

app = Flask(__name__)

# donations = [
#   { 'title': 'St. Jude', 'description': 'fund for underserved members of the community', 'amount': '1000' },
#   { 'title': 'Red Cross', 'description': 'fund to aid those affected by disasters', 'amount': '1000' }
# ]

# home/donations route ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
@app.route('/')
def donations_index():
  ''' Show all donations '''
  return render_template('donations_index.html', donations=donations.find())

# new donation form route ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
@app.route('/donations/new')
def donations_new():
  ''' Create a new donation '''
  return render_template('donations_new.html')

# donations post request route ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
# submit route for donations post request form dict info to be added as a donation object in the database
@app.route('/donations', methods=['POST'])
def donations_submit():
  ''' Submit a new donation '''
  donation = {
    'title': request.form.get('title'),
    'description': request.form.get('description'),
    'amount': '$' + request.form.get('amount'),
    'rating': request.form.get('rating')
  }
  donations.insert_one(donation)
  print(f"donation is '{donation}'")
  return redirect(url_for('donations_index'))



if __name__ == '__main__':
  app.run(debug=True)