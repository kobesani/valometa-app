"use strict"

// Example POST method implementation:
async function postData(url = '', data = {}) {
    // Default options are marked with *
    const response = await fetch(url, {
      method: 'POST', // *GET, POST, PUT, DELETE, etc.
      mode: 'cors', // no-cors, *cors, same-origin
      cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
      credentials: 'same-origin', // include, *same-origin, omit
      headers: {
        'Content-Type': 'application/json'
        // 'Content-Type': 'application/x-www-form-urlencoded',
      },
      redirect: 'follow', // manual, *follow, error
      referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
      body: JSON.stringify(data) // body data type must match "Content-Type" header
    });
    return response.json(); // parses JSON response into native JavaScript objects
  }


$(function() {
    $('input[name="daterange"]').daterangepicker({
      opens: 'left'
    }, async function(start, end, label) {
        let timeFormat = "YYYY-MM-DD";
        let outputData = {
          date_begin : start.format(timeFormat),
          date_end : end.format(timeFormat)
        };
        console.log(outputData);
        let response_data = await postData(
            "/valometa/matches-per-day-json", outputData
        );
        plot(response_data);
    });
  });


async function plot(data = []) {
    let xValues = [];
    let yValues = [];

    data.forEach(element => {
        xValues.push(element['date_of_count']);
        yValues.push(element['count']);
    });
    let testerEl = document.getElementById("tester");

    let trace = {
        x: xValues,
        y: yValues,
        mode: 'lines'
    };

    let dataToPlot = [trace];
    let layout = {
        title: 'Line Plot Test'
    };

    Plotly.newPlot(testerEl, dataToPlot, layout)
}


async function fetch_matches_per_day() {
    let fetched_data;

    await fetch("/valometa/matches-per-day-json")
      .then(response => response.json())
      .then(data => fetched_data = data);
    //   .then(() => console.log(fetched_data));

    return fetched_data;
}


async function test() {
    let data = await fetch_matches_per_day();
    let xValues = [];
    let yValues = [];

    data.forEach(element => {
        xValues.push(element['date_of_count']);
        yValues.push(element['count']);
    });
    let testerEl = document.getElementById("tester");

    let trace = {
        x: xValues,
        y: yValues,
        mode: 'lines'
    };

    let dataToPlot = [trace];
    let layout = {
        title: 'Line Plot Test'
    };

    Plotly.newPlot(testerEl, dataToPlot, layout)
}