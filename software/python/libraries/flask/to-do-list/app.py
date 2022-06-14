from crypt import methods
from email.policy import default
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<Task {self.id}>"

@app.route("/")
def index():
    return render_template('index.html', tasks=Todo.query.order_by(Todo.created_at).all())

@app.route("/create", methods=['POST'])
def create():
    try:
        print(request.form['content'])
        db.session.add(Todo(content=request.form['content']))
        db.session.commit()
        return redirect('/')
    except:
        return "There was an issue adding your task."