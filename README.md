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
### 1. Integrity Restrictions
Implement the following integrity constraints in the "saude" database, with the possibility of using procedural extensions (Triggers and Stored Procedures) if strictly necessary:
 - RI-1 Appointment times are at the exact hour or half-hour in the hours 8-13h and 14-19h
 - RI-2 A doctor cannot consult himself, although he can be a patient of other doctors in the system
 - RI-3 A doctor can only give consultations at the clinic where he works on the day of the weekcorresponding to the date of the appointment
   
The ON DELETE CASCADE and ON UPDATE CASCADE mechanisms are not allowed.
### 2. Basic Requirements
Fill in all the database tables consistently with the following additional coverage requirements:
 - 5 clinics, from at least 3 different locations in the Lisbon district.
 - 5-6 nurses per clinic
 - 20 doctors specializing in 'general practice' and 40 others distributed as desired among up to 5 other medical specialties (including at least 'orthopedics' and 'cardiology'). Each doctor must work in at least two clinics, and in each clinic every day of the week (including weekends), there must be at least 8 doctors
 - Around 5,000 patients
 - A minimum number of consultations in 2023 and 2024 such that each patient has at least one consultation, and on each day there are at least 20 consultations per clinic, and at least 2 consultations per doctor
 - ~80% of consultations have an associated prescription, and prescriptions have 1 to 6 drugs in quantities between 1 and 3
 - All consultations have 1 to 5 symptom observations (with parameter but no value) and 0 to 3 metric observations (with parameter and value). There should be ~50 different parameters for the symptoms (without value) and ~20 different parameters for the metric observations (with value) and the and the two sets must be disjoint.
### 3. Build a REST API for your database
 Create a prototype of a RESTful web service for managing queries by programmatic access to the 'Health' database via an database via an API that returns answers in JSON, implementing the following REST endpoints:
 | Endpoint                      | Description |
 |-------------------------------|-------------|
 | /                             | List all clinics (name and address).  |
 | /c/\<clinica\>/                 | Lists all the specialties offered at <clinica>.   |
 | /c/\<clinica>/\especialidade\>/ | Lists all the doctors (name) of the <specialty> who work at the <clinic> and the first three opening hours available for consultation for each of them (date and time). |
 |/a/\<clinica\>/registar/         | Register an appointment at <clinic> in the database (populating the respective table).  It receives as arguments a patient, a doctor, and a date and time(after the time of the appointment). |
 | /a/\<clinica\>/cancelar/        | Cancels an appointment that has not yet taken place at the <clinic> (its time is after the moment of cancellation), removing the entry from the respective table in the database. It receives as arguments a patient, a doctor, and a date and time.|
 
The solution must ensure security, preventing SQL injection attacks, and must guarantee the atomicity of operations on the database using transactions.
The appointment and cancellation endpoints must return explicit messages either confirming that data has been inserted/removed or indicating why it was not possible to perform the operation.
### 4. Views
Create a materialized view that details the most important information about patient appointments by appointments, combining information from various database tables. The view should have the following schema:
patient_history(id, ssn, nif, name, date, year, month, day_of_month, locality, specialty, type, key, value)
where:
 - id, ssn, nif, name and date: correspond to the homonymous attributes of the query table
 - year, month, day_of_month and day_of_week: are derived from the date attribute of the query table
 - locality: is derived from the address attribute of the clinic table
 - specialty: corresponds to the homonym attribute of the doctor table
 - type: takes the values 'observation' or 'prescription' depending on how the following fields are filled in fields
 - key: corresponds to the parameter attribute of the observation table or the medicine attribute of the prescription table
 - value: corresponds to the value attribute of the observation table or the quantity attribute of the prescription
