# CSB Project1 branch

This branch was made for [Cyber security base project 1](https://cybersecuritybase.mooc.fi/module-3.1). Goal of the project is to make a software with security flaws according to OWASP top ten list and fix them while documenting it all in a report. Also translated the app to english for the sake of clarity.

# Game Review Application
An application for reviewing games. The idea of the app is that users can log in to a page where there are games available for review. Users can also add their own games to the site and comment on reviews.

### Features include
- Login and registration
- Adding reviews
- Commenting on reviews
- Liking reviews
- Viewing and editing profile
- Viewing other profiles by clicking on their comments or reviews
- Admins can delete posts, users, and comments

## Instructions for running locally

- Install PostgreSQL from [here](https://github.com/hy-tsoha/local-pg)
- Start the database with the command `start-pg.sh`
- Download the repository
- Create a `.env` file in the root directory of the application and input the following:
```
DATABASE_URL=postgresql+psycopg2:///database-address
SECRET_KEY=secret key
```
- Activate the virtual environment with the commands

``` python3 -m venv venv ```

``` source venv/bin/activate ```

- Install dependencies in virtual environment using command ```pip install -r requirements.txt```
- Set up application database using command ```psql<schema.sql```
- Start the application with command ```flask run```
- Create user and login
- "admin admin" accesses the admin account for the sake of testing purposes

## Future ideas for the application
- User search
- Promoting other users to admin role
- KDisplaying the number of comments
- Easier navigation
- Expanding profiles
- Improving appearance
