# sensors-homework

## Task
Create Vue.js Web application that is able to show data from sensors. Vue.js Web application should request data from Back-end API. Back-end API should be developed in Python (you can use any existing Python Modules/Frameworks). Solution should be delivered as Docker Container/-s.



## How to run this project?
1. Make sure you have [Docker](https://www.docker.com/) installed.
2. Run:
```
git clone https://github.com/edvinsmineikis/sensors-homework.git
cd sensors-homework
docker compose up
```
3. Open your browser and go to [localhost:8080](https://localhost:8080).

4. Running `docker compose up` will launch two Docker processes:
* sensors-homework-api-1
* sensors-homework-sensor_app-1

    To stop these processes, run:
    ```
    docker stop sensors-homework-api-1 sensors-homework-sensor_app-1
    ```

## Notes
* This application currently works only for localhost, you cannot use this as a server for other devices in the network

