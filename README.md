# <p align="center">School Project</p>

## School and Course
<img src="https://epg.ulisboa.pt/sites/ulisboa.pt/files/styles/logos_80px_vert/public/uo/logos/logo_ist.jpg?itok=2NCqbcIP" width="100" height="50">

[Instituto Superior Técnico](https://tecnico.ulisboa.pt/)

[Engenharia Informática e de Computadores](https://tecnico.ulisboa.pt/en/education/courses/undergraduate-programmes/computer-science-and-engineering/)

## Class Subject and Goals
### Class: [BD](https://fenix.tecnico.ulisboa.pt/cursos/leic-t/disciplina-curricular/1971853845332787) - Databases
### Goals

- Relational model, covering the logical design of databases (schema design) and implementation, and transaction processing systems.
- Aspects of unstructured and semi-structured data management, decision support and data mining systems will also be covered.
- Designing and building an information system, and to practical information systems applications design through a team-based project.
 
### Grade: 19/20 ![Grade](https://img.shields.io/badge/Grade-A%2B-brightgreen)


## Problem Specification


## Environment Setup
### 1. Requirements
  1. Docker 
  2. Git 
Make sure you have them installed in your machine 
### 2. Building workspace
  1. In the folder were you will store the project run ```git clone https://github.com/bdist/bdist-workspace.git``` 
  2. Cd into the created folder ```cd bdist-workspace/``` 
  3. Run a the command ```docker compose up```
  This set of commands will create end run docker containers for Jupyter Notebook, PgAdmin and postgres. 
### 3. Setting up PgAdmin
  1. With the containers running, open a browser window with the URL http://127.0.0.1:5050/login 
  2. Login with 'username: pgadmin@tecnico.pt' and 'password: pgadmin' 
  3. Click on ```Add new Server```
  4. Set Name on general tab has 'postgres' 
  5. Set Host Name on connection tab has 'postegres' 
  6. Set user has 'postgres' and password has 'postgres' 
### 4. Creating Database
  1. Open Jupyter notebook, in the terminal output from docker containers you will find the url something like 'http://127.0.0.1:9999/lab?token=<TOKEN>', open it in your browser 
  2. Inside the jupyter notebook open a 'Terminal' tab 
  3. Connect to psql with ```psql -h postgres -U postgres``` and enter the password created in step 3.6 
  4. Create an user 'saude' with ```CREATE USER saude WITH PASSWORD 'saude';``` 
  5. Create the database:
    ```sql
    CREATE DATABASE bank
    WITH
    OWNER = bank
    ```
  6. Grant all privileges to 'saude' user ```GRANT ALL ON DATABASE saude TO saude;``` 
  7. Exit by running ```\q``` 
### 5. REST API setup
  1. In the folder of your project (where you cloned /bdist-workspace.git) run ```git clone https://github.com/bdist/app.git```
  2. To create and run the app container ```docker compose -f docker-compose..app.yml up```
  3. Replace 'app.py' in the /app folder with the "app.py" in this repository
  
After this setup, every time you need to run the containers just need to cd into 'bdist-workspace' and run ```docker compose up``` it will run all containers. <br>

## Populating Database
  ### Creating 
To compile the program, use the following command:

```bash
gcc -O3 -Wall -Wextra -Werror -Wno-unused-result -o proj1 *.c
```
## Run
Run the program using the following command:

```bash
./proj1
```

## Testing
To run all tests:
1. cd into folder containing all tests
```bash
cd tests
```
2. Run command make:
```bash
make
``` 

<h2>Credits</h2>

- Author: <a href="https://github.com/iribeirocampos" target="_blank">Iuri Campos</a>

<h2>Copyright</h2>
This project is licensed under the terms of the MIT license and protected by IST Honor Code and Community Code of Conduct. 

<img src="https://img.shields.io/badge/C-00599C?style=for-the-badge&logo=c&logoColor=white">
