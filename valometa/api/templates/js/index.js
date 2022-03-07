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


const picker = new Litepicker({ 
  firstDay: 1,
  format: "YYYY/MM/DD",
  numberOfMonths: 2,
  numberOfColumns: 2,
  autoApply: true,
  showTooltip: false,
  mobileFriendly: true,
  hotelMode: true,
  singleMode: false,
  element: document.getElementById('daterange')
});


async function postDates() {
  let outputData = {
    date_begin : picker.getStartDate().format('YYYY-MM-DD'),
    date_end : picker.getEndDate().format('YYYY-MM-DD')
  };
  let response_data = await postData(
    "/valometa/matches-per-day-json", outputData
  );
  plot(response_data);
};


async function plot(data = []) {
    let xValues = [];
    let yValues = [];

    data.forEach(element => {
        xValues.push(element['date_of_count']);
        yValues.push(element['count']);
    });
    let plotElement = document.getElementById("plot-element");

    let trace = {
        x: xValues,
        y: yValues,
        mode: 'lines'
    };

    let dataToPlot = [trace];
    let layout = {
        title: 'Line Plot Test'
    };

    Plotly.newPlot(plotElement, dataToPlot, layout)
}
