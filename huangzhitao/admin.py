#coding: utf-8
#author: shenminjun


import json
from flask import Blueprint, render_template, request, session
from website.models import db


app = Blueprint("admin",__name__)


@app.route('/admin')
def index():
    return render_template('admin/admin.html')


@app.route('/admin/login', methods=['POST', ])
def login():
    data = request.form.to_dict()
    res = db.loginAuth(**data)
    if res and res['permission'] == 0:
        session['username'] = res['user']
        session['permission'] = res['permission']
        return 'yes'
    return 'no'


@app.route('/admin/home')
def home():
    username = session['username']
    permission = session['permission']
    if username and permission == 0:
        return render_template('/admin/home.html')
    return render_template('admin/admin.html')


@app.route('/admin/account')
def account():
    return render_template('/admin/account.html')


@app.route('/admin/logout')
def logout():
    session.pop('type', None)
    return render_template('admin/admin.html')


@app.route('/admin/account/details')
def account_details():
    params = request.args.to_dict()
    item = db.require_account(**params)
    count = len(item) if item else 0
    response = {
        "code": 0,
        "msg": "",
        "count": count,
        "data": item
    }
    return json.dumps(response)


@app.route('/admin/newAccount')
def newAccount():
    return render_template('/admin/newAccount.html')


@app.route('/admin/newAccount/insert', methods=["POST", ])
def newAccount_insert():
    data = request.form.to_dict()
    
    db.save_data('account', **data)
    return '保存成功！'


@app.route('/admin/account/delete')
def account_delete():
    name = request.args['user']
    db.delete_account('account', name)
    return '删除成功！'


@app.route('/admin/editAccount')
def editAccount():
    params = request.args.to_dict()
    data = db.require_account(**params)
    return render_template('/admin/editAccount.html', **data)


if __name__ == '__main__':
    pass
    # make_directory()
