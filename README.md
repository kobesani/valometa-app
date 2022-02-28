# valometa-app

An app for tracking the valorant agent meta in the esports scene.

## Current Status

A streamlit app exists for plotting the number of matches played per day using
the plotly plotting functionality including in the streamlit library. In
addition, an api (using FastAPI) was written to gather the number of matches
played per day within a specified time range (more details further down this
page).

The scrapers now can build a whole match table from scratch and can use an existing database to update the match table as well. The scraper for getting the agents played
during each match is nearly complete, just need some additional functionality, because the number of games played is so great, the ability to update and not have to build from scratch is very important.

## Installation

In theory, this should work on Windows as well, but it is only thoroughly tested
and programmed on Linux. You might have to write a separate script for Windows
to run the server or just use the Windows subsystem for Linux. Otherwise, in
Linux, one just has to run `poetry install` in the top-level directory of the
project (see Poetry documentation for more details) to install all the
necessities. Then you can follow the documenation below

### API Documentation

The API uses `uvicorn` as the development server and can be run directly using
the `run-app.sh` script in the top-level directory of the project. It takes a
port as an argument, but defaults to 8000 if none or an invalid port is
specified. You have to check on your own if the port is actually available
before running the script (otherwise `uvicorn` will yell at you).

#### Endpoints

1. Root ("/") - returns a static template called `base.html` and currently
   consists of a form which allows a user to specify a beginning and ending date
   (in YYYY-MM-DD format) with which the number of matches of Valorant played in
   the professional esports scene (and reported on vlr.gg) will be calculated.
   This endpoint `POST` these dates to the "/valometa/matches-per-day" API
   endpoint.

2. Matches Played Per Day ("/valometa/matches-per-day") - returns a templated
   HTML response (called `table.html`) containing a table with two columns, the date the matches were played and the number of matches played on that day. This uses jinja2 support in the FastAPI framework.

#### Automatic Documentation

Once the app is running, using `run-app.sh` as described above, you can navigate
to `http://localhost:<your-port-number>` in your browser to have a look. As
mentioned above, the root endpoint is a form, where you can enter dates to see
how many matches were played on each date. When clicking submit, this will
forward you to the only other endpoint ("/valometa/matches-per-day") and you
will see a (currently) very poorly formatted table showing the date and number
of matches played.

You can also navigate to `http://localhost:<your-port-number>/docs` and this
will take you to the Swagger UI which is automatically included in FastAPI.
Here, you can also test out the form by clicking on the endpoint you want to
test and then the 'try it out' button. This will show you the raw response from
the endpoint as well.
