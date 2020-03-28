from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

# initializes our app
app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
    app.debug = True

    # connection to Postgres                 #postgres,   username:password@localhost/database_name
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:jeonju123@localhost/restaurant_feedback'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# sets database object to db, query database
db = SQLAlchemy(app)


# creates models, similar with mongoose
class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200), unique=True)
    email = db.Column(db.Text())
    waiter = db.Column(db.String(50))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    # constructor/initializer
    def __init__(self, customer, email, waiter, rating, comments):
        self.customer = customer
        self.email = email
        self.waiter = waiter
        self.rating = rating
        self.comments = comments


# creates home page route
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        customer = request.form['customer']  # name of field from index input file
        waiter = request.form['waiter']
        rating = request.form['rating']
        comments = request.form['comments']
        customer_email = request.form['customer_email']
        # print(customer, dealer, rating, comments)

        # validation that customer enters data into fields
        if customer == '' or waiter == '':
            return render_template('index.html', message='Please enter required fields')
        return render_template('success.html')


if __name__ == '__main__':
    app.run()
