from flask import Flask, request, jsonify,Blueprint
from flask_marshmallow import Marshmallow
from app.models import User, Group, Role
from app import ma


api = Blueprint('api', __name__)

class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id', 'confirmed','first_name','last_name', 'email', 'active')

user_schema = UserSchema()
users_schema = UserSchema(many=True)


class GroupSchema(ma.Schema):
    users = ma.Nested(UserSchema, many=True)

    class Meta:
        # Fields to expose
        fields = ('id', 'name','users')

group_schema = GroupSchema()
groups_schema = GroupSchema(many=True)


class RoleSchema(ma.Schema):
    users = ma.Nested(UserSchema, many=True)

    class Meta:
        # Fields to expose
        fields = ('id', 'name','default','permissions','users')

role_schema = RoleSchema()
roles_schema = RoleSchema(many=True)


@api.route("/user", methods=["GET"])
def get_user():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result)


# endpoint to get user detail by id
@api.route('/user/<int:id>', methods=["GET"])
def user_detail(id):
    user = User.query.get(id)
    return user_schema.jsonify(user)

@api.route("/group", methods=["GET"])
def get_group():
    all_groups = Group.query.all()
    result = groups_schema.dump(all_groups)
    return jsonify(result)

# endpoint to get group detail by id
@api.route('/group/<int:id>', methods=["GET"])
def group_detail_id(id):
    group = Group.query.get(id)
    return group_schema.jsonify(group)

@api.route('/group/<string:name>', methods=["GET"])
def group_detail_name(name):
    group = Group.query.filter_by(name=name).first()
    return group_schema.jsonify(group)

@api.route("/role", methods=["GET"])
def get_role():
    all_roles = Role.query.all()
    result = roles_schema.dump(all_roles)
    return jsonify(result)

# endpoint to get group detail by id
@api.route('/role/<int:id>', methods=["GET"])
def role_detail_id(id):
    role = Role.query.get(id)
    return role_schema.jsonify(role)

@api.route('/role/<string:name>', methods=["GET"])
def role_detail_name(name):
    role = Role.query.filter_by(name=name).first()
    return role_schema.jsonify(role)