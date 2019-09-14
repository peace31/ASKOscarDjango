var doughnutData = {
    labels: [
        'Current',
        'Left',
    ],
    datasets: [{
        data: [300, 100],
        backgroundColor: [
            '#FF6384',
            '#36A2EB',
        ],
        hoverBackgroundColor: [
            '#FF6384',
            '#36A2EB',
        ]
    }]
};

var options = {
    responsive: true,
    legend: {
        display: false
    },
    elements: {
        arc: {
            borderWidth: 0
        }
    }


};


var ctx = document.getElementById('canvas-3');
var chart = new Chart(ctx, {
    type: 'doughnut',
    data: doughnutData,
    options: options
});
