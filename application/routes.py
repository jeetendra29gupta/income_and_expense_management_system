from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from application.models import db, Category, Transaction
import json
import random

bp = Blueprint('main', __name__)

title = "Income & Expense Management System"
color_names = [
    "Red", "Green", "Blue", "Yellow", "Purple",
    "Orange", "Pink", "Brown", "Black", "White",
    "Gray", "Cyan", "Magenta", "Maroon", "Olive",
    "Lime", "Navy", "Teal", "Aqua", "Silver"
]


@bp.route('/')
def dashboard():
    query_result = db.session.query(Transaction.amount, Category.type).join(Category).all()
    pie_chart_data = list()
    pie_chart_data.append(["Income", sum(a for a, t in query_result if t == 'income')])
    pie_chart_data.append(["Expense", sum(a for a, t in query_result if t == 'expense')])
    pie_chart_data = json.dumps(pie_chart_data)

    transactions = Transaction.query.all()
    column_chart_data = list()
    for tt in transactions:
        column_chart_data.append([tt.category.name, tt.amount, random.choice(color_names)])
    column_chart_data = json.dumps(column_chart_data)
    return render_template('index.html', title=title, pie_chart_data=pie_chart_data,
                           column_chart_data=column_chart_data)


@bp.route('/category')
def category():
    categories = Category.query.all()
    return render_template('category.html', title=title, categories=categories, )


@bp.route('/add_category')
def add_category():
    return render_template('add_category.html', title=title)


@bp.route('/transaction')
def transaction():
    transactions = Transaction.query.all()
    return render_template('transaction.html', title=title, transactions=transactions)


@bp.route('/add_transaction')
def add_transaction():
    categories = Category.query.all()
    return render_template('add_transaction.html', title=title, categories=categories)


@bp.route('/save_category', methods=['POST'])
def save_category():
    name = request.form.get('name')
    type_ = request.form.get('type')
    old_category = Category.query.filter_by(name=name, type=type_).first()
    if not old_category:
        new_category = Category(name=name, type=type_)
        db.session.add(new_category)
        db.session.commit()
    return redirect(url_for('main.category'))


# @bp.route('/')
# def index():
#     categories = Category.query.all()
#     transactions = Transaction.query.all()
#     return render_template('index.html', categories=categories, transactions=transactions)


@bp.route('/save_transaction', methods=['POST'])
def save_transaction():
    amount = float(request.form.get('amount'))
    category_id = int(request.form.get('category'))
    new_transaction = Transaction(amount=amount, category_id=category_id)
    db.session.add(new_transaction)
    db.session.commit()
    return redirect(url_for('main.transaction'))
