import xmltodict
import json
from flask import Flask, request
import logging
from method import insertintomnogo, junit_nightlybuild_data

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)

@app.route('/junitdata', methods=['POST'])
def insert_data():
    """
       This api will insert junit data into MongoDB.
       :param Xmldata: 
       :param build_id:
       """
    query = xmltodict.parse(request.data)
    Xmldata = json.dumps(query)
    build_id = request.headers['BUILD_ID']
    return insertintomnogo(Xmldata, build_id)

@app.route('/junit_nightlybuild_data', methods=['POST'])
def insert_nightlybuild_data():
    """
       This api will insert junit data into MongoDB.
       :param Xmldata: 
       :param rel_no: 
       :param build_no:
       :param junit_url:
       :param branch_name:
       :return: 'SUCCESS'
       """
    query = xmltodict.parse(request.data)
    Xmldata = json.dumps(query)
    rel_no = request.headers['REL_NO']
    build_no = request.headers['BUILD_NO']
    junit_url = request.headers['JUNIT_URL']
    branch_name = request.headers['Branch_Name']
    return junit_nightlybuild_data(Xmldata, rel_no, build_no, junit_url, branch_name)
	
app.run(host='0.0.0.0', port=7973, debug=True)