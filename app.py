from flask import Flask, render_template, request, redirect
from datetime import datetime
from models import db, Expense

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.before_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    expenses = Expense.query.order_by(Expense.date.desc()).all()
    return render_template('index.html', expenses=expenses)

@app.route('/add', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        title = request.form['title']
        amount = float(request.form['amount'])
        category = request.form['category']
        date = datetime.strptime(request.form['date'], '%Y-%m-%d')

        new_expense = Expense(title=title, amount=amount, category=category, date=date)
        db.session.add(new_expense)
        db.session.commit()
        return redirect('/')

    return render_template('add_expense.html')

if __name__ == '__main__':
    app.run(debug=True)
