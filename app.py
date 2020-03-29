from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

# initializes our app
app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
    app.debug = True

    # connection to Postgres                 #postgres,   username:password@localhost/database_name
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:jeonju123@localhost/restaurant_feedback'
else:

    # production database
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://yxgxmedzznltne:2da5d036b511c53add231bf8c91adce5bde4387565c1435680d7c4439668c5c5@ec2-35-174-88-65.compute-1.amazonaws.com:5432/d73mc5h8pq4nn4'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# sets database object to db, query database
db = SQLAlchemy(app)


# creates models, similar with mongoose
class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(100), unique=True)
    customer_email = db.Column(db.Text())
    waiter = db.Column(db.String(50))
    rating = db.Column(db.Text)
    comments = db.Column(db.Text())

    # constructor/initializer
    def __init__(self, customer, customer_email, waiter, rating, comments):
        self.customer = customer
        self.customer_email = customer_email
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

        # checks to make sure that customer doesnt already exist
        if db.session.query(Feedback).filter(Feedback.customer == customer).count() == 0:
            # add data to database
            data = Feedback(customer, customer_email, waiter, rating, comments)
            db.session.add(data)
            db.session.commit()

            return render_template('success.html')
        return render_template('index.html', message='You have already submitted feedback!')


if __name__ == '__main__':
    app.run()
