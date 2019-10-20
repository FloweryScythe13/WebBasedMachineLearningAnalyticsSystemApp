$(document).ready(function () {

    var predict_actual = JSON.parse(document.getElementById("predict_actual").textContent);
    var regdata0 = JSON.parse(document.getElementById("regdata0").textContent);
    var regdata1 = JSON.parse(document.getElementById("regdata1").textContent);

    var data = [];
    var maxX = 0;
    var minX = 0;
    console.log("predict_actual, if loaded, is as follows:");

    for (var i = 0; i < predict_actual.length; i++) {
        data.push([predict_actual[i][0], predict_actual[i][1]]);
        if (i === 0) {
            maxX = predict_actual[i][0];
            minX = predict_actual[i][0];
        }
        else {
            if (predict_actual[i][0] > maxX) {
                maxX = predict_actual[i][0];
            }
            if (predict_actual[i][0] < minX) {
                minX = predict_actual[i][0]
            }
        }
    }
    
    var minY = regdata0 * minX + regdata1;
    var maxY = regdata0 * maxX + regdata1;

    var dis = document.getElementById("appcontent_trainmodel");
    dis.style.display = "block";

    Highcharts.chart({
        chart: {
            renderTo: 'chart_scatter',
            type: 'scatter',
            zoomType: 'xy'
        },
        title: {
            text: 'Deep Neural Network Regression'
        },
        xAxis: {
            title: {
                enabled: true,
                text: "Prediction (nm)"
            },
            startOnTick: true,
            endOnTick: true,
            showLastLabel: true
        },
        yAxis: {
            title: {
                text: 'Actual (nm)'
            }
        },
        legend: {
            layout: 'vertical',
            align: 'left',
            verticalAlign: 'top',
            x: 100,
            y: 70,
            floating: true,
            borderWidth: 1
        },
        plotOptions: {
            scatter: {
                marker: {
                    radius: 5,
                    states: {
                        hover: {
                            enabled: true,
                            lineColor: 'rgb(100, 100, 100)'
                        }
                    }
                },
                states: {
                    hover: {
                        marker: {
                            enabled: false
                        }
                    }
                },
                tooltip: {
                    headerFormat: '<b>{series.name}</b><br />',
                    pointFormat: '{point.x} nm, {point.y} nm'
                }
            }
        },
        series: [{
            name: 'Regression Line',
            data: [[minX, minY], [maxX, maxY]],
            marker: {
                enabled: false
            },
            type: 'line',
            states: {
                hover: {
                    lineWidth: 0
                }
            },
            enableMouseTracking: false
        },
        {
            name: 'Modeling',
            data: data,
            type: 'scatter',
            marker: {
                radius: 4
            }
        }]
    });
});