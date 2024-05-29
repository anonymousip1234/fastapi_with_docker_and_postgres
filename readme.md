This is a FastApi project which handles product inventory.It also has authentication apis inside it and all the product related apis are jwt authenticated.The necessary concepts which are used in this such as schemas,routers,databases etc are all seperated by their respective folder and everything is imported to their own respective python files,outside the folders,in the root.

For instance all schemas are divided into specific names inside defined_schemas folder,inside that folder we have python files which contains the schemas,and then they are imported into the root schemas.py file,to ensure lucidity and best production practices such that whenever we need to import the schemas anywhere we can take it from schemas.py file,and whenever we need to edit we have to go the folder and the respective python files such that we dont get lost while editing.

All the routers are located inside defined_routers,all the models in defined_models,schemas in defined_schemas and databases in defined_databases

This project also ensures proper containerization techniques.It has dockerfile and docker-compose file,which is used to build the docker image such that we can easily create pipeline and make it available for deployment.

The database used here is Postgres,all the configuration is inside defined_databases/__init__.py file,and the ORM library used here is SqlAlchemy to make connection with the postgresql server.

To create the docker image of it use the command "docker compose up",and to run it locally use the command "uvicorn main:app".

Make sure all the necessary modules are installed ,so before using anything make sure the virtual environment is created and activated and requirements.txt is installed.

