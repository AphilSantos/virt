from flask import Flask, render_template

#create a flask instance
app = Flask(__name__)


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


#error pages
#invalid URL
@app.errorhandler(404)
def page_not_found(e):
    render_template("404.html"), 404

#Internal error
@app.errorhandler(500)
def page_not_found(e):
    render_template("500.html"), 500

    