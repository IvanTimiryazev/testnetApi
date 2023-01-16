from app.api import bp
from app.models import Users, Source, UsersRegex, Task, LastParseResults
from flask import jsonify, request
from app import db
from app.api.errors import bad_request


@bp.route('/register', methods=['POST'])
def register():
    data = request.json or {}
    if 'email' not in data or 'password' not in data:
        return bad_request('must include email and password fields')
    if Users.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    user = Users(email=data['email'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    token = user.get_token()
    return jsonify({'access_token': token})


@bp.route('/login', methods=['POST'])
def login():
    data = request.json or {}
    if 'email' not in data or 'password' not in data:
        return bad_request('must include email and password fields')
    user = Users.authenticate(email=data['email'], password=data['password'])
    if user:
        token = user.get_token()
        return jsonify({'access_token': token})
    else:
        return bad_request('wrong password')







