from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(35), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    role = db.Column(db.String(15), nullable=False)

    def __repr__(self):
        return '<Task %r>' %self.id

@app.route('/', methods =['POST', 'GET'])
def index():
    if request.method == 'POST':
        exists = Todo.query.filter_by(email=request.form["username"]).scalar() is not None
        if exists:
            users = Todo.query.filter_by(email=request.form["username"]).first()
            if users.password == request.form["pass"]:
                return render_template('user.html', user=users.role)
            else:
                return render_template('index.html', wrong="True")
        else:
            return render_template('index.html', wrong="pass")
    else:
        return render_template('index.html')

@app.route('/delete/<int:id>')
def delete(id):
    task_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_delete)
        db.session.commit()
        users = Todo.query.all()
        return render_template('manage.html', users=users)
    except:
        return "Error while deleting"

@app.route('/update/<int:id>', methods = ['POST', 'GET'])
def update(id):
    user = Todo.query.get_or_404(id)

    if request.method == 'POST':
        user.email = request.form['email']
        user.password = request.form['pass']
        user.role = request.form['role']

        try:
            db.session.commit()
            users = Todo.query.all()
            return render_template('manage.html', users=users)
        except:
            return "Update Error"
    else:
        return render_template('update.html', user = user)

@app.route('/user/<string:email_ad>', methods = ['POST', 'GET'])
def signin(email_ad):
    users = Todo.query.get_or_404(email_ad)

@app.route('/manage')
def manage():
    users = Todo.query.all()
    return render_template('manage.html', users=users)

@app.route("/add_role", methods = ['POST', 'GET'])
def add():
    if request.method == 'POST':
        emails = request.form['email']
        pswd = request.form['pass']
        roles = request.form['role']
        new_user = Todo(email=emails, password=pswd, role=roles)

        try:
            db.session.add(new_user)
            db.session.commit()
            users = Todo.query.all()
            return render_template('manage.html', users=users)
        except:
            return "error"
    else:
        return render_template('add_role.html')

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                 endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

if __name__ == "__main__":
    app.run(debug=True)
