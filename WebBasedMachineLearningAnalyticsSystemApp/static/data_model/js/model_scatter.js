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
            }
        }, {}
    );

    lr['slope'] = (n * sums.sum_xy - sums.sum_x * sums.sum_y) / (n * sums.sum_xx - sums.sum_x ** 2);
    lr['intercept'] = (sums.sum_y - lr.slope * sums.sum_x) / n;
    let r_xy = (n * sums.sum_xy - sums.sum_x * sums.sum_y) / Math.sqrt((n * sums.sum_xx - sums.sum_x ** 2) * (n * sums.sum_yy - sums.sum_y ** 2));
    lr['r2'] = r_xy ** 2; 

    return lr;
}