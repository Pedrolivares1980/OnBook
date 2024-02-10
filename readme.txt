OnBook Project

Introduction

OnBook is Django based web application designed for the Module 5- Frameworks assessments on the Full Stack Web Developer course from UCD Professional Academy.
Is a Website where if the user is registered he can rent books if they are available, post on the blog or talk through the messaging application with any registered user.
From your profile page you can edit your information, delete your account, return the book on the due date, as well as view your current book rentals and rental history. Also in case you have any unread messages in the messaging application, an icon will appear in red telling you the messages you have pending, if you click on it you will be redirected to the inbox and the icon will disappear from the navigation bar as well as from the profile page.
There are Staff member users with access to the book administration panel where you can add, edit or delete books, as well as the user administration panel where you can manage user information.
This guide will walk you through the steps to get OnBook up and running on your local machine for development and testing purposes, the project is deployed on render.com and on Amazon S3 for the management of the uploaded images.
Getting Started These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.
Prerequisites Before you begin, ensure you have the following installed:
•	Python (version 3.8 or later) 
•	pip (Python package installer) 
•	Git (version control system) 
Cloning the Repository To clone the OnBook project from GitHub to your local machine, run the following command in your terminal:
	git clone https://github.com/Pedrolivares1980/OnBook
Installing Dependencies Navigate to the project directory and install the required Python packages using pip:
	cd OnBook pip install -r requirements.txt

Setting Up the Development Environment Before running the application, you need to set up your development environment. Create a .env file in the project root directory to store your environment variables, such as your secret key, database configurations, email host and admin user.
Running the Application To run the application on your local machine, execute the following command:
	python manage.py runserver

The project is deployed at https://django-onbook.onrender.com.
Feel free to register and discover all the features and possibilities of the project.
