"use strict"


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