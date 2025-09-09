from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model
class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    data_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"


# Create tables once
with app.app_context():
    db.create_all()


# Home route -> Add todo & show table
@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        title = request.form.get('title')
        desc = request.form.get('desc')
        if title and desc:
            todo = Todo(title=title, desc=desc)
            db.session.add(todo)
            db.session.commit()
        return redirect("/")  # redirect after POST
    allSite = Todo.query.all()
    return render_template('index.html', allSite=allSite)


# Delete route
@app.route("/delete/<int:sno>")
def delete(sno):
    todo = Todo.query.get_or_404(sno)
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")


# Update route
@app.route("/update/<int:sno>", methods=['GET', 'POST'])
def update(sno):
    todo = Todo.query.get_or_404(sno)
    if request.method == 'POST':
        todo.title = request.form['title']
        todo.desc = request.form['desc']
        db.session.commit()
        return redirect("/")
    return render_template("update.html", todo=todo)


# Show all todos route
@app.route("/show")
def show():
    allSite = Todo.query.all()
    return render_template("show.html", allSite=allSite)


if __name__ == "__main__":
    app.run(debug=True, port=8000)
