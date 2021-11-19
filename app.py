from flask import Flask, render_template, request, redirect, url_for
from bson.objectid import ObjectId
from pymongo import MongoClient

client = MongoClient()
db = client.Contractor
donations = db.donations

app = Flask(__name__)

# home/donations route ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
@app.route('/')
def donations_index():
  ''' Show all donations '''
  return render_template('donations_index.html', donations=donations.find())

# new donation form route ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
@app.route('/donations/new')
def donations_new():
  ''' Create a new donation '''
  return render_template('donations_new.html', title='New Donation')

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
  donation_id = donations.insert_one(donation).inserted_id
  return redirect(url_for('donations_show', donation_id=donation_id))

# single donation route ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
@app.route('/donations/<donation_id>')
def donations_show(donation_id):
  ''' Show a single donation '''
  donation = donations.find_one({'_id': ObjectId(donation_id)})
  return render_template('donations_show.html', donation=donation)

# Edit route for single donations ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
@app.route('/donations/<donation_id>/edit')
def donations_edit(donation_id):
  ''' Edit a single donation '''
  donation = donations.find_one({'_id': ObjectId(donation_id)})
  return render_template('donations_edit.html', donation=donation, title='Edit Donation')

# Update route for single donations ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
@app.route('/donations/<donation_id>', methods=['POST'])
def donations_update(donation_id):
  ''' Submit an edited donation '''
  updated_donation = {
    'title': request.form.get('title'),
    'description': request.form.get('description'),
    'amount': '$' + request.form.get('amount'),
    'rating': request.form.get('rating')
  }
  donations.update_one(
    {'_id': ObjectId(donation_id)},
    {'$set': updated_donation}
  )
  return redirect(url_for('donations_show', donation_id=donation_id))

# Delete route for single donations ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
@app.route('/donations/<donation_id>/delete', methods=['POST'])
def donations_delete(donation_id):
  ''' Delete one donation '''
  donations.delete_one({'_id': ObjectId(donation_id)})
  return redirect(url_for('donations_index'))

if __name__ == '__main__':
  app.run(debug=True)