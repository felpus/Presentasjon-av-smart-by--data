//used to set the URL where the API is running. (everything before /solapi/.../...) Example: "http://localhost:5000"
host = "http://213.236.208.110/"


document.getElementById('Radio_Year').addEventListener('click', async function () {
    //Set month and day element to non-visible and their values to none
    document.getElementById('month').style.display = 'none';
    document.getElementById('day').style.display = 'none';
    document.getElementById('month').value = 'none';
    document.getElementById('day').value = 'none';
});

document.getElementById('Radio_Month').addEventListener('click', async function () {
    document.getElementById('month').style.display = 'block';
    document.getElementById('day').style.display = 'none';
    document.getElementById('month').value = 1;
    document.getElementById('day').value = 'none';
});

document.getElementById('Radio_Day').addEventListener('click', async function () {
    document.getElementById('month').style.display = 'block';
    document.getElementById('day').style.display = 'block';
    document.getElementById('month').value = 1;
});

$(document).ready(function dropdown () {
    //Variables for month drop down
    const monthNames = ["January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ];

    var selectYear = $("#year");
    var selectMonth = $("#month");
    var selectDay = $("#day");

    var currentYear = new Date().getFullYear();
    var min = 2020;

    for (var y = currentYear; y >= min; y--) {

        var yearElem = document.createElement("option");
        yearElem.value = currentYear
        yearElem.textContent = currentYear;
        selectYear.append(yearElem);
        currentYear--;
    }

    for (var m = 0; m < 12; m++) {

        let month = monthNames[m];
        var monthElem = document.createElement("option");

        monthElem.value = m + 1;
        monthElem.textContent = month;
        selectMonth.append(monthElem);
    }

    var d = new Date();
    var month = d.getMonth();
    var year = d.getFullYear();
    var day = d.getDate();

    selectYear.val(year);
    selectYear.on("change", AdjustDays);
    selectMonth.val(month);
    selectMonth.on("change", AdjustDays);

    AdjustDays();
    selectDay.val(day)

    function AdjustDays() {
        var year = selectYear.val();
        var month = parseInt(selectMonth.val());
        selectDay.empty();

        //get the last day, so the number of days in that month
        var days = new Date(year, month, 0).getDate();

        //lets create the days of that month
        for (var d = 1; d <= days; d++) {
            var dayElem = document.createElement("option");
            dayElem.value = d;
            dayElem.textContent = d;
            selectDay.append(dayElem);
            document.getElementById('day').value = 'none';
        }
    }
});

function googleTranslateElementInit() {
    new google.translate.TranslateElement({pageLanguage: 'en'}, 'google_translate_element');
}

function splice(datetime) {
    return datetime
}

async function getlatest() {

    var langedalsvatnetlatest = (host + "/solapi/recent/latest?sensorid=00000520")
    var guttebuktalatest = (host + "/solapi/recent/latest?sensorid=00000466")
    var traudalsbekken = (host + "/solapi/recent/latest?sensorid=00000519")

    var langedalsvatnetlatestdata = await getdata(langedalsvatnetlatest)
    var guttebuktalatestdata = await getdata(guttebuktalatest)
    var traudalsbekkenlatestdata = await getdata(traudalsbekken)

    var lastreadinglangedalsvatnet = splice(langedalsvatnetlatestdata.datetime)
    var lastreadingguttebukta = splice(guttebuktalatestdata.datetime)
    var lastreadingtraudalsbekken = splice(traudalsbekkenlatestdata.datetime)

    document.getElementById("langedalsvatnetwater").innerHTML = "<b>" + "Langedalsvatnet" +"<br>" + "Last reading: " + "</b>" + "<br>" + lastreadinglangedalsvatnet + "<br>" + "<b>" + "<br>" + "Water temperature: " + "</b>" + "<br>" + langedalsvatnetlatestdata.temperature_b + "°C" + "<b>" + "<br>" + "Air temperature: " + "</b>" + "<br>" + langedalsvatnetlatestdata.temperature + "°C";;
    document.getElementById("guttebuktawater").innerHTML = "<b>" + "Guttebukta" + "<br>" + "Last reading: " + "</b>" + "<br>" + lastreadingguttebukta + "<br>" + "<b>" + "<br>" + "Water temperature: " + "</b>" + "<br>" + guttebuktalatestdata.temperature_b + "°C";
    document.getElementById("traudalsbekkenwater").innerHTML = "<b>" + "Traudalsbekken" +"<br>" + "Last reading: " + "</b>" + "<br>" + lastreadingtraudalsbekken + "<br>" + "<b>" + "<br>" + "Water temperature: " + "</b>" + "<br>" + traudalsbekkenlatestdata.temperature_b + "°C" + "<b>" + "<br>" + "Air temperature: " + "</b>" + "<br>" + traudalsbekkenlatestdata.temperature + "°C";;
    setTimeout(showPage);
}

getlatest()

function showPage() {
    document.getElementById("loader").style.display = "none";
    document.getElementById("myDiv").style.display = "block";
}

async function getdata(api_url) {
    const response = await fetch(api_url);
    const data = await response.json();
    return data;
}

//add sensor label as name for dropdown menu
async function sensorname() {
    let dropdown = document.getElementById('sensorlabel');
    dropdown.length = 0;

    let defaultOption = document.createElement('option');
    defaultOption.text = 'Choose sensor';

    dropdown.add(defaultOption);
    dropdown.selectedIndex = 0;

    const url = host + "/solapi/sensors";

    const request = new XMLHttpRequest();
    request.open('GET', url, true);

    request.onload = function () {
        if (request.status === 200) {
            const data = JSON.parse(request.responseText);
            let option;
            for (let i = 0; i < data.length; i++) {
                option = document.createElement('option');
                option.text = data[i].label;
                option.value = data[i].id;
                dropdown.add(option);
            }
        } else {
            // Reached the server, but it returned an error
        }
    }

    request.onerror = function () {
        console.error('An error occurred fetching the JSON from ' + url);
    };

    request.send();
}

sensorname();

document.getElementById('lastday').addEventListener('click', async function () {
    var sensorid = document.getElementById("sensorlabel").value;
    var sensortype = document.getElementById("sensors").value;
    var url = host + "/solapi/" + sensortype + "/recent/day?sensorid=" + sensorid
    var datasetname = "Data"
    var value = [];
    var time = [];
    var data = await getdata(url);
    var min = data[0].min;
    var max = 0;
    for (var item in data) {
        value.push(data[item][sensortype]);
        time.push(data[item].hour);
        if (data[item].min <= min) {
            min = data[item].min;
            document.getElementById("minv").innerHTML = "<b>" + "Minimum value: " + "</b>" + "<br>" + min;
        }
        if (data[item].max > max) {
            max = data[item].max;
            document.getElementById("maxv").innerHTML = "<b>" + "Maximum value: " + "</b>" + "<br>" + max;
        }
    }

    addData(myChart, value, time, datasetname);
});

document.getElementById('lastweek').addEventListener('click', async function () {
    var sensorid = document.getElementById("sensorlabel").value;
    var sensortype = document.getElementById("sensors").value;
    var url = host + "/solapi/" + sensortype + "/recent/week?sensorid=" + sensorid
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
        date1 = date.slice(0,4)
        date2 = date.slice(17, 23)
        var date3 = date1+" "+date2

        time.push(date3);
        if (data[item].min <= min) {
            min = data[item].min;
            document.getElementById("minv").innerHTML = "<b>" + "Minimum value: " + "</b>" + "<br>" + min;

        }
        if (data[item].max > max) {
            max = data[item].max;
            document.getElementById("maxv").innerHTML = "<b>" + "Maximum value: " + "</b>" + "<br>" + max;
        }
    }

    addData(myChart, value, time, datasetname, maxticks);
});

