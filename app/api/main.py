from app.api import bp
from app.models import Users, Source, UsersRegex, Task, LastParseResults
from flask import jsonify, abort, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api.errors import bad_request
from app import db


@bp.route('/api/users/<int:id>', methods=['GET'])
@jwt_required()
def get_user(id):
    user_id = get_jwt_identity()
    user = Users.query.filter_by(id=id).first_or_404()
    if int(user_id) != int(id):
        abort(401)
    return jsonify({'user': user.email, 'id': user.id})


@bp.route('/api/edit_profile/<int:id>', methods=['PUT'])
@jwt_required()
def edit_profile(id):
    user_id = get_jwt_identity()
    if int(user_id) != int(id):
        abort(401)
    user = Users.query.filter_by(id=id).first_or_404()
    data = request.json or {}
    if 'email' not in data:
        return bad_request('must include email field')
    if data['email'] != user.email and Users.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    for key, value in data.items():
        setattr(user, key, value)
    db.session.commit()
    return jsonify({'user': user.email, 'id': user.id})


@bp.route('/users/edit_password', methods=['PUT'])
@jwt_required()
def edit_password():
    user_id = get_jwt_identity()
    user = Users.query.filter_by(id=user_id).first_or_404()
    data = request.json or {}
    if 'current_password' not in data or 'password' not in data:
        return bad_request('must include current_password and password fields')
    if not user.authenticate(email=user.email, password=data['current_password']):
        return bad_request('wrong password')
    user.set_password(data['password'])
    db.session.commit()
    return jsonify({'user': user.email, 'id': user.id})


@bp.route('/accounts', methods=['GET'])
@jwt_required()
def get_accounts():
    user_id = get_jwt_identity()
    user = Users.query.filter_by(id=user_id).first_or_404()
    result = user.user_tweeter_accounts()
    resp = [{'id': i.id, 'user_id': i.user_id, 'account': i.account} for i in result]
    return jsonify(resp)


@bp.route('/accounts', methods=['DELETE'])
@jwt_required()
def delete_accounts():
    data = request.json or {}
    if 'id' not in data:
        return bad_request('must include id field')
    user_id = get_jwt_identity()
    user = Users.query.filter_by(id=user_id).first_or_404()
    if not user.accounts.filter_by(id=data['id']).first():
        return bad_request('There is not account with this id')
    user.remove_tweeter_account(data['id'])
    db.session.commit()
    return jsonify({'status': 'OK'})


@bp.route('/accounts', methods=['POST'])
@jwt_required()
def create_account():
    data = request.json or {}
    if 'account' not in data:
        return bad_request('must include account field')
    user_id = get_jwt_identity()
    user = Users.query.filter_by(id=user_id).first_or_404()
    account = Source(account=data['account'], author=user)
    db.session.add(account)
    db.session.commit()
    resp = [
        {'id': i.user_id, 'account': i.account}
        for i in Source.query.filter_by(user_id=user.id).order_by(Source.created.desc())
    ]
    return jsonify(resp)


@bp.route('/keys', methods=['GET'])
@jwt_required()
def get_keys():
    user_id = get_jwt_identity()
    user = Users.query.filter_by(id=user_id).first_or_404()
    result = user.user_regs()
    resp = [{'id': i.id, 'user_id': i.user_id, 'regex': i.regex} for i in result]
    return jsonify(resp)


@bp.route('/keys', methods=['DELETE'])
@jwt_required()
def delete_key():
    data = request.json or {}
    if 'id' not in data:
        return bad_request('must include id field')
    user_id = get_jwt_identity()
    user = Users.query.filter_by(id=user_id).first_or_404()
    if not user.regs.filter_by(id=data['id']).first():
        return bad_request('There is not key with this id')
    user.remove_users_regex(id=data['id'])
    db.session.commit()
    return jsonify({'status': 'OK'})


@bp.route('/keys', methods=['POST'])
@jwt_required()
def create_key():
    data = request.json or {}
    if 'key' not in data:
        return bad_request('must include key field')
    user_id = get_jwt_identity()
    user = Users.query.filter_by(id=user_id).first_or_404()
    regex = UsersRegex(regex=data['key'].strip(), author=user)
    db.session.add(regex)
    db.session.commit()
    resp = [
        {'id': i.user_id, 'regex': i.regex}
        for i in UsersRegex.query.filter_by(user_id=user.id).order_by(UsersRegex.created.desc())
    ]
    return jsonify(resp)


@bp.route('/last_results', methods=['GET'])
@jwt_required()
def get_last_results():
    pass


@bp.route('/last_results', methods=['DELETE'])
@jwt_required()
def delete_last_results():
    pass


@bp.route('/parsing', methods=['GET'])
@jwt_required()
def parser():
    user_id = get_jwt_identity()
    user = Users.query.filter_by(id=user_id).first_or_404()
    accounts = user.user_tweeter_accounts_for_p()
    keys = user.user_regs_for_p()
    if user.get_task_in_progress('scrap'):
        return bad_request('A parsing task is currently in progress')
    if accounts and keys:
        parsed_tweets = user.launch_tasks('scrap', 'parsing')
        db.session.commit()
        return jsonify(parsed_tweets)
    else:
        return bad_request('First you must add some accounts and keys')

