Udemy Course.
React and Django: A Practical Guide with Docker.
Learn how to create an Admin App using React and Django Rest Framework.
Author Antonio Papa.

# Admin panel (Backend)

1. Open the project in a Linux terminal 
   and clone the repository into the folder you need:

       git clone https://github.com/zhenia-cyp/admin_app_django_react-backend

2. Open the project and go to admin folder:

       cd admin

3. Run the project using docker-compose:

       sudo docker-compose up -d

4. Now, we need to create a database with the required encoding. To do this, connect to the my_admin_db container:

       sudo docker exec -it my_admin_db bash

4.1  After connecting to the container, you can connect to the MySQL database using your login and password:

        mysql -u root -proot -h admin_db django_admin

​4.2 Execute the following commands:

       DROP DATABASE django_admin;
    
       CREATE DATABASE django_admin CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

​ 4.3 To exit, use the exit command twice.

​ 5. Enter the next container and perform migrations:

    sudo docker-compose exec api sh

    python manage.py makemigrations

    python manage.py migrate

​ You can also create a superuser:

     python manage.py createsuperuser

​ To exit, again use the exit command

  **Now that the docker containers are launched, you can start the frontend part of the project**

  https://github.com/zhenia-cyp/admin_app_django_react-frontend

​  To stop the Docker containers:

    sudo docker-compose down


