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


    //Cards with Charts
    var labels = ['January', 'February', 'March', 'April', 'May', 'June', 'July'];
    var data = {
        labels: labels,
        datasets: [
            {
                label: 'My First dataset',
                backgroundColor: 'rgba(255,255,255,.2)',
                borderColor: 'rgba(255,255,255,.55)',
                data: [65, 59, 84, 84, 51, 55, 40]
            },
        ]
    };
    var options = {
        maintainAspectRatio: false,
        legend: {
            display: false
        },
        scales: {
            xAxes: [{
                gridLines: {
                    color: 'transparent',
                    zeroLineColor: 'transparent'
                },
                ticks: {
                    fontSize: 2,
                    fontColor: 'transparent',
                }

            }],
            yAxes: [{
                display: false,
                ticks: {
                    display: false,
                    min: Math.min.apply(Math, data.datasets[0].data) - 5,
                    max: Math.max.apply(Math, data.datasets[0].data) + 5,
                }
            }],
        },
        elements: {
            line: {
                borderWidth: 1
            },
            point: {
                radius: 4,
                hitRadius: 10,
                hoverRadius: 4,
            },
        }
    };
    var ctx = $('#card-chart1');
    var cardChart1 = new Chart(ctx, {
        type: 'line',
        data: data,
        options: options
    });

    var labels = ['January', 'February', 'March', 'April', 'May', 'June', 'July'];
    var data = {
        labels: labels,
        datasets: [
            {
                label: 'My First dataset',
                backgroundColor: 'rgba(255,255,255,.2)',
                borderColor: 'rgba(255,255,255,.55)',
                data: [65, 59, 84, 84, 51, 55, 40]
            },
        ]
    };
    var options = {
        maintainAspectRatio: false,
        legend: {
            display: false
        },
        scales: {
            xAxes: [{
                gridLines: {
                    color: 'transparent',
                    zeroLineColor: 'transparent'
                },
                ticks: {
                    fontSize: 2,
                    fontColor: 'transparent',
                }

            }],
            yAxes: [{
                display: false,
                ticks: {
                    display: false,
                    min: Math.min.apply(Math, data.datasets[0].data) - 5,
                    max: Math.max.apply(Math, data.datasets[0].data) + 5,
                }
            }],
        },
        elements: {
            line: {
                borderWidth: 1
            },
            point: {
                radius: 4,
                hitRadius: 10,
                hoverRadius: 4,
            },
        }
    };
    var ctx = $('#card-chart2');
    var cardChart2 = new Chart(ctx, {
        type: 'line',
        data: data,
        options: options
    });

    var labels = ['January', 'February', 'March', 'April', 'May', 'June', 'July'];
    var data = {
        labels: labels,
        datasets: [
            {
                label: 'My First dataset',
                backgroundColor: 'rgba(255,255,255,.2)',
                borderColor: 'rgba(255,255,255,.55)',
                data: [65, 59, 84, 84, 51, 55, 40]
            },
        ]
    };
    var options = {
        maintainAspectRatio: false,
        legend: {
            display: false
        },
        scales: {
            xAxes: [{
                gridLines: {
                    color: 'transparent',
                    zeroLineColor: 'transparent'
                },
                ticks: {
                    fontSize: 2,
                    fontColor: 'transparent',
                }

            }],
            yAxes: [{
                display: false,
                ticks: {
                    display: false,
                    min: Math.min.apply(Math, data.datasets[0].data) - 5,
                    max: Math.max.apply(Math, data.datasets[0].data) + 5,
                }
            }],
        },
        elements: {
            line: {
                borderWidth: 1
            },
            point: {
                radius: 4,
                hitRadius: 10,
                hoverRadius: 4,
            },
        }
    };
    var ctx = $('#card-chart3');
    var cardChart3 = new Chart(ctx, {
        type: 'line',
        data: data,
        options: options
    });

    var labels = ['January', 'February', 'March', 'April', 'May', 'June', 'July'];
    var data = {
        labels: labels,
        datasets: [
            {
                label: 'My First dataset',
                backgroundColor: 'rgba(255,255,255,.2)',
                borderColor: 'rgba(255,255,255,.55)',
                data: [65, 59, 84, 84, 51, 55, 40]
            },
        ]
    };
    var options = {
        maintainAspectRatio: false,
        legend: {
            display: false
        },
        scales: {
            xAxes: [{
                gridLines: {
                    color: 'transparent',
                    zeroLineColor: 'transparent'
                },
                ticks: {
                    fontSize: 2,
                    fontColor: 'transparent',
                }

            }],
            yAxes: [{
                display: false,
                ticks: {
                    display: false,
                    min: Math.min.apply(Math, data.datasets[0].data) - 5,
                    max: Math.max.apply(Math, data.datasets[0].data) + 5,
                }
            }],
        },
        elements: {
            line: {
                borderWidth: 1
            },
            point: {
                radius: 4,
                hitRadius: 10,
                hoverRadius: 4,
            },
        }
    };

    var ctx = $('#card-chart4');
    var cardChart4 = new Chart(ctx, {
        type: 'line',
        data: data,
        options: options
    });


    var labels = ['January', 'February', 'March', 'April', 'May', 'June', 'July'];
    var data = {
        labels: labels,
        datasets: [
            {
                label: 'My First dataset',
                backgroundColor: 'rgba(255,255,255,.2)',
                borderColor: 'rgba(255,255,255,.55)',
                data: [65, 59, 84, 84, 51, 55, 40]
            },
        ]
    };
    var options = {
        maintainAspectRatio: false,
        legend: {
            display: false
        },
        scales: {
            xAxes: [{
                gridLines: {
                    color: 'transparent',
                    zeroLineColor: 'transparent'
                },
                ticks: {
                    fontSize: 2,
                    fontColor: 'transparent',
                }

            }],
            yAxes: [{
                display: false,
                ticks: {
                    display: false,
                    min: Math.min.apply(Math, data.datasets[0].data) - 5,
                    max: Math.max.apply(Math, data.datasets[0].data) + 5,
                }
            }],
        },
        elements: {
            line: {
                borderWidth: 1
            },
            point: {
                radius: 4,
                hitRadius: 10,
                hoverRadius: 4,
            },
        }
    };
    var ctx = $('#card-chart5');
    var cardChart5 = new Chart(ctx, {
        type: 'line',
        data: data,
        options: options
    });


    var labels = ['January', 'February', 'March', 'April', 'May', 'June', 'July'];
    var data = {
        labels: labels,
        datasets: [
            {
                label: 'My First dataset',
                backgroundColor: 'rgba(255,255,255,.2)',
                borderColor: 'rgba(255,255,255,.55)',
                data: [65, 59, 84, 84, 51, 55, 40]
            },
        ]
    };
    var options = {
        maintainAspectRatio: false,
        legend: {
            display: false
        },
        scales: {
            xAxes: [{
                gridLines: {
                    color: 'transparent',
                    zeroLineColor: 'transparent'
                },
                ticks: {
                    fontSize: 2,
                    fontColor: 'transparent',
                }

            }],
            yAxes: [{
                display: false,
                ticks: {
                    display: false,
                    min: Math.min.apply(Math, data.datasets[0].data) - 5,
                    max: Math.max.apply(Math, data.datasets[0].data) + 5,
                }
            }],
        },
        elements: {
            line: {
                borderWidth: 1
            },
            point: {
                radius: 4,
                hitRadius: 10,
                hoverRadius: 4,
            },
        }
    };
    var ctx = $('#card-chart6');
    var cardChart6 = new Chart(ctx, {
        type: 'line',
        data: data,
        options: options
    });


    var labels = ['January', 'February', 'March', 'April', 'May', 'June', 'July'];
    var data = {
        labels: labels,
        datasets: [
            {
                label: 'My First dataset',
                backgroundColor: 'rgba(255,255,255,.2)',
                borderColor: 'rgba(255,255,255,.55)',
                data: [65, 59, 84, 84, 51, 55, 40]
            },
        ]
    };
    var options = {
        maintainAspectRatio: false,
        legend: {
            display: false
        },
        scales: {
            xAxes: [{
                gridLines: {
                    color: 'transparent',
                    zeroLineColor: 'transparent'
                },
                ticks: {
                    fontSize: 2,
                    fontColor: 'transparent',
                }

            }],
            yAxes: [{
                display: false,
                ticks: {
                    display: false,
                    min: Math.min.apply(Math, data.datasets[0].data) - 5,
                    max: Math.max.apply(Math, data.datasets[0].data) + 5,
                }
            }],
        },
        elements: {
            line: {
                borderWidth: 1
            },
            point: {
                radius: 4,
                hitRadius: 10,
                hoverRadius: 4,
            },
        }
    };
    var ctx = $('#card-chart7');
    var cardChart7 = new Chart(ctx, {
        type: 'line',
        data: data,
        options: options
    });


    var labels = ['January', 'February', 'March', 'April', 'May', 'June', 'July'];
    var data = {
        labels: labels,
        datasets: [
            {
                label: 'My First dataset',
                backgroundColor: 'rgba(255,255,255,.2)',
                borderColor: 'rgba(255,255,255,.55)',
                data: [65, 59, 84, 84, 51, 55, 40]
            },
        ]
    };
    var options = {
        maintainAspectRatio: false,
        legend: {
            display: false
        },
        scales: {
            xAxes: [{
                gridLines: {
                    color: 'transparent',
                    zeroLineColor: 'transparent'
                },
                ticks: {
                    fontSize: 2,
                    fontColor: 'transparent',
                }

            }],
            yAxes: [{
                display: false,
                ticks: {
                    display: false,
                    min: Math.min.apply(Math, data.datasets[0].data) - 5,
                    max: Math.max.apply(Math, data.datasets[0].data) + 5,
                }
            }],
        },
        elements: {
            line: {
                borderWidth: 1
            },
            point: {
                radius: 4,
                hitRadius: 10,
                hoverRadius: 4,
            },
        }
    };
    var ctx = $('#card-chart8');
    var cardChart8 = new Chart(ctx, {
        type: 'line',
        data: data,
        options: options
    });


    var labels = ['January', 'February', 'March', 'April', 'May', 'June', 'July'];
    var data = {
        labels: labels,
        datasets: [
            {
                label: 'My First dataset',
                backgroundColor: 'rgba(255,255,255,.2)',
                borderColor: 'rgba(255,255,255,.55)',
                data: [65, 59, 84, 84, 51, 55, 40]
            },
        ]
    };
    var options = {
        maintainAspectRatio: false,
        legend: {
            display: false
        },
        scales: {
            xAxes: [{
                gridLines: {
                    color: 'transparent',
                    zeroLineColor: 'transparent'
                },
                ticks: {
                    fontSize: 2,
                    fontColor: 'transparent',
                }

            }],
            yAxes: [{
                display: false,
                ticks: {
                    display: false,
                    min: Math.min.apply(Math, data.datasets[0].data) - 5,
                    max: Math.max.apply(Math, data.datasets[0].data) + 5,
                }
            }],
        },
        elements: {
            line: {
                borderWidth: 1
            },
            point: {
                radius: 4,
                hitRadius: 10,
                hoverRadius: 4,
            },
        }
    };
    var ctx = $('#card-chart9');
    var cardChart9 = new Chart(ctx, {
        type: 'line',
        data: data,
        options: options
    });


    //Sparkline Charts
    var labels = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];

    var options = {
        legend: {
            display: false,
        },
        scales: {
            xAxes: [{
                display: false,
            }],
            yAxes: [{
                display: false,
            }]
        },
        elements: {
            point: {
                radius: 0,
                hitRadius: 10,
                hoverRadius: 4,
                hoverBorderWidth: 3,
            }
        },
    };

    var data1 = {
        labels: labels,
        datasets: [
            {
                backgroundColor: 'transparent',
                borderColor: $.brandPrimary,
                borderWidth: 2,
                data: [35, 23, 56, 22, 97, 23, 64]
            }
        ]
    };
    var ctx = $('#sparkline-chart-1');
    var sparklineChart1 = new Chart(ctx, {
        type: 'line',
        data: data1,
        options: options
    });

    var data2 = {
        labels: labels,
        datasets: [
            {
                backgroundColor: 'transparent',
                borderColor: $.brandDanger,
                borderWidth: 2,
                data: [78, 81, 80, 45, 34, 12, 40]
            }
        ]
    };
    var ctx = $('#sparkline-chart-2');
    var sparklineChart2 = new Chart(ctx, {
        type: 'line',
        data: data2,
        options: options
    });

    var data3 = {
        labels: labels,
        datasets: [
            {
                backgroundColor: 'transparent',
                borderColor: $.brandWarning,
                borderWidth: 2,
                data: [35, 23, 56, 22, 97, 23, 64]
            }
        ]
    };
    var ctx = $('#sparkline-chart-3');
    var sparklineChart3 = new Chart(ctx, {
        type: 'line',
        data: data3,
        options: options
    });

    var data4 = {
        labels: labels,
        datasets: [
            {
                backgroundColor: 'transparent',
                borderColor: $.brandSuccess,
                borderWidth: 2,
                data: [78, 81, 80, 45, 34, 12, 40]
            }
        ]
    };
    var ctx = $('#sparkline-chart-4');
    var sparklineChart4 = new Chart(ctx, {
        type: 'line',
        data: data4,
        options: options
    });

    var data5 = {
        labels: labels,
        datasets: [
            {
                backgroundColor: 'transparent',
                borderColor: '#d1d4d7',
                borderWidth: 2,
                data: [35, 23, 56, 22, 97, 23, 64]
            }
        ]
    };
    var ctx = $('#sparkline-chart-5');
    var sparklineChart5 = new Chart(ctx, {
        type: 'line',
        data: data5,
        options: options
    });

    var data6 = {
        labels: labels,
        datasets: [
            {
                backgroundColor: 'transparent',
                borderColor: $.brandInfo,
                borderWidth: 2,
                data: [78, 81, 80, 45, 34, 12, 40]
            }
        ]
    };
    var ctx = $('#sparkline-chart-6');
    var sparklineChart6 = new Chart(ctx, {
        type: 'line',
        data: data6,
        options: options
    });

});


