from marshmallow import ValidationError
from module import db
from module import app
from datetime import datetime
from flask import make_response, request, jsonify
import json
from module.schemas import UserSchema, CategorySchema, RecordSchema
from module.dbModels import User, Category, Record

# Flask routes

@app.route("/")
def home():
    return "Backend Project Maksym G."

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    response = {
        'status': 'UP',
        'timestamp': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    }
    response = json.dumps(response, indent=4)
    return make_response((response, 200, {'Content-Type': 'application/json'}))

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_schema = UserSchema(many=True)
    return jsonify(user_schema.dump(users)), 200


@app.route('/user', methods=['POST'])
def add_user():
    user_schema = UserSchema()
    try:
        user_data = user_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    new_user = User(name=user_data['name'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'user_id': new_user.id}), 201

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        user_schema = UserSchema()
        return jsonify(user_schema.dump(user)), 200
    return jsonify({'error': 'User not found'}), 404

@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({}), 204
    return jsonify({'error': 'User not found'}), 404

@app.route('/category', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    category_schema = CategorySchema(many=True)
    return jsonify(category_schema.dump(categories)), 200


@app.route('/category', methods=['POST'])
def add_category():
    category_schema = CategorySchema()
    try:
        category_data = category_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    new_category = Category(category_name=category_data['category_name'])
    db.session.add(new_category)
    db.session.commit()
    return jsonify({'category_id': new_category.id}), 201

@app.route('/category/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    category = Category.query.get(category_id)
    if category:
        db.session.delete(category)
        db.session.commit()
        return jsonify({}), 204
    return jsonify({'error': 'Category not found'}), 404

@app.route('/record', methods=['POST'])
def add_record():
    record_schema = RecordSchema()
    try:
        record_data = record_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    new_record = Record(
        user_id=record_data['user_id'],
        category_id=record_data['category_id'],
        timestamp=datetime.utcnow(),
        amount=record_data['amount']
    )
    db.session.add(new_record)
    db.session.commit()
    return jsonify({'record_id': new_record.id}), 201

@app.route('/record', methods=['GET'])
def get_records():
    user_id = request.args.get('user_id')
    category_id = request.args.get('category_id')
    records = Record.query.filter(
        (Record.user_id == user_id) if user_id else True,
        (Record.category_id == category_id) if category_id else True
    ).all()
    record_schema = RecordSchema(many=True)
    return jsonify(record_schema.dump(records)), 200

@app.route('/record/<int:record_id>', methods=['GET'])
def get_record_by_id(record_id):
    record = Record.query.get(record_id)
    if record is None:
        return jsonify({'message': 'Record not found'}), 404


    record_schema = RecordSchema()
    return jsonify(record_schema.dump(record)), 200

@app.route('/record/<int:record_id>', methods=['DELETE'])
def delete_record(record_id):
    record = Record.query.get(record_id)
    if record:
        db.session.delete(record)
        db.session.commit()
        return jsonify({}), 204
    return jsonify({'error': 'Record not found'}), 404


if __name__ == '__main__':
    app.run()
