from flask import Blueprint, request, jsonify
from app import db
from app.models import User, BlogPost
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

bp = Blueprint('api', __name__)

@bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already exists'}), 400
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already exists'}), 400
    user = User(username=data['username'], email=data['email'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@bp.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        token = create_access_token(identity=user.id)
        return jsonify({'token': token}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@bp.route('/posts', methods=['POST'])
@jwt_required()
def create_post():
    data = request.get_json()
    user_id = get_jwt_identity()
    post = BlogPost(title=data['title'], body=data['body'], user_id=user_id)
    db.session.add(post)
    db.session.commit()
    return jsonify({'message': 'Post created successfully'}), 201

@bp.route('/posts', methods=['GET'])
def get_posts():
    posts = BlogPost.query.all()
    return jsonify([{'id': post.id, 'title': post.title, 'body': post.body} for post in posts]), 200

@bp.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    return jsonify({'id': post.id, 'title': post.title, 'body': post.body}), 200

@bp.route('/posts/<int:post_id>', methods=['PUT'])
@jwt_required()
def update_post(post_id):
    data = request.get_json()
    post = BlogPost.query.get_or_404(post_id)
    if post.user_id != get_jwt_identity():
        return jsonify({'message': 'Unauthorized'}), 403
    post.title = data['title']
    post.body = data['body']
    db.session.commit()
    return jsonify({'message': 'Post updated successfully'}), 200

@bp.route('/posts/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    if post.user_id != get_jwt_identity():
        return jsonify({'message': 'Unauthorized'}), 403
    db.session.delete(post)
    db.session.commit()
    return jsonify({'message': 'Post deleted successfully'}), 200
