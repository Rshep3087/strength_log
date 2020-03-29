// define global variables
Chart.defaults.global.responsive = false;
Chart.defaults.global.layout.padding.top = 15;
Chart.defaults.global.elements.point.radius = 10;
Chart.defaults.global.elements.point.hoverRadius = 10;
Chart.defaults.global.elements.point.borderWidth = 1;
Chart.defaults.global.elements.point.hitRadius = 10;
Chart.defaults.global.elements.point.hoverBorderWidth = 2;
Chart.defaults.global.spanGaps = false;
Chart.defaults.global.legend.display = false;

Chart.defaults.global.elements.point.pointStyle = "triangle";

Chart.defaults.global.elements.line.borderWidth = 6;

// define the squat data
var squatData = {
    labels: [{% for item in labels %}
"{{ item }}",
    {% endfor %}],
datasets: [{
    label: 'Squat',
    fill: false,
    backgroundColor: "rgba(75,192,192,0.4)",
    borderColor: "#0509E4",
    borderCapStyle: 'butt',
    borderDash: [],
    borderDashOffset: 0.0,
    borderJoinStyle: 'miter',
    pointBackgroundColor: "#fff",
    pointHoverBackgroundColor: "#0509E4",
    pointHoverBorderColor: "rgba(220,220,220,1)",
    data:
        [{% for item in squat_values %}
                {{ item }},
{% endfor %}],
    }]
};
var benchData = {
    labels:
        [{% for item in labels %}
"{{ item }}",
    {% endfor %}],
datasets: [{
    label: 'Bench',
    fill: false,
    backgroundColor: "rgba(75,192,192,0.4)",
    borderColor: "#04BA04",
    borderCapStyle: 'butt',
    borderDash: [],
    borderDashOffset: 0.0,
    borderJoinStyle: 'miter',
    pointBackgroundColor: "#fff",
    pointHoverBackgroundColor: "#04BA04",
    pointHoverBorderColor: "rgba(220,220,220,1)",
    data:
        [{% for item in bench_values %}
                {{ item }},
{% endfor %}],
    }]
};
var deadliftData = {
    labels:
        [{% for item in labels %}
"{{ item }}",
    {% endfor %}],
datasets: [{
    label: 'Deadlift',
    fill: false,
    backgroundColor: "rgba(75,192,192,0.4)",
    borderColor: "#E45502",
    borderCapStyle: 'butt',
    borderDash: [],
    borderDashOffset: 0.0,
    borderJoinStyle: 'miter',
    pointBackgroundColor: "#fff",
    pointHoverBackgroundColor: "#E45502",
    pointHoverBorderColor: "rgba(220,220,220,1)",
    data:
        [{% for item in deadlift_values %}
                {{ item }},
{% endfor %}],
    }]
};
var pressData = {
    labels: [{% for item in labels %}
"{{ item }}",
    {% endfor %}],
datasets: [{
    label: 'Press',
    fill: false,
    backgroundColor: "rgba(75,192,192,0.4)",
    borderColor: "#F60505",
    borderCapStyle: 'butt',
    borderDash: [],
    borderDashOffset: 0.0,
    borderJoinStyle: 'miter',
    pointBackgroundColor: "#fff",
    pointHoverBackgroundColor: "#F60505",
    pointHoverBorderColor: "rgba(220,220,220,1)",
    data: [{% for item in press_values %}
        {{ item }},
{% endfor %}],
    }]
};

// get squat canvas
var ctxSquat = document.getElementById("squatChart").getContext("2d");
var ctxBench = document.getElementById("benchChart").getContext("2d");
var ctxDeadlift = document.getElementById("deadliftChart").getContext("2d");
var ctxPress = document.getElementById("pressChart").getContext("2d");

// create the chart using the chart canvas
var squatChart = new Chart(ctxSquat, {
    // The type of chart to create
    type: 'line',
    // Data for the chart
    data: squatData,
    // Configuraition options
    options: {
        title: {
            display: true,
            fontSize: 24,
            text: "Squat"
        },
        scales: {
            yAxes: [{
                scaleLabel: {
                    display: true,
                    labelString: "LBS",
                    fontSize: 18
                },
                ticks: {
                    beginAtZero: true
                }
            }],
            xAxes: [{
                scaleLabel: {
                    display: true,
                    labelString: "DATE",
                    fontSize: 18
                }
            }]
        }
    }
});
var benchChart = new Chart(ctxBench, {
    type: 'line',
    data: benchData,
    options: {
        title: {
            display: true,
            fontSize: 24,
            text: "Bench"
        },
        scales: {
            yAxes: [{
                scaleLabel: {
                    display: true,
                    labelString: "LBS",
                    fontSize: 18
                },
                ticks: {
                    beginAtZero: true
                }
            }],
            xAxes: [{
                scaleLabel: {
                    display: true,
                    labelString: "DATE",
                    fontSize: 18
                }
            }]
        }
    }
});
var deadliftChart = new Chart(ctxDeadlift, {
    type: 'line',
    data: deadliftData,
    options: {
        title: {
            display: true,
            fontSize: 24,
            text: "Deadlift"
        },
        scales: {
            yAxes: [{
                scaleLabel: {
                    display: true,
                    labelString: "LBS",
                    fontSize: 18
                },
                ticks: {
                    beginAtZero: true
                }
            }],
            xAxes: [{
                scaleLabel: {
                    display: true,
                    labelString: "DATE",
                    fontSize: 18
                }
            }]
        }
    }
});
var pressChart = new Chart(ctxPress, {
    type: 'line',
    data: pressData,
    options: {
        title: {
            display: true,
            fontSize: 24,
            text: "Press"
        },
        scales: {
            yAxes: [{
                scaleLabel: {
                    display: true,
                    labelString: "LBS",
                    fontSize: 18
                },
                ticks: {
                    beginAtZero: true
                }
            }],
            xAxes: [{
                scaleLabel: {
                    display: true,
                    labelString: "DATE",
                    fontSize: 18
                }
            }]
        }
    }
});