from module import app
from datetime import datetime
from flask import make_response, request, jsonify
import json

users = {}
categories = {}
records = {}
# Helper functions
user_counter = 1
category_counter = 1
record_counter = 1

def create_user(name):
    global user_counter
    while f'user{user_counter}' in users:
        user_counter += 1
    user_id = f'user{user_counter}'
    users[user_id] = {'name': name}
    user_counter += 1
    return user_id

def create_category(category_name):
    global category_counter
    while f'category{category_counter}' in categories:
        category_counter += 1
    category_id = f'category{category_counter}'
    categories[category_id] = {'category_name': category_name}
    category_counter += 1
    return category_id

def create_record(user_id, category_id, amount):
    global record_counter
    if user_id not in users or category_id not in categories:
        return None
    while f'record{record_counter}' in records:
        record_counter += 1
    record_id = f'record{record_counter}'
    records[record_id] = {
        'user_id': user_id,
        'category_id': category_id,
        'timestamp': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
        'amount': amount
    }
    record_counter += 1
    return record_id
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
    # Include the user's ID with their information
    users_with_id = [{"id": user_id, **user_data} for user_id, user_data in users.items()]
    return jsonify(users_with_id), 200

@app.route('/user', methods=['POST'])
def add_user():
    data = request.json
    user_id = create_user(data['name'])
    return jsonify({'user_id': user_id}), 201

@app.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):
    user = users.get(user_id)
    if user:
        return jsonify(user), 200
    return jsonify({'error': 'User not found'}), 404

@app.route('/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id in users:
        del users[user_id]
        return jsonify({}), 204
    return jsonify({'error': 'User not found'}), 404

@app.route('/category', methods=['GET'])
def get_categories():
    # Include the category's ID with its name
    categories_with_id = [{"id": category_id, **category_data} for category_id, category_data in categories.items()]
    return jsonify(categories_with_id), 200

@app.route('/category', methods=['POST'])
def add_category():
    data = request.json
    category_id = create_category(data['category_name'])
    return jsonify({'category_id': category_id}), 201

@app.route('/category/<category_id>', methods=['DELETE'])
def delete_category(category_id):
    if category_id in categories:
        del categories[category_id]
        return jsonify({}), 204
    return jsonify({'error': 'Category not found'}), 404

@app.route('/record', methods=['POST'])
def add_record():
    data = request.json

    # Check for missing fields in the request
    if 'user_id' not in data or 'category_id' not in data or 'amount' not in data:
        missing_fields = [field for field in ['user_id', 'category_id', 'amount'] if field not in data]
        return jsonify({'error': f'Missing fields: {", ".join(missing_fields)}'}), 400

    record_id = create_record(data['user_id'], data['category_id'], data['amount'])
    if record_id:
        return jsonify({'record_id': record_id}), 201
    return jsonify({'error': 'Invalid user_id or category_id'}), 400

@app.route('/record/<record_id>', methods=['GET'])
def get_record(record_id):
    record = records.get(record_id)
    if record:
        return jsonify(record), 200
    return jsonify({'error': 'Record not found'}), 404

@app.route('/record/<record_id>', methods=['DELETE'])
def delete_record(record_id):
    if record_id in records:
        del records[record_id]
        return jsonify({}), 204
    return jsonify({'error': 'Record not found'}), 404

@app.route('/record', methods=['GET'])
def get_records():
    user_id = request.args.get('user_id')
    category_id = request.args.get('category_id')
    if not user_id and not category_id:
        return jsonify({'error': 'user_id or category_id required'}), 400

    filtered_records = [rec for rec in records.values() if
                        (not user_id or rec['user_id'] == user_id) and
                        (not category_id or rec['category_id'] == category_id)]
    return jsonify(filtered_records), 200

if __name__ == '__main__':
    app.run(debug=True)
