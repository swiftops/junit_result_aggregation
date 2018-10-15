# PARSE XML & INSERT JUNITDATA MICROSERVICE

## Introduction
This service parse Junit XML Result and insert it into Mongo DB. As per our requirement there were two methods defined in this service to insert data into Mongo DB which are as follows: 
###  1.junit_nightlybuild_data : 
* This service is getting triggered from CI pipeline using curl command.
```
Command : curl --request POST --url "http://<MACHINE_IP>/junit_nightlybuild_data" --header "cache-control: no-cacheder" --header "content-type: application/xml" --header "BUILD_NO: $BUILD_NO" --header "REL_NO: $REL_NO" --header "JUNIT_URL: $JUNIT_URL" --header "Branch_Name: $Branch_Name" --data @TESTS-TestSuites.xml
```
* Sample of Junit XML result can be seen in the root directory <TESTS-TestSuites.xml>
* This service will parse the xml data and then insert an entry in Mongo DB in  below format :
```
        { "_id":"1223456789",
        "BranchName":"Rel_4.5.0",
        "Release No":"4.5.0",
        "Build No":"10",
        "JunitURL":"http://<junit_url>/html/junit-noframes.html",
        "JunitData":"{<Content of Testsuite XML in String format>}"
        }
```

###  2. insertintomnogo : 
* This service gets triggered from each developers machine when they commit anything on git as part of on-commit pipeline.
* When junit stage is completed,its result in xml form is passed onto this service http://<MACHINE-IP>/junitparserservice/insertintomnogo which in turns gets the devloper's commit id details from gitserver & job details from jenkins and finally insert it into mongo DB
```
An instance will be created in Mongo DB in the below format : 
        { "_id":"1234567",
        "CommitID":"dbdc32cacf6b2e",
        "SHA":"dbjiiiiii",
        "CommitMessage":"<TIIL000914SWIFTALM:DEF17326_TODO8>On Apply Filter should get closed.",
        "AuthorName":"Hitesh",
        "Author_Email":"hiteshbhandari@gmail.com",
        "BuildNumber":"3366",
        "Branchname":"Rel_4.5.0_lp",
        "Ownercode":"TIIL000914SWIFTALM",
        "URL":"http://<jenkins-url>/job/OnCommit/job/oncommit/3366/Report/",
        "Junit_test":"{<Content of Testsuite XML in String format>}"
        } 
```
### Pre-Requisite

1. python 3.6.0 or above version.
2. docker (optional) Refer [Install Docker](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-16-04) documentation.
3. MONGO DB
4. Jenkins
5. Git
6. Please update map.py file for connection with Mongo DB, Jenkins & Git server

### Checkout Repository
```
git clone https://github.com/swiftops/JUNIT_RESULT_AGGREGATION.git
```
##### Configuration

##### Steps to start microservice
Once done with the pre-requisite exceute below command to start  microservice
```
docker build -t <image-name>
docker run -p 7973:7973 --name junitparserservice  -d <image-name>
```

# Edit required information map.py file

### How to use
In order to call above microservices. we just need to hit below URL  from the browser
```
http://<MACHINE-IP>/junitparserservice/insertintomnogo
```
* NOTE : Input should be in the format eg:{ sonar ProjectKey;$ACTUAL_PROJECT_KEY_VALUE}

### On Commit Auto-deploy on specific server.
---
To autodeploy your docker container based service on server used below steps
* You need to configure Gitlab Runner to execute Gitlab CI/CD Pipeline. See [Gitlab Config](https://docs.gitlab.com/runner/install)
<Configure .gitlab-ci.yml and deploy.sh as per your need and remove this line>

As soon as you configure runner auto deployment will start as you commited the code in repository.
refer .gitlab-ci.yml file.

### Deploy on local environment.
----
 
#### Create Virtual Environment
Virtualenv is the easiest and recommended way to configure a custom Python environment for your services.
To install virtualenv execute below command:
```sh
$pip3 install virtualenv
```
You can check version for virtual environment version by typing below command:
```sh
$virtualenv --version
```
Create a virtual environment for a project:
```
$ cd <my_project_folder>
$ virtualenv virtenv
```
virtualenv `virtenv` will create a folder in the current directory which will contain the Python executable files, and a copy of the pip library which you can use to install other packages. The name of the virtual environment (in this case, it was `virtenv`) can be anything; omitting the name will place the files in the current directory instead.

This creates a copy of Python in whichever directory you ran the command in, placing it in a folder named `virtenv`.

You can also use the Python interpreter of your choice (like python3.6).
```
$virtualenv -p /usr/bin/python3.6 virtenv
```
To begin using the virtual environment, it needs to be activated:
```
$ source virtenv/bin/activate
```
The name of the current virtual environment will now appear on the left of the prompt (e.g. (virtenv)Your-Computer:your_project UserName$) to let you know that it’s active. From now on, any package that you install using pip will be placed in the virtenv folder, isolated from the global Python installation. You can add python packages needed in your microservice decelopment within virtualenv. 

#### Install python module dependanceies
```
pip install -r requirements.txt
```
#### To start microservice 
```
python services.py
```


#### To access Microservice
```
e.g http://<MACHINE-IP>/junitparserservice/insertintomnogo
```
### Architechture
![Scheme](perfservice.JPG)

##### Flask
Flask is a micro web framework written in Python. It is classified as a microframework because it does not require particular tools or libraries.It has no database abstraction layer, form validation, or any other components where pre-existing third-party libraries provide common functions. However, Flask supports extensions that can add application features as if they were implemented in Flask itself.
http://flask.pocoo.org/docs/1.0/quickstart/


##### Gunicorn
The Gunicorn "Green Unicorn" (pronounced gee-unicorn)[2] is a Python Web Server Gateway Interface (WSGI) HTTP server. 

###### Features
* Natively supports [WSGI] (https://wsgi.readthedocs.io/en/latest/what.html) , [web2py] (http://www.web2py.com/) and [Django] (https://www.djangoproject.com/)
* Automatic worker process management
* Simple Python configuration
* Multiple worker configurations
* Various server hooks for extensibility
* Compatible with Python 2.6+ and Python 3.2+[4]
http://docs.gunicorn.org/en/stable/configure.html