var randomScalingFactor = function () {
    return Math.round(Math.random() * 900)
};
var lineChartData = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    datasets: [
        {
            label: 'Revenue',
            labelColor: '#fff',
            fontColor: '#fff',
            backgroundColor: 'rgba(220,220,220,0.2)',
            borderColor: 'rgba(220,220,220,1)',
            pointBackgroundColor: 'rgba(220,220,220,1)',
            pointBorderColor: '#fff',
            data: [randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor()]
        }
    ]
};

var options = {
        maintainAspectRatio: true,
        tooltips: {
            callbacks: {
                label: (item) = > `${item.yLabel} USD`,
        },
    },
    legend
:
{
    display: false,
}
,
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
        yAxes
:
    [{
        gridLines: {
            display: false,
            color: '#03A5C5',
            lineWidth: 8,
        },
        ticks: {
            callback: function (value) {
                return Number(value).toFixed() + " USD"
            },
            fontColor: "white",
            beginAtZero: true,
        }
    }]
}
}
;
var ctx = document.getElementById('revenue-chart');
var chart = new Chart(ctx, {
    responsive: true,
    type: 'line',
    data: lineChartData,
    options: options
});

var randomScalingFactor = function () {
    return Math.round(Math.random() * 15)
};
var lineChartData = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    datasets: [
        {
            label: 'Revenue per user',
            labelColor: '#fff',
            fontColor: '#fff',
            backgroundColor: 'rgba(220,220,220,0.2)',
            borderColor: 'rgba(220,220,220,1)',
            pointBackgroundColor: 'rgba(220,220,220,1)',
            pointBorderColor: '#fff',
            data: [randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor()]
        }
    ]
};

