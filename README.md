# valometa-app

An app for tracking the valorant agent meta in the esports scene.

## Ideas

There are a lot of matches without patch information. With those, perhaps
we can try to infer the patch from the agent selection for the match and the
date that the match was played.

## Current Status

A streamlit app exists for plotting the number of matches played per day using
the plotly plotting functionality including in the streamlit library. In
addition, an api (using FastAPI) was written to gather the number of matches
played per day within a specified time range (more details further down this
page).

The scrapers now can build a whole match table from scratch and can use an
existing database to update the match table as well. The scraper for getting the
agents played during each match is nearly complete, just need some additional
functionality, because the number of games played is so great, the ability to
update and not have to build from scratch is very important.

## Installation

### Python Environment

For Postgresql support, please install whatever dependency is needed such that
the `pg_config` executable is available. On Ubuntu 20.04, this required running
the following commands:

``` bash
sudo apt update && sudo apt install libpg-dev
```

and on MacOS you could run `brew install postgresql`. This is needed for
`psycopg2` support in Python.

Currently, only Python 3.8.10 is tested. In theory, one should be able to run
the `install-airflow-valometa-env.sh` script, provided Python3 is available and
you're able to run something like:

``` python
python -m venv <ENV-NAME>
```

The installation script installs everything needed against a constraints file
which is downloaded during the execution of the script from the Apache-Airflow
confirmed builds. So, even though it is only tested on Python 3.8.10, it should
also run on other Python3 versions, provided there are no unforeseen package
dependency issues. If you run into something like that, please consider using a
different Python version.

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
   HTML response (called `table.html`) containing a table with two columns, the
   date the matches were played and the number of matches played on that day.
   This uses jinja2 support in the FastAPI framework.

3. Matches Played Per Day JSON ("/valometa/matches-per-day-json) - takes a JSON
   POST input `{'date_begin': 'YYYY-MM-DD', 'date_end': 'YYYY-MM-DD'}` from a
   [daterangepicker](https://www.daterangepicker.com/) and returns a JSON which
   is ultimately used to plot the number of matches played per day over the time
   period specified in the input.

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

### Matches Scraping

The `MatchesBuild` scraper builds an entirely new 'matches' database table from
scratch and does this by pulling the results from the following page:
`https://vlr.gg/matches/results`. On these pages, there are up to 50 "match
cards" with information about each match being played. These are scraped and the
data is extracted and placed into the 'matches' database table. One can build
this table using the `build-matches-table.py` script with no arguments.

If the 'matches' table was built previously and the database is located in the
correct place ("valometa/data/vlr-gg.db"), then one can use the `MatchesUpdate`
scraper and the `update-matches-table.py` script to get the matches that haven't
been added since the last update or build of the table. Again, this requires
simply running the script in the poetry environment with no arguments.


### Agents Scraping

Another scraper is currently being built to extract the agents played on each
map for every match that is in the 'matches' table of the valometa database.
This is almost done and will be available shortly. Follow ups include: writing
the necessary pandas dataframe manipulations needed to answer the questions we
wish to know about (and plot results) and write API endpoints that allow access
of the resulting data for the front-end plotting code. Will update soon!
