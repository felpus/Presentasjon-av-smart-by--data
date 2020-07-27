async function getdata(api_url) {
    const response = await fetch(api_url);
    const data = await response.json();
    return data;
}

document.getElementById('lastday').addEventListener('click', async function () {
    var sensortype = document.getElementById("sensors").value;
    var url = "http://localhost:5000/solapi/" + sensortype + "/recent/day?sensorid=00000466"
    var datasetname = "Data"
    var value = [];
    var time = [];
    var data = await getdata(url);
    var min = data[0].min;
    var max = 0;
    console.log(data)
    for (var item in data) {
        value.push(data[item][sensortype]);
        time.push(data[item].hour);
        if (data[item].min <= min) {
            min = data[item].min;
            //document.getElementById("minv").innerHTML = "minimum value: " + "<br>" + min;
        }
        if (data[item].max > max) {
            max = data[item].max;
            // document.getElementById("maxv").innerHTML = "maximum value: " + "<br>" + max;
        }
    }

    addData(myChart, value, time, datasetname);
});

document.getElementById('lastweek').addEventListener('click', async function () {
    var sensortype = document.getElementById("sensors").value;
    var url = "http://localhost:5000/solapi/" + sensortype + "/recent/week?sensorid=00000466"
    var datasetname = "Data"
    var maxticks = "7"
    var value = [];
    var time = [];
    var data = await getdata(url);
    var min = data[0].min;
    var max = 0;
    for (var item in data) {
        value.push(data[item][sensortype]);
        var date = data[item].datetime

        time.push(date);
        if (data[item].min <= min) {
            min = data[item].min;
            // document.getElementById("minv").innerHTML = "<b>" + "Minimum value: " + "</b>" + "<br>" + min;

        }
        if (data[item].max > max) {
            max = data[item].max;
            //  document.getElementById("maxv").innerHTML = "<b>" + "Maximum value: " + "</b>" + "<br>" + max;
        }
    }

    addData(myChart, value, time, datasetname, maxticks);
});

document.getElementById('lastmonth').addEventListener('click', async function () {
    var sensortype = document.getElementById("sensors").value;
    var url = "http://localhost:5000/solapi/" + sensortype + "/recent/month?sensorid=00000466"
    var datasetname = "Data"
    var maxticks = "10"
    var value = [];
    var time = [];
    var data = await getdata(url);
    var min = data[0].min;
    var max = 0;
    for (var item in data) {
        value.push(data[item][sensortype]);
        var date = data[item].date
        date = date.slice(0, 12)
        time.push(date);
        if (data[item].min <= min) {
            min = data[item].min;
            //   document.getElementById("minv").innerHTML = "minimum value: " + "<br>" + min;
        }
        if (data[item].max > max) {
            max = data[item].max;
            //   document.getElementById("maxv").innerHTML = "maximum value: " + "<br>" + max;
        }
    }

    addData(myChart, value, time, datasetname, maxticks);
});

document.getElementById('lastyear').addEventListener('click', async function () {
    var sensortype = document.getElementById("sensors").value;
    var url = "http://localhost:5000/solapi/" + sensortype + "/recent/year?sensorid=00000466"
    var datasetname = "Data"
    var maxticks = "13"
    var value = [];
    var time = [];
    var data = await getdata(url);
    var min = data[0].min;
    var max = 0;
    for (var item in data) {
        value.push(data[item][sensortype]);
        time.push(data[item].month);
        if (data[item].min <= min) {
            min = data[item].min;
            //   document.getElementById("minv").innerHTML = "minimum value: " + "<br>" + min;
        }
        if (data[item].max > max) {
            max = data[item].max;
            //  document.getElementById("maxv").innerHTML = "maximum value: " + "<br>" + max;
        }
    }

    addData(myChart, value, time, datasetname, maxticks);
});

function addData(chart, data, labels, datasetname, maxticks) {
    chart.data.labels = [];
    chart.data.datasets = [];
    //changes line color, accepts RGBA, hexadecimal, or HSL notation
    color = '#0092ce';
    var l = labels.length;
    for (var i = 0; i < l; i++) {
        config.data.labels.push(labels[i]);
    }
    config.data.datasets.push({
        label: datasetname,
        fill: false,
        data: data,
        borderColor: color
    });
    config.options.scales.xAxes[0].ticks.maxTicksLimit = maxticks;
    chart.update();
}


var config = {
    type: 'line',
    data: {
        labels: [],
        datasets: [],
    },
    options: {
        responsive: false,
        maintainAspectRatio: true,
        legend: {
            position: "top"
        },
        scales: {
            yAxes: [{
                ticks: {
                    fontColor: "rgba(0,0,0,0.5)",
                    fontStyle: "bold",
                    beginAtZero: false,
                    maxTicksLimit: 25,
                    padding: 20
                },
                gridLines: {
                    drawTicks: false,
                    display: true
                }

            }],
            xAxes: [
                {
                    ticks: {
                        autoSkip: true,
                        maxRotation: 0,
                    }
                }
            ]
        }
    }
}


var ctx = document.getElementById('iframechart').getContext("2d");


var myChart = new Chart(ctx, config);

document.getElementById("lastweek").click();