var options = {
        maintainAspectRatio: true,
        tooltips: {
            callbacks: {
                label: (item) = > `${item.yLabel} USD`,
        },
    },
    legend
:
{
    display: false,
}
,
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
        yAxes
:
    [{
        gridLines: {
            display: false,
            color: '#03A5C5',
            lineWidth: 8,
        },
        ticks: {
            callback: function (value) {
                return Number(value).toFixed() + " USD"
            },
            fontColor: "white",
            beginAtZero: true,
        }
    }]
}
}
;
var ctx = document.getElementById('rpu-chart');
var chart = new Chart(ctx, {
    responsive: true,
    type: 'line',
    data: lineChartData,
    options: options
});


var randomScalingFactor = function () {
    return Math.round(Math.random() * 80)
};
var lineChartData = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    datasets: [
        {
            label: 'Average order value',
            labelColor: '#fff',
            fontColor: '#fff',
            backgroundColor: 'rgba(220,220,220,0.2)',
            borderColor: 'rgba(220,220,220,1)',
            pointBackgroundColor: 'rgba(220,220,220,1)',
            pointBorderColor: '#fff',
            data: [randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor()]
        }
    ]
};

var options = {
        maintainAspectRatio: true,
        tooltips: {
            callbacks: {
                label: (item) = > `${item.yLabel} USD`,
        },
    },
    legend
:
{
    display: false,
}
,
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
        yAxes
:
    [{
        gridLines: {
            display: false,
            color: '#03A5C5',
            lineWidth: 8,
        },
        ticks: {
            callback: function (value) {
                return Number(value).toFixed() + " USD"
            },
            fontColor: "white",
            beginAtZero: true,
        }
    }]
}
}
;
var ctx = document.getElementById('aov-chart');
var chart = new Chart(ctx, {
    responsive: true,
    type: 'line',
    data: lineChartData,
    options: options
});


