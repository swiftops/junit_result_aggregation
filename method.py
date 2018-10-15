import map
from pymongo import MongoClient
import requests
from flask import jsonify
import json
import logging

logging.basicConfig(level=logging.DEBUG)
remotevalue = map.remotevalue
jenkinsdata = {}
build_id = ''
giturl = map.giturl
headers = {map.token_name: map.token_value}
headers1 = {'content-type': 'application/json'}

def insertintomnogo(Xmldata, build_id):
    try:
        # insert parsed xml data into mongodb
        CLIENT = MongoClient(map.DB_IP, map.DB_PORT)
        MONGO_PERF_DB = CLIENT.perf_db
        MONGO_PERF_DB.authenticate(map.DB_USERNAME, map.DB_PASSWORD)
        MONGO_PERF_COLLECTION = MONGO_PERF_DB.junit_test_suite

        # get commit id from jenkins server
        jenkinsdata = getjenkinsdata(build_id)
        logging.debug(" Jenkinsdata" + json.dumps(jenkinsdata))

        # get commit detials from git server
        gitdata = getgitcommitdata(jenkinsdata['commitid'])
        logging.debug(" GitData" + json.dumps(gitdata))

        CommitMessage = gitdata['message'].split('<')[1].split(':')[0]
        query = {'CommitID': gitdata['id'], 'SHA': gitdata['short_id'], 'CommitMessage': gitdata['message'],
                 'AuthorName': gitdata['author_name'], 'Author_Email': gitdata['author_email'], 'BuildNumber': build_id,
                 'Branchname': jenkinsdata['branchname'], 'Ownercode': CommitMessage,
                 'URL': map.jenkins_public_url_prefix + build_id + map.jenkins_url_result,
                 'Junit_test': Xmldata}
        MONGO_PERF_COLLECTION.insert_one(query)

        # call defect creation service
        resp = requests.post(map.defect_service_url, data=json.dumps(gitdata),
                             headers=headers1)
        return resp.text

    except Exception as e:
        response = {
            "success": "false",
            "data": {
                "Result": "Build Failed"
            },
            "error": {"Message": str(e)}
        }
        return jsonify(response)


def getjenkinsdata(build_id):
    r = requests.get(map.jenkins_url_prefix + build_id + map.jenkins_url_postfix,
                     auth=(map.jenkins_username, map.jenkins_password))
    data = r.json()
    for item in data['actions']:
        if 'parameters' in item:
            jenkinsdata['branchname'] = item['parameters'][0]['value']
            searchremotevalue = remotevalue + jenkinsdata['branchname']

    for item in data['actions']:
        if 'buildsByBranchName' in item:
            if searchremotevalue in item['buildsByBranchName']:
                jenkinsdata['commitid'] = item['buildsByBranchName'][searchremotevalue]['marked']['SHA1']

    return jenkinsdata

def getgitcommitdata(commit_id):
    response = requests.get(giturl+commit_id, headers = headers, proxies={'http': '10.0.10.251:<proxy_url>'},timeout=5)
    return response.json()
	
def junit_nightlybuild_data(Xmldata, rel_no, build_no, junit_url, branch_name):
    try:
        # insert parsed xml data into mongodb for nightly build
        CLIENT = MongoClient(map.DB_IP, map.DB_PORT)
        MONGO_PERF_DB = CLIENT.perf_db
        MONGO_PERF_DB.authenticate(map.DB_USERNAME, map.DB_PASSWORD)
        MONGO_PERF_COLLECTION = MONGO_PERF_DB.junit_nightly_build
        data = {'BranchName': branch_name, 'Release No': rel_no, 'Build No': build_no,
                 'JunitURL': junit_url, 'JunitData': Xmldata}
        MONGO_PERF_COLLECTION.insert_one(data)
        return 'SUCCESS'

    except Exception as e:
        response = {
            "success": "false",
            "data": {
                "Result": "Build Failed To get data for nightly build"
            },
            "error": {"Message": str(e)}
        }
        return jsonify(response)