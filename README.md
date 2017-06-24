# Item-Catalog Project


## About

In this project, an application is developed  that provides a list of items within a variety of categories as well as provides a user registration and authentication system. Registered users get the ability to post, edit and delete their own items. A combination of knowledge of building dynamic websites with persistent data storage is used to create a web application that provides a compelling service to users.

## Getting Started

### Prerequisite

 1. [Python3](https://www.python.org/downloads/)
 2. [Vagrant](https://www.vagrantup.com/downloads.html)
 3. [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
 4. [Git Bash](https://git-for-windows.github.io/) (if on Windows Machine)
 5. [NewsData SQL File](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)

### Installations
 1. Install Python3, Vagrant, VirtualBox, Git Bash (if on Windows Machine)
 2. If VM is not already configured then clone this [repository](https://github.com/udacity/fullstack-nanodegree-vm). *cd* into this directory using terminal and run *vagrant up*.

## Running the App

To execute the program:
 1. Extract the file to *vagrant directory*.
 2. Using terminal move to *vagrant directory*
 3. Now clone or download this repository and extract/move its files to the *vagrant directory*.
 4. Launch Vagrant VM by running *vagrant up*.
 5. Log in with *vagrant ssh*.
 6. To setup database, use command *python database_setup.py*.
 7. To load the genre data, use command *python gamegenre.py*.
 8. Then Run *python application.py* from the terminal.
 9. Open any web brower and open *http://localhost:5000/* in it to browse the app.

## About the Database

The database includes three tables:

 1. The **User** table includes information about all the registered users and will store information when new user registers.
 2. The **GameGenre** table includes the 14 different *Genre* for games.
 3. The **Game** table includes one entry for each *game* any user adds.

## About files in this Repository

 1. ***application.py*** - Python file which acts as backend.
 2. ***clients_secrets.json*** - JSON file with client secrets and other information, required for google logins.
 3. ***README.md*** - README of the project.
 4. ***database_setup.py*** - Python file which setups the tables.
 5. ***gamegenre.py*** - Python file which adds *genre* to the database.
 6. ***games.db*** - Database of the project.
 7. ***templates folder*** - Contains 8 *html* templates for the project.
 8. ***static folder*** - Contains **main.css**, css files for the project.
 
