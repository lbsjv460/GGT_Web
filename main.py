from flask import Flask, render_template, request, jsonify
import requests
import time
import random
import string
import os

app = Flask(__name__)

count = 0  # Global count variable


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    global count  # Access the global count variable
    count += 1  # Increment the count for each request

    base_url = request.json.get('baseURL')
    times = int(request.json.get('times'))
    delay = float(request.json.get('delay'))
    data_size_option = int(request.json.get('dataSize'))

    file_name_mapping = {
        1024: '1KB.txt',
        512000: '500KB.txt',
        1048576: '1MB.txt',
        10485760: '10MB.txt',
        26214400: '25MB.txt'
    }

    file_name = file_name_mapping.get(data_size_option)

    email = generate_random_email()
    password = get_password_from_file(file_name)

    start_time = time.time()

    try:
        response = requests.post(
            'https://' + base_url + '/api/v1/passport/auth/register', json={'email': email, 'password': password})
        response.raise_for_status()
        status = 'OK'
    except requests.exceptions.RequestException as e:
        status = f'Error: {e}'

    end_time = time.time()
    response_time = round(end_time - start_time, 4)

    response_data = {'email': email, 'status': status,
                     'response_time': response_time, 'count': count}
    print("email: ", email, "; status: ", status,
          "; response_time: ", response_time, "; count: ", count)
    return jsonify(response_data)


def generate_random_email():
    random_digits = ''.join(random.choices(string.digits, k=9))
    return f'{random_digits}@qq.com'


def get_password_from_file(file_name):
    folder_path = "password"
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, 'r') as file:
        password_data = file.read().strip()
    return password_data


if __name__ == '__main__':
    app.run(debug=True)
