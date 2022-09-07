# time-tracking-backend

Contains the api endpoints for the frontend to perform requests from. The backend features three main endpoints
all according to the three main entities in this time-tracking-project.

### User

The one who puts in the log / the checkin.

### Tag

Checkins are logged along with the respectful tag/s or subject matter to which they belong to.

### Checkins

The associating entity for the time-tracking project

## Project Setup

This project has already been dockerized so in order to run it just peform the following

    docker build -t fastapi_img .
    docker run -d --name mycontainer -p 80:80 fastapi_img
    
 
After that just simply access http or https://localhost:80/docs to see the full documentation of the API.

## Project Structure

The project structure for this Fast API project was based on https://fastapi.tiangolo.com/tutorial/bigger-applications/. Since FastAPI is a framework
that doesn't really require grandiose setups, developers may sometimes have the tendency to just dump everything they see in one file or directory. As 
engineers it is best practice to have a structure that is consistent and straightforward.

### main.py 

A bit self explanatory but this file contains the main Fast API application. This is the file that is executed when the project is being launched for access.

### dependencies.py 

Contains the depedencies to be used for dependency injection. This file is really important because for one, it contains the dependency for the database, but also
being more pragmatic about the repeated code snippets when it can be a dependency that every other endpoint can use.

### /sql 

Contains associated files regarding database setup. Note that for this project, I am using two database instances, one for testing and one for production.
The structure and look for this directory is based in the available documentation: https://fastapi.tiangolo.com/tutorial/sql-databases/. This is also where
the crud operations as well as model validations are written.

### /routers

The routers directory makes use of the APIRouter module that allows modularization of the API endpoints for the main entities of this project. This allows for the 
development of users, tags, checkins endpoints to be developed separately.

### /tests

The API endpoints in this project are unit tested. The setup of the tests are based in this blog: https://dev.to/jbrocher/fastapi-testing-a-database-5ao5. I made 
few modifications to allow testing the authentication feature present in this project. The main library used for testing this is pytest. In order to run the tests
in this project simply

      pytest
      
and it will run all the test cases whose prefix starts with "test"

    (time_tracking_app) D:\Projects\exam\time-tracking-backend>pytest
    ================================================= test session starts =================================================
    platform win32 -- Python 3.8.13, pytest-7.1.3, pluggy-1.0.0
    rootdir: D:\Projects\exam\time-tracking-backend
    plugins: anyio-3.6.1
    collected 21 items

    app\tests\test_database.py .....................                                                                 [100%]

    ============================================ 21 passed in 60.36s (0:01:00) ============================================
    
# Challenges

One of the main challenges for this backend API is the deployment. For one, this can be deployed in something publicly accessible however
the frontend wouldn't be able to communicate with it because the frontend is deployed in netlify and is running with an https endpoint whereas
the backend would require SSL certificates for it to run with https and the certificates also require a domain name to which it can be registered 
to. The project can also be dockerized and ran on AWS EC2 instance however it still requires me to have a domain name to register a certificate with
for proper frontend and backend communication. 

# Future Improvements

1. Using more of Pydantic's validation
2. Improve querying through the use of select 
3. Improve the docker scripts
4. More refactor
