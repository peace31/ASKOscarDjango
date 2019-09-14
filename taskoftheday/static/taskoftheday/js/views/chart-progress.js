$(function () {
    'use strict';

    //convert Hex to RGBA
    function convertHex(hex, opacity) {
        hex = hex.replace('#', '');
        var r = parseInt(hex.substring(0, 2), 16);
        var g = parseInt(hex.substring(2, 4), 16);
        var b = parseInt(hex.substring(4, 6), 16);

        var result = 'rgba(' + r + ',' + g + ',' + b + ',' + opacity / 100 + ')';
        return result;
    }


    var randomScalingFactor = function () {
        return Math.round(Math.random() * 100)
    };
    var lineChartData = {
        labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
        datasets: [
            {
                label: 'My First dataset',
                labelColor: '#fff',
                fontColor: '#fff',
                backgroundColor: 'rgba(220,220,220,0.2)',
                borderColor: 'rgba(220,220,220,1)',
                pointBackgroundColor: 'rgba(220,220,220,1)',
                pointBorderColor: '#fff',
                data: [randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor()]
            }
        ]
    };

    var options = {
        maintainAspectRatio: false,
        legend: {
            display: false,
        },
        scales: {
            xAxes: [{
                gridLines: {
                    display: false,
                    color: '#03A5C5',
                    lineWidth: 8,
                },
                ticks: {
                    fontColor: "white",
                },
            }],
            yAxes: [{
                gridLines: {
                    display: false,
                    color: '#03A5C5',
                    lineWidth: 8,
                },
                ticks: {
                    fontColor: "white",
                    beginAtZero: true,
                }
            }]
        }
    };
    var ctx = document.getElementById('canvas-1');
    var chart = new Chart(ctx, {
        responsive: true,
        type: 'line',
        data: lineChartData,
        options: options
    });