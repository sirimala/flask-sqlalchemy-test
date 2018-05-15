from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

class User(db.Model):
	_tablename_ = "users"
	id = db.Column(db.Integer, primary_key=True)
	student_id = db.Column(db.String(100), unique=True, nullable=False)
	email = db.Column(db.String(100), unique=True, nullable=False)
	first_name = db.Column(db.String(100), nullable=True)
	last_name = db.Column(db.String(100), nullable=True)
	display_name = db.Column(db.String(100), nullable=True)
	photo = db.Column(db.LargeBinary)
	gender = db.Column(db.String(100), nullable=True)
	password = db.Column(db.String(100), nullable=True)
	user_type = db.Column(db.String(100), nullable=True)
	student_id_valid = db.Column(db.Boolean, default=False)
	student_deleted = db.Column(db.Boolean, default=False)
	created_at = db.Column(db.DateTime, default=datetime.now(IST))
	Logs = relationship("Log")
	ActivitySubmissions = relationship("ActivitySubmission")
	Enrollments = relationship("Enrollment")

class Log(db.Model):
	_tablename_ = "logs"
	parent_id = db.Column(Integer, ForeignKey('user.id'))
	log_type = db.Column(db.Text, nullable=False) //sign-up, sign-in, logout, video .,
	timestamp = db.Column(db.DateTime, default=datetime.now(IST))
	unit = db.Column(db.String(100), nullable=False)
	activity = db.Column(db.String(100), nullable=False)
	link = db.Column(db.String(100), nullable=False)

class ActivitySubmission(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	parent_id = db.Column(Integer, ForeignKey('user.id'))
	unit = db.Column(db.Text)
	activity = db.Column(db.Text)
	timestamp = db.Column(db.DateTime, default=datetime.now(IST))
	question = db.Column(db.Text)
	response = db.Column(db.Text)
	real_score = db.Column(db.Integer, default=0)
	tentative_score = db.Column(db.Integer, default=0)

class Enrollment(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	parent_id = db.Column(Integer, ForeignKey('user.id'))
	course_id = db.Column(db.String(100), nullable=False)
	timestamp = db.Column(db.DateTime, default=datetime.now(IST))
	enrolled = db.Column(db.Boolean, default=False) //true = enrolled, false= unenrolled by mentor or admin