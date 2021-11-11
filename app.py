from flask import Flask
from flask.templating import render_template

app = Flask(__name__)

donations = [
  { 'title': 'St. Jude', 'description': 'fund for underserved members of the community', 'amount': '1000' },
  { 'title': 'Red Cross', 'description': 'fund to aid those affected by disasters', 'amount': '1000' }
]

# home/donations route ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
@app.route('/')
def donations_index():
  ''' Show all donations '''
  return render_template('donations_index.html', donations=donations)




if __name__ == '__main__':
  app.run(debug=True)