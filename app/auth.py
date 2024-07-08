from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models import User, Organisation
from app import db

auth = Blueprint("auth", __name__, url_prefix='/auth')

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    required_fields = ["firstName", "lastName", "email", "password"]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({"errors": [{"field": field, "message": f"{field} is required"} for field in missing_fields]}), 422
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"errors": [{"field": "email", "message": "Email already exists"}]}), 422

    new_user = User(
        firstName=data['firstName'],
        lastName=data['lastName'],
        email=data['email'],
        phone=data.get('phone')
    )

    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()

    org_name = f"{new_user.firstName}'s Organisation"
    new_org = Organisation(name=org_name)
    new_user.organisations.append(new_org)

    db.session.add(new_user)
    db.session.add(new_org)
    db.session.commit()

    access_token = create_access_token(identity=str(new_user.userId))

    return jsonify({
        "status": "success",
        "message": "Registration successful",
        "data": {
            "accessToken": access_token,
            "user": {
                "userId": str(new_user.userId),
                "firstName": new_user.firstName,
                "lastName": new_user.lastName,
                "email": new_user.email,
                "phone": new_user.phone
            }
        }
    }), 201


@auth.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()

    required_fields = ["email", "password"]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({"errors": [{"field": field, "message": f"{field} is required"} for field in missing_fields]}), 422

    user = User.query.filter_by(email=data['email']).first()
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=str(user.userId))

        return jsonify({
            "status": "success",
            "message": "Login successful",
            "data": {
                "accessToken": access_token,
                "user": {
                    "userId": str(user.userId),
                    "firstName": user.firstName,
                    "lastName": user.lastName,
                    "email": user.email,
                    "phone": user.phone
                }
            }
        }), 200
    else:
        return jsonify({"errors": [{"field": "login", "message": "Invalid email or password"}]}), 401