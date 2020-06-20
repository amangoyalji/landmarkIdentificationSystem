from flask import Flask, request, flash, url_for, redirect, render_template,session
from flask_sqlalchemy import SQLAlchemy
from flask import Response
import cv2
import json
from keras.preprocessing.image import img_to_array

import numpy as np
import tensorflow as tf
from io import StringIO,BytesIO
from matplotlib import pyplot as plt
from PIL import Image

import cv2
import os
import Image_Prediction


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///User.sqlite3'
app.config['SECRET_KEY'] = "random string"


image_data={
    0:{
    'log':"41.9022° N",
    'lat':"12.4539° E",
    'address':"St. Peter's Basilica",
    'description':"The Papal Basilica of Saint Peter in the Vatican (Italian: Basilica Papale di San Pietro in Vaticano), or simply Saint Peter's Basilica (Latin: Basilica Sancti Petri), is a church built in the Renaissance style located in Vatican City, the papal enclave which is within the city of Rome."
    },


    1:{
    'log':"41.8902° N,",
    'lat':"12.4922° E",
    'address':"Colosseum",
    'description':"The Colosseum is famous because it was a place where gladiator fights and executions took place in Ancient Rome.he Flavian Amphitheater (now known as the Roman Colosseum) was built by the order of Emperor Vespasian in 72 AD and took around 8 years to build"
    },

}


db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column('user_id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(50))
    password = db.Column(db.String(200))


def __init__(self, name, email, password, id):
    self.name = name
    self.email = email
    self.password = password
    self.id = id

@app.route("/home")
@app.route("/")
def home():
    print("check")
    return render_template("index.html")

@app.route("/thelink")
def thelink():
    return render_template("show_all.html",users=User.query.all())

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route('/contactSubmit', methods=['GET', 'POST'])
def contactSubmit():
  if request.method == 'GET': 
    phone = request.args.get('phone')
    name=request.args.get('name')
    message=request.args.get('message')
  return Response("submit it")
    

@app.route("/login")
def login():
    if 'email' not in session:
        return render_template("login.html")
    else:
        print("check2")
        return redirect(url_for('home'))




@app.route('/loginsubmit', methods=['GET', 'POST'])
def loginsubmit():
    message=None
    if request.method == 'POST':
        email=request.form['email']
        password=request.form['password']
        if not email or not password:
            message="Please enter all the fields"
            flash(message)
            return redirect(url_for('login'))
        else:
            peter = User.query.filter_by(email=email).first()
            if(not peter is None):
                if(peter.password==password):
                    session['email']=email
                    return redirect(url_for('home'))
                else:
                    message="Invalid Email or Password"
                    flash(message)
                    return redirect(url_for('login'))
    else:
        return "Problem arise due to technical problem..."

@app.route('/logout')
def logout():
    session.pop('email')
    return redirect(url_for('home'))

@app.route("/signup")
def signup():
    if 'email' not in session:
        return render_template("signup.html")
    else:
        return redirect(url_for('home'))


@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        if not request.form['username'] or not request.form['email'] or not request.form['password']:
            flash('Please enter all the fields', 'error')
        else:
            user = User(name=request.form['username'], email=request.form['email'],
                               password=request.form['password'])

            db.session.add(user)
            db.session.commit()
            return redirect(url_for('thelink'))
    return render_template('signup.html')
    
data=None

@app.route('/camera')
def camera():
    if 'email' in session:
        print(data)
        return render_template('camera.html',data=data)
    else:
        return redirect(url_for('login'))


@app.route('/camera_image',methods=['POST'])
def camera_image():
  image=request.files['image']
  image=BytesIO(image.read())
  image=Image.open(image)
  image=image.resize((240,240))
  p=Image_Prediction.Prediction('project12.h5')
  p.load_model()
  print(p.predict(image))
  id=p.predict(image)[0]
  global data
  data=image_data[id]
  print(image_data[id])
  return redirect(url_for('camera'))



if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

    