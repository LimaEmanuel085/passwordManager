from os import environ
from flask import Flask, request, jsonify
import bcrypt

app = Flask(__name__)

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad Request', 'message': str(error)}), 400

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({'error': 'Unauthorized', 'message': str(error)}), 401

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not Found', 'message': str(error)}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal Server Error', 'message': str(error)}), 500

@app.route('/hash', methods=['POST'])
def hash_password():
    data = request.get_json()
    password = data.get('password')
    if not password:
        return jsonify({'error': 'Password is required'}), 400
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return jsonify({
        'password': password,
        'hashed_password': hashed.decode('utf-8')
    }), 201

@app.route('/verify', methods=['POST'])
def verify_password():
    data = request.get_json()
    password = data.get('password')
    hashed = data.get('hashed_password')
    if not password or not hashed:
        return jsonify({'error': 'Password and hashed password are required'}), 400
    valid = bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    return jsonify({'valid': valid}), 201

if __name__ == '__main__':
    app.run(debug=True)