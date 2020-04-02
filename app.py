from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    task = db.Column(db.String(200), nullable=False)
    dateCreated = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['POST', 'GET'])

def index():
    if request.method == 'POST':
        content = request.form['task']
        new_task = Todo(task = content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "Error adding task"
    else:
        tasks = Todo.query.order_by(Todo.dateCreated).all()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    taskToDelete = Todo.query.get_or_404(id)

    try:
        db.session.delete(taskToDelete)
        db.session.commit()
        return redirect('/')
    except:
        return 'error Deleting'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['task']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'error updating'

    else:
        return render_template('update.html', tasky=task)


app.run(debug=True)