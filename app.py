from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime

#create a flask instance
app = Flask(__name__)

#add database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
#new slq db
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:a2zSaintz@localhost/our_users'
#secret key
app.config['SECRET_KEY'] = "my secret key is 1"
#initialize the database
db = SQLAlchemy(app)

#Create a Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    #create A String

    def __repr__(self):
        return '<Name %r>' % self.name
    



#create a form class
class NamerForm(FlaskForm):
    name = StringField("What is your name", validators=[DataRequired()])
    submit = SubmitField("Submit")

class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField("Submit")
#create a route decrator
@app.route('/')

# def index():
#     return "<h1>Hello World!</h1>"


def index():
    first_name = "Aaron"
    favorite_pizza = ["Pepperoni", "Cheese"]
    return render_template("index.html", first_name=first_name, favorite_pizza=favorite_pizza)

@app.route('/user/<name>')

def user(name):
    return render_template("user.html", user_name=name)


@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    form = UserForm()
    name = None
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email = form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        flash("User added successfully!")
    our_users = Users.query.order_by(Users.date_added)
    return render_template("add_user.html",
                           form = form,
                           name = name,
                           our_users=our_users
                           )

#error pages
#invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

#Internal error
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500


#create name page
@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NamerForm()
    #validate form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Form Submitted Successfully!")

    return render_template("name.html",
                    name = name,
                    form = form
                    )

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)