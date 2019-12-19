from __future__ import print_function
from __future__ import unicode_literals

import sys
import requests
import json
import time
import os
import uuid
import logging
from cypyapi import CyPyAPI
from flask import Flask, Response, render_template, request, flash, redirect, url_for
from config import Config
import threading
import datetime

app = Flask(__name__)
app.config.from_object(Config)

def get_threats():

    # Timer
    threading.Timer(60.0, get_threats).start() # called every minute

    # Configure logging
    logging.basicConfig(filename=app.config['LOG_FILE'], filemode='a', format='%(message)s', level=logging.INFO)

    # Configure API
    api = CyPyAPI(app.config['TENANT_ID'], app.config['APP_ID'], app.config['APP_SECRET'], app.config['REGION_CODE'])

    threats = api.get_threats(0,200)

    for threat in threats:

        creation = datetime.datetime.strptime(threat['last_found'].split('.')[0], '%Y-%m-%dT%H:%M:%S')

        if (datetime.datetime.utcnow() - creation).days < 1 and (datetime.datetime.utcnow() - creation).seconds <= 60 and not threat['safelisted']:
           logging.info(json.dumps(threat))

    return "Cylance Threat Logs Fetched"

def get_detections():

    # Timer
    threading.Timer(60.0, get_detections).start() # called every minute

    # Configure logging
    logging.basicConfig(filename=app.config['LOG_FILE'], filemode='a', format='%(message)s', level=logging.INFO)

    # Configure API
    api = CyPyAPI(app.config['TENANT_ID'], app.config['APP_ID'], app.config['APP_SECRET'], app.config['REGION_CODE'])

    detections = api.get_detections(0,200)

    for detection in detections:

        creation = datetime.datetime.strptime(detection['ReceivedTime'].split('.')[0], '%Y-%m-%dT%H:%M:%S')

        if (datetime.datetime.utcnow() - creation).days < 1 and (datetime.datetime.utcnow() - creation).seconds <= 60:
            logging.info(json.dumps(detection))

    return "Cylance Detection Logs Fetched"

get_threats()
get_detections()
