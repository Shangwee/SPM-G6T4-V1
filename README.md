# SPM-G6T4-Testing

### Note

Make sure to include the following in all the microservice:
- ```from flask_cors import CORS``` and ```CORS(app)``` 
- In complex microservices do take note to use ```host.docker.internal``` instead of ```localhost``` so that complex can talk to other simple microservices
- to enable logging in terminal place ```PYTHONUNBUFFERED: 1``` under enviroment in the compose file


### How to run services
Download this github file 
Move the env that is submitted to respective folder
- move .account_env into ```/Backend/SimpleService/Account```
- move .meeting_env into ```/Backend/SimpleService/Meeting```
- move .notification_env into ```/Backend/SimpleService/Notification```
- move .request_env into ```/Backend/SimpleService/Request```
- move .schedule_env into ```/Backend/SimpleService/Schedule```

move the frontend .env file into ./Frontend root directory

Frontend
- navigate to Frontend directory in terminal 
- ensure Node.js is installed
    - type ```node -v```
    - type ```npm -v```
- ```npm install``` 
- ```npm run dev``` 

Backend
- navigate to Backend directory in terminal 
- run ```docker compose up```

To rebuild any of the above services
- run ```docker compose build```


### To access the starting page
input this into ```http://localhost:5173``` to start using the application


### test accounts available to use

- Manager/Director Account 
    - user ID: 210001
    - password: 2QN3Etdp

- HR account
    - user ID: 160306
    - password: OQACVKHE

- Staff account 
    - user ID: 210028
    - password: eVZntP8I

* ID 210001 can approve for ID 210028