import traceback

from flask import jsonify, request, Blueprint
from flask_login import login_user, logout_user, current_user, login_required

from datetime import datetime

from mongo import login_manager
from result import Result
from user.user import User

user_blueprint = Blueprint('users', __name__)


@login_manager.user_loader
def load_user(uid):
    return User.objects(uid=uid).first()


@user_blueprint.route('/register', methods=['POST'])
def register_user():
    if not request.json \
            or not 'name' in request.json \
            or not 'password' in request.json \
            or not 'email' in request.json:
        return Result.gen_fail(None, 'Request not Json or miss name/email/password')
    elif User.objects(name=request.json['name']).first():

        return Result.gen_fail(None, 'Name is already existed.')
    else:
        user = User(
            uid=User.objects().count() + 1,
            name=request.json['name'],
            email=request.json['email'] if 'email' in request.json else "",
            password=request.json['password'],
            createtime=datetime.now()
        )
        try:
            user.save()
        except Exception as ex:

            traceback.print_exc()

            return Result.gen_fail(None, 'Register error.')

    return Result.gen_success({'uid': user.get_id()}, 'Register success.')


@user_blueprint.route('/login', methods=['POST'])
def login():
    if not request.json or not 'name' in request.json or not 'password' in request.json:
        return Result.gen_fail(None, 'Request not Json or miss name/password')
    else:
        user = User.objects(
            name=request.json['name'], password=request.json['password']).first()
    if user:
        login_user(user)
        return Result.gen_success({'uid': user.get_id()}, 'Login success.')
    else:

        return Result.gen_fail(None, 'Login fail.')


@user_blueprint.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return Result.gen_success(None, 'Logout success.')


@user_blueprint.route('/user', methods=['GET'])
def get_user():
    if current_user.is_authenticated:

        return Result.gen_success({'user': current_user.to_json()})
    else:
        return Result.gen_fail(None, 'Not login.')


@user_blueprint.route('/user/email', methods=['PUT'])
@login_required
def put_user_email():
    if not request.json or not 'email' in request.json:
        return Result.gen_fail(None, 'Request not Json or miss email')
    else:
        current_user.email = request.json['email']
        try:
            current_user.save()
        except Exception:
            return Result.gen_fail(None, 'Modify email error.')
        return Result.gen_success({'uid': current_user.uid}, 'Email has been modified.')


@user_blueprint.route('/user/password', methods=['PUT'])
@login_required
def put_user_password():
    if not request.json or not 'current_password' in request.json or not 'new_password' in request.json:

        return Result.gen_fail(None, 'Request not Json or miss current_password/new_password')
    else:
        current_password = current_user.password
    if not request.json['current_password'] == current_password:
        return Result.gen_fail(None, 'current_password is not right.')
    else:
        current_user.password = request.json['new_password']
        try:
            current_user.save()
        except Exception:
            return Result.gen_fail(None, 'Modify password error.')

        return Result.gen_success({'uid': current_user.uid}, 'password has been modified.')