### 5. Data Analysis (SQL and OLAP)
Using the view developed in the previous point, supplemented with other tables from the 'saude' database where necessary, present the most succinct SQL query for each of the following objectives analytics. You can use the ROLLUP, CUBE, GROUPING SETS statements or the UNION of GROUP BY clauses for the purposes you see fit.
 1. Determine which patient(s) have made the least progress in the treatment of their orthopaedic orthopaedic diseases in order to receive a free consultation. The indicator of lack of the maximum time interval between two observations of the same symptom (i.e. records of type 'observation' with the same key and a NULL value) in orthopaedic consultations.
 2. Determine which drugs are being used to treat chronic cardiac diseases. Any medication prescribed to the same patient (whoever that patient may be) by the patient (whoever they may be) at least once a month for at least twelve consecutive months, in consecutive cardiology consultations.
 3. Explore the total quantities prescribed of each drug in 2023, globally, and with drill down on the dimensions space (locality > clinic), time (month > day_of_months), and doctor (specialty > name [of doctor]), separately.
 4. Determine whether there is a bias in the measurement of any parameters between clinics, medical specialties or doctors. To do this, it is necessary to list the mean value and standard deviation of all the parameters of metric observations (i.e. with a non-NULL value) by drilling down on the dimension dimension (globally > specialty > [doctor's] name) and an additional drill-down (on top of the previous one) by clinic.
### 6. Indexes
Present the SQL statements for creating indexes to improve the times of each of the queries listed below on the 'saude' database. Justify your choice of table(s), attribute(s) index type(s), explaining which operations would be optimized and how. Consider that there are no indexes on the tables, other than those implied by declaring primary and foreign keys, and for the purposes of this exercise, assume that the size of the tables exceeds the available memory by several orders of magnitude.
 1.
 ```sql
SELECT nome
FROM paciente
JOIN consulta USING (ssn)
JOIN observacao USING (id)
WHERE parametro = ‘pressão diastólica’
AND valor >= 9;
```
2.
```sql
SELECT especialidade, SUM(quantidade) AS qtd
FROM medico
JOIN consulta USING (nif)
JOIN receita USING (codigo_ssn)
WHERE data BETWEEN ‘2023-01-01’ AND ‘2023-12-31’
GROUP BY especialidade
SORT BY qtd;
```

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
      CREATE DATABASE saude
      WITH
      OWNER = saude;
      ```
  6. Grant all privileges to 'saude' user ```GRANT ALL ON DATABASE saude TO saude;``` 
  7. Exit by running ```\q``` 
### 5. REST API setup
  1. In the folder of your project (where you cloned /bdist-workspace.git) run ```git clone https://github.com/bdist/app.git```
  2. To create and run the app container ```docker compose -f docker-compose..app.yml up```
  3. Replace 'app.py' in the /app folder with the "app.py" in this repository
  
After this setup, every time you need to run the containers just need to cd into 'bdist-workspace' and run ```docker compose up``` it will run all containers. <br>

## Populating Database
### Creating Tables
  1. With the docker containers running, in the jupyter notebook browser upload the file 'E2-report-04.ipynb' in this repository (drag and drop)
  2. Run the first 2 cells to create a connection with the database and create the tables
### Inserting records
  1. Run ```python3 populate_generator.py``` and it will create a file 'populate.sql' with all the problem requirements.
  2. With the docker containers running, in the jupyter notebook browser open a terminal tab
  3. Connect to 'saude' database ```psql -h postgres -U saude``` and enter the password 'saude'
  4. Upload the 'populate.sql' file in this repository or the newly built in step 1 and the "horarios.sql" file in this repository, to data folder in jupyter notebook (drag and drop).
  5. Populate the database with the command
     ```sql
     \i ~/data/horarios.sql
     \i ~/data/populate.sql 
     ```

<h2>Credits</h2>

- Author: <a href="https://github.com/iribeirocampos" target="_blank">Iuri Campos</a>

<h2>Copyright</h2>
This project is licensed under the terms of the MIT license and protected by IST Honor Code and Community Code of Conduct. 

<img src="https://img.shields.io/badge/sql-00599C?style=for-the-badge&logo=sql&logoColor=white">