var randomScalingFactor = function () {
    return Math.round(Math.random() * 12)
};
var lineChartData = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    datasets: [
        {
            label: 'Conversion rate',
            labelColor: '#fff',
            fontColor: '#fff',
            backgroundColor: 'rgba(220,220,220,0.2)',
            borderColor: 'rgba(220,220,220,1)',
            pointBackgroundColor: 'rgba(220,220,220,1)',
            pointBorderColor: '#fff',
            data: [randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor()]
        }
    ]
};

var options = {
        maintainAspectRatio: true,
        tooltips: {
            callbacks: {
                label: (item) = > `${item.yLabel}%`,
        },
    },
    legend
:
{
    display: false,
}
,
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
        yAxes
:
    [{
        gridLines: {
            display: false,
            color: '#03A5C5',
            lineWidth: 8,
        },
        ticks: {
            callback: function (value) {
                return Number(value).toFixed() + "%"
            },
            fontColor: "white",
            beginAtZero: true,
        }
    }]
}
}
;
var ctx = document.getElementById('cr-chart');
var chart = new Chart(ctx, {
    responsive: true,
    type: 'line',
    data: lineChartData,
    options: options
});


var randomScalingFactor = function () {
    return Math.round(Math.random() * 80)
};
var lineChartData = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    datasets: [
        {
            label: 'Bounce rate',
            labelColor: '#fff',
            fontColor: '#fff',
            backgroundColor: 'rgba(220,220,220,0.2)',
            borderColor: 'rgba(220,220,220,1)',
            pointBackgroundColor: 'rgba(220,220,220,1)',
            pointBorderColor: '#fff',
            data: [randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor()]
        }
    ]
};

