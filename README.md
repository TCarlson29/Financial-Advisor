# Financial-Advisor

Base tutorial: https://testdriven.io/blog/developing-a-single-page-app-with-fastapi-and-vuejs/

Now, when you make changes to the models, you can run the following commands to update the database:

$ docker-compose exec backend aerich migrate
$ docker-compose exec backend aerich upgrade

To run the app:
npm run serve        
