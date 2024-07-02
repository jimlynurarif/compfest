from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client['sea_salon']
reviews_collection = db['reviews']
reservations_collection = db['reservations']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reserve', methods=['POST'])
def reserve():
    name = request.form['name']
    phone = request.form['phone']
    service = request.form['service']
    datetime = request.form['datetime']
    
    reservation = {
        'name': name,
        'phone': phone,
        'service': service,
        'datetime': datetime
    }
    
    reservations_collection.insert_one(reservation)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
