from flask import Flask, session, redirect, url_for, escape, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import enum

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.secret_key = 'any random string'

class UserType(enum.Enum):
    admin = "admin"
    mentor = "mentor"
    student = "student"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    photo = db.Column(db.LargeBinary)
    gender = db.Column(db.String(100))
    password = db.Column(db.String(100))
    user_type = db.Column(db.Enum("admin", "mentor", "student", user_type="user_types"), default="student")
    is_student_id_valid = db.Column(db.Boolean, default=False)
    is_student_deleted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    logs = db.relationship("Log", backref='user')
    activitySubmissions = db.relationship("ActivitySubmission", backref='user')
    enrollments = db.relationship("Enrollment", backref='user')

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    log_type = db.Column(db.Text, nullable=False) #sign-up, sign-in, logout, video .,
    timestamp = db.Column(db.DateTime, default=datetime.now())
    unit = db.Column(db.String(100), nullable=False)
    activity = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(100), nullable=False)

class ActivitySubmission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    unit = db.Column(db.Text)
    activity = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.now())
    question = db.Column(db.Text)
    response = db.Column(db.Text)
    real_score = db.Column(db.Integer, default=0)
    tentative_score = db.Column(db.Integer, default=0)

class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    course_id = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now())
    enrolled = db.Column(db.Boolean, default=False) #true = enrolled, false= unenrolled by mentor or admin

@app.route('/signin', methods = ['GET', 'POST'])
def login():
   if request.method == 'POST':
      session['username'] = request.form['username']
      return "you are logged in %s"%session['username']
   return '''
    
   <form method="post">
      <input type="text" name="username">
      <input type="submit" value="Login">
   </form>
    
   '''
@app.route('/signout')
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   return "you are logged out"

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        try:
            student_id = request.form['student_id']
            first_name = request.form['first_name']
            email = request.form['email']
            user = User()
            is_exist = user.query.filter_by(student_id=student_id).first()
            if is_exist is None:
                user.student_id = student_id
                user.first_name = first_name
                user.email = email
                # user.user_type = ""
                db.session.add(user)
                db.session.commit()
                return "user with ID %s successfully created. <a href='/signin'>signin</a>"%student_id
            return "This student ID already exists. Please contact admin"
        except Exception as e:
            print(e)
    return '''

    <form method="post">
      student ID: <input type="text" name="student_id"><br>
      First Name: <input type="text" name="first_name"><br>
      Email: <input type="text" name="email"><br>
      <input type="submit" value="Sing Up">
    </form>

    '''

if __name__ == '__main__':
   app.run(host='0.0.0.0', debug=True)