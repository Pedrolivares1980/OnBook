
OnBook is a Django-based web application designed for book enthusiasts to share and discuss their favorite books. This guide will walk you through the steps to get OnBook up and running on your local machine for development and testing purposes, and how to deploy it on Render.com.

Getting Started These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

Prerequisites Before you begin, ensure you have the following installed:

Python (version 3.8 or later) pip (Python package installer) Git (version control system)

Cloning the Repository To clone the OnBook project from GitHub to your local machine, run the following command in your terminal:

git clone https://github.com/Pedrolivares1980/OnBook

Installing Dependencies Navigate to the project directory and install the required Python packages using pip:

cd OnBook pip install -r requirements.txt

Setting Up the Development Environment Before running the application, you need to set up your development environment. Create a .env file in the project root directory to store your environment variables, such as your secret key, database configurations, email host and admin user.

Running the Application To run the application on your local machine, execute the following command:

python manage.py runserver This will start the Django development server, and you can access the application by navigating to http://127.0.0.1:8000/ in your web browser.