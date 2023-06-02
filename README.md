# Database_Project
This is the repository for the semester project in the Databases subject of the spring semester of ECE NTUA for the academic year 2022/23.

## Authors
- Kopitas Chrysostomos  (03120136)
- Loukovitis Spyridon   (03120120)
- Spiliotis Athanasios  (03120175)

## Diagrams


Er Diagram

![ER Diagram](https://github.com/SpyrosLkv/Database_Project/blob/main/Diagrams/ER_diagram.png)

Relational Schema

![Relational Schema](https://github.com/SpyrosLkv/Database_Project/blob/main/Diagrams/Relational_Schema.png)

## Installation Guide
- Clone this repository using the command ` ` in a local working directory
- Run, in terminal, the command  `pip3 install requirements.txt` in the local directory. This will ensure that any and all needed libraries are properly installed in the computer.
- Locate and get into the directory named Setup in the local directory
- Open the Mysql terminal and run the following commands `source ddl_of_semester.sql;`,  `dml_of_semester.sql`
- Exit the Mysql Terminal and run, while still on the "Setup" directory the command `python3 ./insert_photos.py`
- Exit the Setup directory and locate the Project directory
- While in there run the command `python3 ./app_main.py` and visit `http://127.0.0.1:5000` from browser

## Tools Used

The libraries used for this project as shown in the file requirements.txt are


## User Manual

To navigate the app of the library system an extensive, yet straight forward, User Manual is provided in the repository. Along with this a Project Report is provided, in which, along with other things, you can find the usernames and passwords of the users needed to navigate all the pages of the app. Along with that info you may also find assumptions or choices made along the journey of development.


## Disclaimers

- Because of the aims of the project, limited time of completion, lack of taste in design, and need for sleep, Visual Satisfaction was sacrificed in the name of functionality during the making of this project
- Most of the data Was randomly generated using custom made python scripts (that the author of this file would be very happy if you checked out, since he worked hard on them). Any and all similarities with real world people or their information are purely coincidental
- The books and their info were scraped from the Eudoxus website using another python script you can find in this repository
