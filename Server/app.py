import json
import uuid
import time
from flask import Flask
from flask import request
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
db = SQLAlchemy(app)

class User(db.Model):
    displayName = db.Column(db.String(120), primary_key=True)
    password = db.Column(db.String(120), nullable=False)
    emailAddress = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.displayName

    def serialize(self):
        return {
            "displayName": self.displayName,
            "emailAddress": self.emailAddress
        }

class Message(db.Model):
    messageId = db.Column(db.String(240), primary_key=True)
    sender = db.Column(db.String(120), nullable=False)
    receiver = db.Column(db.String(120), nullable=False)
    message = db.Column(db.String(120), nullable=False)

    def serialize(self):
        return {
            "messageId": self.messageId,
            "sender": self.sender,
            "receiver": self.receiver,
            "message": self.message
        }

def addUserToDB(username, password, email):
    new_user = User(displayName=username, password=password, emailAddress=email)
    db.session.add(new_user)
    db.session.commit()

def addMessageToDB(sender, receiver, message):
    messageId = str(uuid.uuid1())
    new_message = Message(messageId=messageId, sender=sender, receiver=receiver, message=message)
    db.session.add(new_message)
    db.session.commit()

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/login", methods=["GET", "POST"])
def login():
    perf_file = open("performance_file.txt", "a")
    tic = time.perf_counter()
    request_data = json.loads(request.data)
    str(request_data)
    existing_user = User.query.filter(
        User.displayName == request_data["email"]
    ).first()
    toc = time.perf_counter()
    perf_file.write("Logging user {}: {:0.4f}\n".format(request_data["email"], (toc - tic)))
    perf_file.close()
    if existing_user:
        return {
            "status": 200,
            "body": json.dumps(existing_user.serialize())
        }
    
    return {
        "status": 500
    }

@app.route("/createuser", methods=["GET"])
def create_user():
    perf_file = open("performance_file.txt", "a")
    tic = time.perf_counter()
    name = request.args.get('name')
    password = request.args.get('password')
    email = request.args.get('email')
    addUserToDB(name, password, email)
    toc = time.perf_counter()
    perf_file.write("Creating user {}: {:0.4f}\n".format(name, (toc - tic)))
    perf_file.close()
    return {
        "status": 200
    }

@app.route("/getrecipients", methods=["GET", "POST"])
def get_recipients():
    perf_file = open("performance_file.txt", "a")
    tic = time.perf_counter()
    recipients = User.query.all()
    serialized_recipients = []
    for recipient in recipients:
        serialized_recipients.append(recipient.serialize())
    toc = time.perf_counter()
    perf_file.write("Getting recipients: {:0.4f}\n".format((toc - tic)))
    perf_file.close()
    return {
        "status": 200,
        "body": json.dumps(serialized_recipients)
    }
    
@app.route("/sendmessage", methods=["POST"])
def send_message():
    perf_file = open("performance_file.txt", "a")
    tic = time.perf_counter()
    request_data = json.loads(request.data)
    addMessageToDB(request_data["sender"], request_data["receiver"], request_data["message"])
    toc = time.perf_counter()
    perf_file.write("Send message: {:0.4f}\n".format((toc - tic)))
    return {
        "status": 200
    }

@app.route("/getmessages", methods=["GET"])
def get_message():
    perf_file = open("performance_file.txt", "a")
    tic = time.perf_counter()
    name = request.args.get('receiver')
    messages = Message.query.filter_by(receiver=name).all()
    serialized_messages = []
    for message in messages:
        serialized_messages.append(message.serialize())
    toc = time.perf_counter()
    perf_file.write("Get message: {:0.4f}\n".format((toc - tic)))
    return {
        "status": 200,
        "body": json.dumps(serialized_messages)
    }

if __name__ == "__main__":
    db.session.commit()
    db.drop_all()
    db.create_all()
    addUserToDB('akriti', 'password', 'akritia1@umbc.edu')
    addUserToDB('sourabh', 'password', 'sssaha2@ncsu.edu')
    app.run()