let inventoryChartInstance = null;
let stockChartInstance = null;
let repairChartInstance = null;
document.addEventListener(
    "DOMContentLoaded",
    function () {
        initializeDashboard();
    }
);
/*INITIALIZE DASHBOARD*/
function initializeDashboard() {
    if (
        typeof Chart === "undefined"
    ) {
        console.error(
            "Chart.js not loaded"
        );
        return;
    }
    loadDashboardCharts();
}
/*LOAD CHARTS*/
function loadDashboardCharts() {
    initializeInventoryChart();
    initializeStockChart();
    initializeRepairChart();
}
/*DASHBOARD DATA*/
function getDashboardData() {
    const defaultData = {
        available: 0,
        installed: 0,
        reserved: 0,
        pulled_out: 0,
        repair: 0,
        disposal: 0,
        spare_parts: 0,
        consumables: 0,
        toner: 0,
        ink: 0,
        office_supplies: 0,
        repair_chart: []
    };
    return {
        ...defaultData,
        ...(window.dashboardData || {})
    };
}
/*DESTROY CHART*/
function destroyChart(chart) {
    if (chart) {
        chart.destroy();
    }
}
/*UNIT STATUS CHART*/
function initializeInventoryChart() {
    const canvas =
        document.getElementById(
            "inventoryChart"
        );
    if (!canvas)
        return;
    destroyChart(
        inventoryChartInstance
    );
    const data =
        getDashboardData();
    inventoryChartInstance =
        new Chart(
            canvas,
            {
                type: "bar",
                data: {
                    labels: [
                        "Available",
                        "Installed",
                        "Reserved",
                        "Pulled Out",
                        "Repair",
                        "Disposal"
                    ],
                    datasets: [{
                        label:
                            "Units",
                        data: [
                            data.available,
                            data.installed,
                            data.reserved,
                            data.pulled_out,
                            data.repair,
                            data.disposal
                        ]
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                precision: 0
                            }
                        }
                    }
                }
            }
        );
}
/*PARTS STOCK CHART*/
function initializeStockChart() {
    const canvas =
        document.getElementById(
            "stockChart"
        );
    if (!canvas)
        return;
    destroyChart(
        stockChartInstance
    );
    const data =
        getDashboardData();
    stockChartInstance =
        new Chart(
            canvas,
            {
                type: "doughnut",
                data: {
                    labels: [
                        "Spare Parts",
                        "Consumables",
                        "Toner",
                        "Ink",
                        "Office Supplies"
                    ],
                    datasets: [{
                        data: [
                            data.spare_parts,
                            data.consumables,
                            data.toner,
                            data.ink,
                            data.office_supplies
                        ]
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    cutout: "70%"
                }
            }
        );
}
/*REPAIR TREND*/
function initializeRepairChart() {
    const canvas =
        document.getElementById(
            "repairChart"
        );
    if (!canvas)
        return;
    destroyChart(
        repairChartInstance
    );
    const data =
        getDashboardData();
    let labels = [];
    let values = [];
    if (
        Array.isArray(
            data.repair_chart
        )
    ) {
        labels =
            data.repair_chart.map(
                item =>
                    item.month
            );
        values =
            data.repair_chart.map(
                item =>
                    item.value
            );
    }
    repairChartInstance =
        new Chart(
            canvas,
            {
                type: "line",
                data: {
                    labels: labels,
                    datasets: [{
                        label:
                            "Repair Requests",
                        data: values,
                        tension: .4,
                        fill: true
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false
                }
            }
        );
}
/*REFRESH SUPPORT*/
function refreshDashboardCharts() {
    initializeInventoryChart();
    initializeStockChart();
    initializeRepairChart();
}
window.addEventListener(
    "resize",
    function () {
        [
            inventoryChartInstance,
            stockChartInstance,
            repairChartInstance
        ].forEach(
            chart => {

                if (chart)
                    chart.resize();
            }
        );
    }
);
