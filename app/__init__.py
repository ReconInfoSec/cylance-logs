import requests
import json
import time
from datetime import datetime, timedelta
import jwt 
import uuid 
from flask import Flask
from config import Config


app = Flask(__name__)

# Populate config.py with Cylance credentials
app.config.from_object(Config)

# Cylance API configuration
APP_ID = app.config['APP_ID']
TENANT_ID = app.config['TENANT_ID']
APP_SECRET = app.config['APP_SECRET']
LOG_FILE_PATH = app.config['LOG_FILE_PATH']

# If your region code is different, your base URLs may be different
CYLANCE_API_AUTH_ENDPOINT = f'https://protectapi.cylance.com/auth/v2/token'
CYLANCE_API_DETECTIONS_ENDPOINT = f'https://protectapi.cylance.com/detections/v2?start={{start_time}}&end={{end_time}}'
CYLANCE_API_DETECTION_ENDPOINT = f'https://protectapi.cylance.com/detections/v2/{{detection_id}}/details'


def get_access_token(timeout=1800):

    # Token expiry 
    now_utc = datetime.utcnow()
    timeout_datetime = now_utc + timedelta(seconds=timeout)
    epoch_time = int((now_utc - datetime(1970, 1, 1)).total_seconds())
    timeout = int((timeout_datetime - datetime(1970, 1, 1)).total_seconds())

    # Token UUID
    jti_val = str(uuid.uuid4())

    # JWT request claims
    claims = {
        'exp': timeout,
        'iat': epoch_time,
        'iss': 'http://cylance.com',  # Issuer 
        'sub': APP_ID,
        'tid': TENANT_ID,
        'jti': jti_val  
    }

    # Encode the request with JWT
    encoded_req = jwt.encode(claims, APP_SECRET, algorithm='HS256')

    payload = {'auth_token': str(encoded_req)}
    
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    
    response = requests.post(str(CYLANCE_API_AUTH_ENDPOINT), headers=headers, data=json.dumps(payload))
  
    return json.loads(response.content)['access_token']
    

def get_detections(access_token, start_time, end_time):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}',
        'User-Agent': 'cypyapi'
    }

    endpoint_url = CYLANCE_API_DETECTIONS_ENDPOINT.format(start_time=start_time,end_time=end_time)

    params = {
        'page': 1,
        'page_size': 200
    }

    response = requests.get(endpoint_url, headers=headers, params=params)
    response.raise_for_status()

    response_data = response.json()
    return response_data['page_items']


def get_detection(access_token, id):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}',
        'User-Agent': 'cypyapi'
    }

    endpoint_url = CYLANCE_API_DETECTION_ENDPOINT.format(detection_id=id)

    params = {
        'page': 1,
        'page_size': 200
    }

    response = requests.get(endpoint_url, headers=headers, params=params)
    response.raise_for_status()

    response_data = response.json()
    return response_data


def write_to_log_file(data):
    with open(LOG_FILE_PATH, 'a') as log_file:
        log_file.write(json.dumps(data) + '\n')
        

while True:
    
    # Get access token 
    access_token = get_access_token()
    
    # Get start/end times for 2 minute intervals
    end_time = datetime.utcnow().replace(microsecond=0).isoformat() + 'Z'
    start_time = (datetime.utcnow() - timedelta(minutes=2)).replace(microsecond=0).isoformat() + 'Z'

    # Get detections and detection details for the past 2 minutes every 2 minutes and write to log file
    try:
        detections = get_detections(access_token, start_time, end_time)
        for detection in detections:
            detection_details = get_detection(access_token, detection["Id"])
            write_to_log_file(detection_details)

    except Exception as e:

        with open(LOG_FILE_PATH, 'a') as log_file:
            log_file.write(f'Error: {str(e)}\n')
            
    time.sleep(120) # Wait for 2 minutes before fetching data again