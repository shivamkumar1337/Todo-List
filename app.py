from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    status = db.Column(db.Boolean, default=False) 
    date_created = db.Column(db.DateTime, default=datetime.utcnow) 

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"
    
@app.route('/', methods=['GET', 'POST'])
def hello_world():
    
    if request.method=='POST':
        task = request.form['task']
        desc = request.form['desc']
        todo = Todo(title=task, desc=desc)
        db.session.add(todo)
        db.session.commit()

    alltodo = Todo.query.all()
    # print(alltodo)
    return render_template('index.html', alltodo=alltodo)

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method=='POST':
        task = request.form['task']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = task
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)

@app.route('/change_status/<int:sno>', methods=['GET', 'POST'])
def change_status(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    status = request.form.get('completed', False, type=bool)
    todo.status = status
    db.session.add(todo)
    db.session.commit()
    return redirect('/')
    

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True, port=8000)