document.getElementById('lastmonth').addEventListener('click', async function () {
    var sensorid = document.getElementById("sensorlabel").value;
    var sensortype = document.getElementById("sensors").value;
    var url = host + "/solapi/" + sensortype + "/recent/month?sensorid=" + sensorid
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
            document.getElementById("minv").innerHTML = "<b>" + "Minimum value: " + "</b>" + "<br>" + min;
        }
        if (data[item].max > max) {
            max = data[item].max;
            document.getElementById("maxv").innerHTML = "<b>" + "Maximum value: " + "</b>" + "<br>" + max;
        }
    }

    addData(myChart, value, time, datasetname, maxticks);
});

document.getElementById('lastyear').addEventListener('click', async function () {
    var sensorid = document.getElementById("sensorlabel").value;
    var sensortype = document.getElementById("sensors").value;
    var url = host + "/solapi/" + sensortype + "/recent/year?sensorid=" + sensorid
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
            document.getElementById("minv").innerHTML = "<b>" + "Minimum value: " + "</b>" + "<br>" + min;
        }
        if (data[item].max > max) {
            max = data[item].max;
            document.getElementById("maxv").innerHTML = "<b>" + "Maximum value: " + "</b>" + "<br>" + max;
        }
    }

    addData(myChart, value, time, datasetname, maxticks);
});

document.getElementById('timeperiod').addEventListener('click', async function () {
    var sensorid = document.getElementById("sensorlabel").value;
    var sensortype = document.getElementById("sensors").value;
    var sdate = document.getElementById("year").value;
    var sdate2 = document.getElementById("month").value;
    var sdate3 = document.getElementById("day").value;

    var url = host + "/solapi/" + sensortype + "/date?&sensorid=" + sensorid + "&year=" + sdate + "&month=" + sdate2 + "&day=" + sdate3
    var datasetname = "Data"
    var maxticks = "10000"
    var value = [];
    var time = [];
    var data = await getdata(url);
    var min = data[0].min;
    var max = 0;
    for (var item in data) {
        value.push(data[item][sensortype]);
        var date = data[item].datetime
        if (sdate3) {
            date = date.slice(date.length - 5)
        }
        else if (sdate2) {
            date = date.slice(0, 12)
        }
        else if (sdate) {
            date = date.slice(8, 12)
        }
        time.push(date);
        if (data[item].min <= min) {
            min = data[item].min;
            document.getElementById("minv").innerHTML = "<b>" + "Minimum value: " + "</b>" + "<br>" + min;
        }
        if (data[item].max > max) {
            max = data[item].max;
            document.getElementById("maxv").innerHTML = "<b>" + "Maximum value: " + "</b>" + "<br>" + max;
        }
    }

    addData(myChart, value, time, datasetname, maxticks);
});


function addData(chart, data, labels, datasetname, maxticks) {
    chart.data.labels = [];
    chart.data.datasets = [];
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
        responsive: true,
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

var gradientStroke = 'rgba(0, 119, 220, 0.6)',
    gradientFill = 'rgba(0, 119, 220, 0.4)';

var ctx = document.getElementById('luftchart').getContext("2d");

var myChart = new Chart(ctx, config);


// Get the modal
var modal = document.getElementById("myModal");

// Get the button that opens the modal
var btn = document.getElementById("myBtn");

// When the user clicks the button, open the modal
btn.onclick = function () {
    modal.style.display = "block";
}

timeperiod.onclick = function () {
    modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function (event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}