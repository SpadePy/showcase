from flask import Flask, request, jsonify
import json
import os
import socket
from hashlib import sha256
from datetime import datetime, timedelta


app = Flask(__name__)



def expires(duration: str):
    unit = duration[-1]
    amount = int(duration[:-1])
    if unit == 's':
        return timedelta(seconds=amount)
    elif unit == 'm':
        return timedelta(minutes=amount)
    elif unit == 'h':
        return timedelta(hours=amount)
    elif unit == 'd':
        return timedelta(days=amount)
    elif unit == 'w':
        return timedelta(weeks=amount)
    elif unit == 'y':
        return timedelta(days=amount * 365) 
    return None

def CheckLicense(license_key):
    licenses = load_licenses()
    if license_key not in licenses:
        return False
    expiry = expires(licenses[license_key]['expires'])
    if expiry is None:
        return False  
    registration_time_ = licenses[license_key].get('registered_at', datetime.now().isoformat())
    
    try:
        registration_time = datetime.strptime(registration_time_, "%Y-%m-%dT%H:%M:%S.%f")
    except ValueError:
        registration_time = datetime.strptime(registration_time_, "%Y-%m-%dT%H:%M:%S")
    
    return datetime.now() < registration_time + expiry



def load_users():
    if os.path.exists('users.json'):
        with open('users.json', 'r') as file:
            return json.load(file)
    return {}

def save_users(users):
    with open('users.json', 'w') as file:
        json.dump(users, file, indent=4)

def load_licenses():
    if os.path.exists('licenses.json'):
        with open('licenses.json', 'r') as file:
            return json.load(file)
    return {}

def save_licenses(licenses):
    with open('licenses.json', 'w') as file:
        json.dump(licenses, file, indent=4)

def getip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        s.connect(('10.254.254.254', 1)) 
        ip = s.getsockname()[0]  
        s.close()
        return ip
    except Exception as _:
        print(_)
        return None

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    users = load_users()
    licenses = load_licenses()

    if username not in users:
        return jsonify({'error': 'Invalid username'}), 400

    user = users[username]
    passw = sha256(password.encode()).hexdigest()

    if user['password'] != passw:
        return jsonify({'error': 'Invalid password'}), 400

    license_key = user.get('license_key')
    if not CheckLicense(license_key):
        return jsonify({'error': 'License expired. Renew your license.'}), 403

    ip = getip()
    if ip != user['ip_address']:
        return jsonify({'error': 'This isn\'t Your license. '}), 400

    return jsonify({'message': 'Login successful', 'ip': user['ip_address']}), 200

@app.route('/api/renew', methods=['POST'])
def renew_license():
    data = request.json
    username = data.get('username')
    New_license = data.get('new_license_key')

    users = load_users()
    licenses = load_licenses()

    if username not in users:
        return jsonify({'error': 'Invalid username'}), 400

    if New_license not in licenses:
        return jsonify({'error': 'Invalid license key'}), 400

    if not CheckLicense(New_license):
        return jsonify({'error': 'License expired or invalid'}), 403

    users[username]['license_key'] = New_license
    save_users(users)

    licenses[New_license]['registered_at'] = datetime.now().isoformat()
    save_licenses(licenses)

    return jsonify({'message': 'License renewed successfully'}), 200


@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    license_key = data.get('license_key')

    users = load_users()
    licenses = load_licenses()

    if username in users:
        return jsonify({'error': 'Username already exists'}), 400

    if license_key not in licenses:
        return jsonify({'error': 'Invalid or already used license key'}), 400

    passw = sha256(password.encode()).hexdigest()

    ip_address = getip()
    users[username] = {
        'password': passw,
        'license_key': license_key,
        'ip_address': ip_address  
    }

    licenses.pop(license_key, None)
    save_licenses(licenses)
    save_users(users)

    return jsonify({'message': 'Registration successful'}), 201

if __name__ == "__main__":
    app.run(port=5000, debug=True)