var options = {
        maintainAspectRatio: true,
        tooltips: {
            callbacks: {
                label: (item) = > `${item.yLabel}%`,
        },
    },
    legend
:
{
    display: false,
}
,
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
        yAxes
:
    [{
        gridLines: {
            display: false,
            color: '#03A5C5',
            lineWidth: 8,
        },
        ticks: {
            callback: function (value) {
                return Number(value).toFixed() + "%"
            },
            fontColor: "white",
            beginAtZero: true,
        }
    }]
}
}
;
var ctx = document.getElementById('br-chart');
var chart = new Chart(ctx, {
    responsive: true,
    type: 'line',
    data: lineChartData,
    options: options
});


var randomScalingFactor = function () {
    return Math.round(Math.random() * 90)
};
var lineChartData = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    datasets: [
        {
            label: 'Shopping cart abandonment rate',
            labelColor: '#fff',
            fontColor: '#fff',
            backgroundColor: 'rgba(220,220,220,0.2)',
            borderColor: 'rgba(220,220,220,1)',
            pointBackgroundColor: 'rgba(220,220,220,1)',
            pointBorderColor: '#fff',
            data: [randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor()]
        }
    ]
};

var options = {
        maintainAspectRatio: true,
        tooltips: {
            callbacks: {
                label: (item) = > `${item.yLabel}%`,
        },
    },
    legend
:
{
    display: false,
}
,
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
        yAxes
:
    [{
        gridLines: {
            display: false,
            color: '#03A5C5',
            lineWidth: 8,
        },
        ticks: {
            callback: function (value) {
                return Number(value).toFixed() + "%"
            },
            fontColor: "white",
            beginAtZero: true,
        }
    }]
}
}
;
var ctx = document.getElementById('scar-chart');
var chart = new Chart(ctx, {
    responsive: true,
    type: 'line',
    data: lineChartData,
    options: options
});


var randomScalingFactor = function () {
    return Math.round(Math.random() * 3000)
};
var lineChartData = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    datasets: [
        {
            label: 'Traffic',
            labelColor: '#fff',
            fontColor: '#fff',
            backgroundColor: 'rgba(220,220,220,0.2)',
            borderColor: 'rgba(220,220,220,1)',
            pointBackgroundColor: 'rgba(220,220,220,1)',
            pointBorderColor: '#fff',
            data: [randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor()]
        }
    ]
};

var options = {
        maintainAspectRatio: true,
        tooltips: {
            callbacks: {
                label: (item) = > `${item.yLabel} visitors`,
        },
    },
    legend
:
{
    display: false,
}
,
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
        yAxes
:
    [{
        gridLines: {
            display: false,
            color: '#03A5C5',
            lineWidth: 8,
        },
        ticks: {
            fontColor: "white",
            beginAtZero: true,
        },
    }]
}
}
;
var ctx = document.getElementById('traffic-chart');
var chart = new Chart(ctx, {
    responsive: true,
    type: 'line',
    data: lineChartData,
    options: options,
});







