from marshmallow import ValidationError
from module import db
from module import app
from datetime import datetime
from flask import make_response, request, jsonify
import json
from module.schemas import UserSchema, CategorySchema, RecordSchema, CurrencySchema
from module.dbModels import User, Category, Record, Currency

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

@app.route('/currency', methods=['POST'])
def add_currency():
    currency_schema = CurrencySchema()
    try:
        currency_data = currency_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    new_currency = Currency(**currency_data)
    db.session.add(new_currency)
    db.session.commit()
    return jsonify({'currency_id': new_currency.id}), 201

@app.route('/currency', methods=['GET'])
def get_currencies():
    currencies = Currency.query.all()
    currency_schema = CurrencySchema(many=True)
    return jsonify(currency_schema.dump(currencies)), 200

@app.route('/currency/<int:currency_id>', methods=['DELETE'])
def delete_currency(currency_id):
    currency = Currency.query.get(currency_id)
    if currency:
        db.session.delete(currency)
        db.session.commit()
        return jsonify({}), 204
    return jsonify({'error': 'Currency not found'}), 404

@app.route('/user/<int:user_id>/set_currency', methods=['POST'])
def set_user_currency(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    try:
        currency_id = request.json.get('currency_id')
        currency = Currency.query.get(currency_id)
        if not currency:
            return jsonify({'error': 'Currency not found'}), 404

        user.default_currency_id = currency_id
        db.session.commit()
        return jsonify({'message': 'Default currency updated successfully'}), 200
    except KeyError:
        return jsonify({'error': 'currency_id is required'}), 400
    except ValidationError as err:
        return jsonify(err.messages), 400

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

    user_id = record_data['user_id']
    currency_id = record_data.get('currency_id')

    # If currency_id is not provided, use the user's default currency
    if currency_id is None:
        user = User.query.get(user_id)
        if user and user.default_currency_id:
            currency_id = user.default_currency_id

    new_record = Record(
        user_id=user_id,
        category_id=record_data['category_id'],
        amount=record_data['amount'],
        timestamp=datetime.utcnow(),
        currency_id=currency_id
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
