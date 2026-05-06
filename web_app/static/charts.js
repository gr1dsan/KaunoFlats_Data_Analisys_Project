function renderChart(onReady) {
    fetch(`/chart_data`)
    .then(response => response.json())
    .then(data => {

        // BAR CHART
        const ctxBar = document.getElementById('expensesChart').getContext('2d');
        if (instance) instance.destroy();
        instance = new Chart(ctxBar, {
            type: 'bar',
            data: {
                labels: ["Under 300 €", "300-600 €", "600-900 €", "900+ €"],
                    datasets: [{
                        data: [
                            data.under_300[0],
                            data.from_300_to_600[0],
                            data.from_600_to_900[0],
                            data.above_900[0]
                        ],
                    backgroundColor: '#89CFF0',
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: { display: false }, tooltip: { callbacks: {label: function(context) {return context.raw + ' %';}}}},
                scales: {
                    x: { grid: { display: false }, ticks: { display: false } },
                    y: { grid: { display: false }, ticks: { display: false } }
                },
                layout: { padding: 10 }
            }
        });

        // PIE CHART
        const ctxPie = document.getElementById('expensesPieChart').getContext('2d');
        new Chart(ctxPie, {
            type: 'pie',
            data: {
                labels: ['Modern buildings offers', 'Old buildings offers'],
                datasets: [{
                    data: [data.number_of_modern_builds[0], data.number_of_old_builds[0]],
                    backgroundColor: ['#89CFF0', '#FFB347'],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: { position: 'bottom' }, tooltip: { callbacks: {label: function(context) {return context.raw + ' %';}}}}
            }
        });

        if (typeof onReady === 'function') onReady();
    });
}