import Highcharts from "../../highcharts/code/es-modules/parts/Globals";

$(document).ready(function () {
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


        Highcharts.chart('')
    }
})
