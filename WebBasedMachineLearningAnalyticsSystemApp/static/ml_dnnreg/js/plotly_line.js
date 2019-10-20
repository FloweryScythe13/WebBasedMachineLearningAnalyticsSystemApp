$(document).ready(function () {
    var MSE = JSON.parse(document.getElementById("MSE").textContent);
    var xData = [];
    var yData = [];
    for (var i = 0; i < MSE.length; i++) {
        xData.push(i + 1);
        yData.push(MSE[i]);
    }

    var trace1 = {
        x: xData,
        y: yData,
        type: 'scatter'
    };

    var data = [trace1]

    var layout = {
        title: "Model Training: Mean Squared Error vs Epoches",
        xaxis: {
            title: 'Epoch Number'
        },
        yaxis: {
            title: 'Mean Squared Error'
        }
    };

    Plotly.newPlot("trend_chart", data, layout);
});
