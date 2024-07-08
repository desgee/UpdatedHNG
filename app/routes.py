from flask import Blueprint, jsonify, request
from app.models import User, Organisation
from app import db
from flask_jwt_extended import jwt_required, get_jwt_identity

route_bp = Blueprint('main', __name__)

@route_bp.route('/')
def home():

    return jsonify({"status": "success", "message": "api connected successfully"}), 200

@route_bp.route('/api/users/<string:id>', methods=['GET'])
@jwt_required()
def get_user(id):
    current_user_id = get_jwt_identity()
    
    user = User.query.filter_by(userId=current_user_id).first()

    if not user:
        return jsonify({"status": "error", "message": "User not found"}), 404
    
    if str(user.userId) != id:
        return jsonify({"status": "error", "message": "Unauthorized access"}), 403
    
    return jsonify({
        "status": "success",
        "message": "User record retrieved",
        "data": {
            "userId": user.userId,
            "firstName": user.firstName,
            "lastName": user.lastName,
            "email": user.email,
            "phone": user.phone
        }
    }), 200

@route_bp.route('/api/organisations', methods=['GET'])
@jwt_required()
def get_organisations():
    current_user_id = get_jwt_identity()
    user = User.query.filter_by(userId=current_user_id).first()

    if not user:
        return jsonify({"status": "error", "message": "User not found"}), 404
    
    organisations = user.organisations
    orgs_data = [{
        "orgId": org.orgId,
        "name": org.name,
        "description": org.description
    } for org in organisations]

    return jsonify({
        "status": "success",
        "message": "Organisations retrieved",
        "data": {
            "organisations": orgs_data
        }
    }), 200

@route_bp.route('/api/organisations/<string:org_id>', methods=['GET'])
@jwt_required()
def get_organisation(org_id):
    current_user_id = get_jwt_identity()
    user = User.query.filter_by(userId=current_user_id).first()

    if not user:
        return jsonify({"status": "error", "message": "User not found"}), 404

    organisation = Organisation.query.filter_by(orgId=org_id).first()

    if not organisation or organisation not in user.organisations:
        return jsonify({"status": "error", "message": "Organisation not found or access denied"}), 404
    
    return jsonify({
        "status": "success",
        "message": "Organisation record retrieved",
        "data": {
            "orgId": organisation.orgId,
            "name": organisation.name,
            "description": organisation.description
        }
    }), 200

@route_bp.route('/api/organisations/<string:org_id>/users', methods=['POST'])
@jwt_required()
def add_user_to_organisation(org_id):
    current_user_id = get_jwt_identity()
    user = User.query.filter_by(userId=current_user_id).first()

    if not user:
        return jsonify({"status": "error", "message": "User not found"}), 404

    organisation = Organisation.query.filter_by(orgId=org_id).first()

    if not organisation or organisation not in user.organisations:
        return jsonify({"status": "error", "message": "Organisation not found or access denied"}), 404

    data = request.get_json()
    target_user = User.query.filter_by(userId=data.get('userId')).first()

    if not target_user:
        return jsonify({"errors": [{"field": "userId", "message": "User not found"}]}), 422

    organisation.users.append(target_user)
    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "User added to organisation successfully"
    }), 200
