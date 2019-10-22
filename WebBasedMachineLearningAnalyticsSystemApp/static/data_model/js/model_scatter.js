import Highcharts from "../../highcharts/code/es-modules/parts/Globals";

$(document).ready(function () {
    var data_json = JSON.parse(document.getElementById("data_json").textContent);
    var dataList = JSON.parse(document.getElementById("dataList").textContent);
    var labels = JSON.parse(document.getElementById("labels").textContent);
    var labels_all = JSON.parse(document.getElementById("labels_all").textContent);

    if (Object.keys(data_json).length > 0) {
        var dis = document.getElementById("appcontent_trainmodel");
        dis.style.display = "block";
    }

    $("#data-table tr").click(function () {
        $(this).addClass("selected").siblings().removeClass("selected");
    });

    /*
     * Linear regression for two matrices X and Y. This method finds the best-fit line, intercept, and R2 value for a pair of X & Y vectors.
     * It does that through the use of two quantities from statistics: the sample correlation coefficient r_xy as an estimate of Pearson's product-moment coefficient (which in this case,
     * when squared, gives you R2) and the least-squares estimate formula for Beta as used in a beginner-friendly simple linear regression model,
     * which is Beta = Covariance(x,y)/Variance(x) = (sum(x_i * y_i) - 1/n * sum(x_i)*sum(y_i)) / (sum(y_i^2) - 1/n * (sum(y_i))^2). 
     * The formulas used in author King's implementation are slightly different, insofar as he multiplied the two equations by n/n to get rid of
     * the 1/n.
     */
    function linearRegression(y, x) {
        var lr = {};
        var n = y.length;

        //King does the summations here using a single simple for-loop, but I'll take this opportunity to practice with the map and reduce patterns.   


        const sums = y.map((yVal, i) => [x[i], yVal]).reduce(
            (sumSet, elem, i) => {
                return {
                    ...sumSet,
                    sum_x: (sumSet[sum_x] || 0) + elem[0],
                    sum_y: (sumSet[sum_y] || 0) + elem[1],
                    sum_xy: (sumSet[sum_xy] || 0) + elem[0] * elem[1],
                    sum_xx: (sumSet[sum_xx] || 0) + elem[0] ** 2,
                    sum_yy: (sumSet[sum_yy] || 0) + elem[1] ** 2
                };
            }, {}
        );

        lr['slope'] = (n * sums.sum_xy - sums.sum_x * sums.sum_y) / (n * sums.sum_xx - sums.sum_x ** 2);
        lr['intercept'] = (sums.sum_y - lr.slope * sums.sum_x) / n;
        let r_xy = (n * sums.sum_xy - sums.sum_x * sums.sum_y) / Math.sqrt((n * sums.sum_xx - sums.sum_x ** 2) * (n * sums.sum_yy - sums.sum_y ** 2));
        lr['r2'] = r_xy ** 2;

        return lr;
    }

    function estimateCoefficientsWithOLS(xVector, yVector, order) {
        var xMatrix = [],
            xTransformed = [];
        var yMatrix = numeric.transpose([yVector]);

        for (j = 0; j < xVector.length; j++) {
            xTransformed = [];
            for (var k = 0; k <= order; k++) {
                xTransformed.push(xVector[j] ** k);
            }
            xMatrix.push(xTransformed);
        }
        //Now that we have the transformed matrix for X, we find the vector of coefficients Beta 
        //via the formula Beta = ((xMatrix^T) dot xMatrix)^-1 dot ((xMatrix^T) dot yMatrix).
        var xMatrixT = numeric.transpose(xMatrix);
        var dot1 = numeric.dot(xMatrixT, xMatrix);
        var dotInv = numeric.inv(dot1);
        var dotRHS = numeric.dot(xMatrixT, yMatrix);
        var beta = numeric.dot(dotInv, dotRHS);

        return beta;
    }

    function executeModelFunc() {
        var dis1 = document.getElementById("selmenu");
        dis1.style.display = "inline-block";
        var e = document.getElementById("listX");
        var parameterX = e.options[e.selectedIndex].value;
        var f = $("#listY");
        var parameterY = f.options[f.selectedIndex].value;
        var data = [],
            X = [],
            Y = [];

        //Extract the X & Y data columns selected by the user into the X and Y array variables
        for (var i = 0; i < labels.length; i++) {
            if (labels[i] === parameterX) {
                X = dataList[i].datavec;
            }
            if (labels[i] === parameterY) {
                Y = dataList[i].datavec;
            }
        }

        var order = document.getElementsByName("order")[0].value;
        var beta = estimateCoefficientsWithOLS(X, Y, order);

        var predict_actual = [],
            predict = [],
            actual = [];
        var formulaStr = "y = ";
        //now we use the Beta coefficients to find the values of the y_model vector
        for (i = 0; i < X.length; i++) {
            var y_predict = 0;
            for (j = 0; j <= order; j++) {
                y_predict += beta[j] * (X[i] ** j);
                if (i === 0) {
                    var newt = parseFloat(solution[j]).toExponential(2);
                    if (j === 0) {
                        formulaStr += `(${newt.toString()})`;
                    }
                    else {
                        formulaStr += ` + (${newt.toString()})*x^${j.toString()}`;
                    }
                }
            }
            predict.push(y_predict);
            actual.push(Y[i]);
            predict_actual.push(y_predict, Y[i]);
        }

        /* It took me a while to figure out the reasoning behind this section below. It applies ordinary
         * least squares estimation a second time to find the linear best-fit line between the predicted 
         * and actual values. That line is what gets plotted to the user in the original code of the book
         * (not including my own plot addition). It appears that the author needed/opted to do this because
         * Highchart line series can only be drawn as straight lines between points. 
         */
        var evaluationBeta = estimateCoefficientsWithOLS(predict, actual, 1);

        var data2 = [];
        var maxX = 0,
            minX = 0;
        for (i = 0; i < predict_actual.length; i++) {
            data2.push([parseFloat(predict_actual[i][0]), parseFloat(predict_actual[i][1])]);
            if (i === 0) {
                maxX = minX = parseFloat(predict_actual[i][0]);
            }
            else {
                if (predict_actual[i][0] > maxX) {
                    maxX = predict_actual[i][0];
                }
                if (predict_actual[i][0] < minX) {
                    minX = predict_actual[i][0];
                }
            }
        }

        var minY = evaluationBeta[1] * minX + evaluationBeta[0];
        var maxY = evaluationBeta[1] * maxX + evaluationBeta[0];
        var lr = linearRegression(predict, actual);

        formulaStr += "<br>";
        formulaStr += `R2 = ${lr.r2.toFixed(3)}`;
        $("#formula").html(formulaStr);


        Highcharts.chart('model_scatter', {
            chart: {
                type: 'scatter',
                zoomType: 'xy'
            },
            title: {
                text: 'Data Plot'
            },
            xAxis: {
                title: {
                    enabled: true,
                    text: 'X'
                },
                startOnTick: true,
                endOnTick: true,
                showLastLabel: true
            },
            yAxis: {
                title: {
                    text: 'Y'
                }
            },
            legend: {
                layout: 'vertical',
                align: 'left',
                verticalAlign: 'top',
                x: 100,
                y: 20,
                floating: true,
                backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColor) || "#FFFFFF",
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
                        headerFormat: '<b>{series.name}</b>',
                        pointFormat: '{point.x}, {point.y}'
                    }
                }
            },
            series: [
                {
                    type: 'line',
                    name: 'Regression Accuracy Line',
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
                    name: 'Modeling',
                    color: "rgba(223, 83, 83, 0.5)",
                    data: data,
                    marker: {
                        radius: 4
                    }
                }]
        });
    }

    //The method that King used involves taking the natural log of the equation Y(t) = exp(Beta*X(t)) and writing 
    //the Y-parameter column into the variable for that transformed Y, and then applying the above 
    //ordinary least squares estimation technique to the resulting linear equation to find the 
    //coefficients. However, we are going to be different and use French mathematician J. Jacquelin's 
    //method instead, pulled from his paper "Régressions et équations intégrales" (2014). Refer to 
    //https://math.stackexchange.com/questions/350754/fitting-exponential-curve-to-data for more information.
    function executeModelFuncExponential() {
        var dis1 = document.getElementById("selmenu");
        dis1.style.display = "inline-block";
        var e = document.getElementById("listX");
        var parameterX = e.options[e.selectedIndex].value;
        var f = $("#listY");
        var parameterY = f.options[f.selectedIndex].value;
        let X = [],
            Y = [],
            points = [];

        //Extract the X & Y data columns selected by the user into the X and Y array variables
        for (var i = 0; i < labels.length; i++) {
            if (labels[i] === parameterX) {
                X = dataList[i].datavec;
            }
            if (labels[i] === parameterY) {
                Y = dataList[i].datavec;
            }
        }

        for (var j = 0; j < X.length; j++) {
            points.push(new { x: X[j], y: Y[j] });
        }
        points = points.sort((a, b) => a - b);

        var S = [];
        var sumXSquared = 0,
            sumX_S = 0,
            sumSSquared = 0,
            sumYX = 0,
            sumY_S = 0;
        for (var k = 0; k < points.length; k++) {
            if (k === 0)
                S.push(0);
            else {
                S.push(S[k - 1] + 0.5 * (points[k].y + points[k - 1].y) * (points[k].x - points[k - 1].x));
                sumXSquared += (points[k].x - points[0].x) ** 2;
                sumX_S += (points[k].x - points[0].x) * S[k];
                sumSSquared += S[k] ** 2;
                sumYX += (points[k].y - points[0].y) * (points[k].x - points[0].x);
                sumY_S += (points[k].y - points[0].y) * S[k];
            }
        }

        var momentMatrix1 = [
            [sumXSquared, sumX_S],
            [sumX_S, sumSSquared]
        ];
        momentMatrix1 = numeric.inv(momentMatrix1);
        var momentMatrix2 = [
            sumYX,
            sumY_S
        ];
        var Beta_initial = numeric.dot(momentMatrix1, momentMatrix2);
        var c2 = Beta_initial[1];
        var thetas = [];
        var sumTheta = 0,
            sumThetaSquared = 0,
            sumY = 0,
            sumYTheta = 0;
        for (var l = 0; l < points.length; l++) {
            var theta_l = Math.exp(c2 * points[l].x);
            thetas.push(theta_l);
            sumTheta += theta_l;
            sumThetaSquared += theta_l ** 2;
            sumY += points[l].y;
            sumYTheta += points[l].y * theta_l;
        }
        var leftMomentMatrix2 = new math.matrix([
            [points.length, sumTheta],
            [sumTheta, sumThetaSquared]
        ]);
        leftMomentMatrix2 = math.inv(leftMomentMatrix2);
        var rightMomentMatrix2 = math.matrix([sumY, sumYTheta]);
        var Beta_solution = math.dot(leftMomentMatrix2, rightMomentMatrix2);
        var a2 = Beta_solution[0];
        var b2 = Beta_solution[1];

        var formulaStr = "y = ";
        var predict_actual = [],
            predict = [],
            actual = [];

        //now we use the Beta coefficients to find the values of the y_model vector
        for (i = 0; i < X.length; i++) {
            var y_predict = a2 + b2 * Math.exp(c2 * X[i]);
            formulaStr += `${a2.toExponential(2).toString()} + ${b2.toExponential(2)}*exp(${c2.toExponential(2)}*x)`;

            predict.push(y_predict);
            actual.push(Y[i]);
            predict_actual.push(y_predict, Y[i]);
        }

        var evaluationBeta = estimateCoefficientsWithOLS(predict, actual, 1);

        var data2 = [];
        var maxX = 0,
            minX = 0;
        for (i = 0; i < predict_actual.length; i++) {
            data2.push([parseFloat(predict_actual[i][0]), parseFloat(predict_actual[i][1])]);
            if (i === 0) {
                maxX = minX = parseFloat(predict_actual[i][0]);
            }
            else {
                if (predict_actual[i][0] > maxX) {
                    maxX = predict_actual[i][0];
                }
                if (predict_actual[i][0] < minX) {
                    minX = predict_actual[i][0];
                }
            }
        }

        var minY = evaluationBeta[1] * minX + evaluationBeta[0];
        var maxY = evaluationBeta[1] * maxX + evaluationBeta[0];
        var lr = linearRegression(predict, actual);

        formulaStr += "<br>";
        formulaStr += `R2 = ${lr.r2.toFixed(3)}`;
        $("#formula").html(formulaStr);

        Highcharts.chart("model_scatter_exponential", {
            chart: {
                type: 'scatter',
                zoomType: 'xy'
            },
            title: {
                text: 'Data Plot'
            },
            xAxis: {
                title: {
                    enabled: true,
                    text: 'X'
                },
                startOnTick: true,
                endOnTick: true,
                showLastLabel: true
            },
            yAxis: {
                title: {
                    text: 'Y'
                }
            },
            legend: {
                layout: 'vertical',
                align: 'left',
                verticalAlign: 'top',
                x: 100,
                y: 20,
                floating: true,
                backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColor) || "#FFFFFF",
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
                        headerFormat: '<b>{series.name}</b>',
                        pointFormat: '{point.x}, {point.y}'
                    }
                }
            },
            series: [
                {
                    type: 'line',
                    name: 'Regression Accuracy Line',
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
                    name: 'Modeling',
                    color: "rgba(223, 83, 83, 0.5)",
                    data: data2,
                    marker: {
                        radius: 4
                    }
                }]
        });
    }
});
