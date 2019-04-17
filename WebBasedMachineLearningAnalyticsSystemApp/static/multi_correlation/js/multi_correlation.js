if (Object.keys(dataList).length > 0) {
    var dis = document.getElementById("selmenu")
    dis.style.display = "block";
}

function linearRegression(y, x) {
    var lr = {};
    var n = y.length;
    var sum_x = 0
    var sum_y = 0
    var sum_xy = 0
    var sum_xx = 0
    var sum_yy = 0;

    for (var i = 0; i < y.length; i++) {
        sum_x += x[i];
        sum_y += y[i];
        sum_xy += (x[i] * y[i]);
        sum_xx += (x[i] * x[i]);
        sum_yy += (y[i] * y[i]);
    }

    lr['slope'] = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x * sum_x);
    lr['intercept'] = (sum_y - lr.slope * sum_x) / n;
    lr['r2'] = Math.pow((n * sum_xy - sum_x * sum_y) / Math.sqrt((n * sum_xx - sum_x * sum_x) * (n * sum_yy - sum_y * sum_y)), 2);

    return lr;
}

function executeModelFunc() {
    // remove all the elements in chartdiv
    $("#chartdiv").empty();

    // get the HTML element listX from the Variables multi-select options. Get the values.
    var e0 = document.getElementById("listX");
    var parX = e0.options[e0.selectedIndex].value;

    var e = document.getElementById("listY");
    var parY = e.options[e.selectedIndex].value;

    var xList = [];
    for (var i = 0; i < e0.selectedOptions.length; i++) {
        xList.push(e0.selectedOptions[i].value);
    }

    for (var k = 0; k < e0.selectedOptions.length; k++) {
        parX = (e0.selectedOptions[k].value);
        parY = e.options[e.selectedIndex].value;
        var X = [],
            Y = [];

        for (var i = 0; i < labels.length; i++) {
            if (parX == labels[i]) {
                for (var j = 0; j < dataList[i].datavec.length; j++) {
                    X.push(parseFloat(dataList[i].datavec[j]));
                }
            }

            if (parY == labels[i]) {
                for (var j = 0; j < dataList[i].datavec.length; j++) {
                    Y.push(parseFloat(dataList[i].datavec[j]));
                }
            }
        }
    }


    let xMatrix = [],
        xTemp = [],
        yMatrix = numeric.transpose([Y]);

    for (j = 0; j < X.length; j++) {
        xTemp = [];
        for (i = 0; i <= 1; i++) {
            xTemp.push(1 * Math.pow(X[j], i));
        }

        xMatrix.push(xTemp);
    }

    var xMatrixT = numeric.transpose(xMatrix);
    var dot1 = numeric.dot(xMatrixT, xMatrix);
    var dotInv = numeric.inv(dot1);

    var dot2 = numeric.dot(xMatrixT, yMatrix);
    var solution = numeric.dot(dotInv, dot2);
    var predict_actual = [];
    var predict = [];
    var actual = [];
    var formulaStr = "y = ";

    for (i = 0; i < X.length; i++) {
        var num = 0;
        for (j = 0; j <= 1; j++) {
            num = num + solution[j] * Math.pow(X[i], j);
        }

        predict_actual.push([num, Y[i]]);
        predict.push(num);
        actual.push(Y[i]);
    }

    formulaStr = formulaStr + "(" + parseFloat(solution[0]).toExponential(2).toString() + ")" + " + (" + parseFloat(solution[1]).toExponential(2).toString() + ") * x";
    var lr = linearRegression(X, Y);
    var maxX = Math.max.apply(Math, X);
    var minX = Math.min.apply(Math, Y);

    var data = [];
    for (var i = 0; i < X.length; i++) {
        data.push([X[i], Y[i]]);
    }

    var minY = parseFloat(solution[1]) * minX + parseFloat(solution[0]);
    var maxY = parseFloat(solution[1]) * maxX + parseFloat(solution[0]);
    var element = document.getElementById("chartdiv");
    var para = document.createElement("div");
    para.setAttribute("id", parX);
    para.setAttribute("style", "min-width: 600px; height: 500px; margin: 0 auto");
    element.appendChild(para);



    Highcharts.chart(parX, {
        chart: {
            type: 'scatter',
            zoomType: 'xy'
        },
        title: {
            text: 'Correlation'
        },
        subtitle: {
            text: `${parY} vs. ${parX}; R^2 = ${lr.r2.toFixed(2)}, ${formulaStr}`
        },
        xAxis: {
            title: {
                enabled: true,
                text: parX
            },
            startOnTick: true,
            endOnTick: true,
            showLastLabel: true
        },
        yAxis: {
            title: {
                text: parY
            }
        },
        legend: {
            layout: 'vertical',
            align: 'left',
            verticalAlign: 'top',
            x: 80,
            y: 0,
            floating: true,
            backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF',
            borderWidth: 1
        },

        plotOptions: {
            scatter: {
                marker: {
                    radius: 5,
                    states: {
                        hover: {
                            enabled: true,
                            lineColor: 'rgb(100,100,100)'
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
                    headerFormat: '<b>{series.name}</b><br>',
                    pointFormat: '{point.x}, {point.y}'
                }
            }
        },

        series: [
            {
                type: 'line',
                name: 'Regression Line',
                data: [[minX, minY], [maxX, maxY]],
                marker: {
                    enabled: false
                },
                states: {
                    hover: {
                        lineWidth: 0
                    }
                },
                enableMouseTracking: false
            },
            {
                type: 'scatter',
                name: 'Correlation',
                color: 'rgba(223, 83, 83, .5)',
                data: data,
                marker: {
                    radius: 4
                }
            }
        ]
    });

}


