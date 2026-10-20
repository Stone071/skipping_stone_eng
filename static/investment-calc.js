let chart;

// Only use 6 digit codes here. We append 2 digit opacity when 
// building the chart config.
const COLORS = [
"#007bff", // Blue
"#28a745", // Green
"#ebb103", // Yellow
"#dc3545", // Red
"#6610f2", // Purple
"#fd7e14", // Orange
];

function generateEras() {
    // Go get the eras container
    const numEras = parseInt(document.getElementById("num_eras").value);
    const container = document.getElementById("eras_container");

    // Cache the current values first
    const cached = {};
    const inputs = container.querySelectorAll(".era-box");
    inputs.forEach((div, i) => {
    cached[i] = {
        years: div.querySelector(`[name="years_${i}"]`)?.value,
        rate: div.querySelector(`[name="rate_${i}"]`)?.value,
        compound_freq: div.querySelector(`[name="compound_freq_${i}"]`)?.value,
        comp_freq_out: div.querySelector(`[name="comp_freq_out_${i}"]`)?.value,
        deposit: div.querySelector(`[name="deposit_${i}"]`)?.value,
        deposit_freq: div.querySelector(`[name="deposit_freq_${i}"]`)?.value,
        dep_freq_out: div.querySelector(`[name="dep_freq_out_${i}"]`)?.value
    };
    });
    
    // Clear and rebuild the container
    container.innerHTML = "";

    // Create the inputs and reused cached values if available
    for (let i = 0; i < numEras; i++) {
        const box = document.createElement("div");
        box.className = "era-box";
        box.style.backgroundColor = COLORS[i % COLORS.length];

        const default_era = { years:5, rate:5, compound_freq:1, 
            comp_freq_out:"Yearly", deposit:1000, deposit_freq:12, dep_freq_out:"Monthly"};

        const era = ((cached[i] == undefined) ? default_era : cached[i]);

        box.innerHTML = `
            <h3>Era ${i + 1}</h3>
            <label>Years:</label>
            <input type="number" name="years_${i}" step="1" value="${era.years}">
            <label>Interest Rate (%):</label>
            <input type="number" name="rate_${i}" step="0.1" value="${era.rate}">
            <label>Compounding Frequency:</label>
            <input type="range" min=1 max=12 step=11 class=freq_sel value=${era.compound_freq} name="compound_freq_${i}">
            <input type="text" name="comp_freq_out_${i}" value="${era.comp_freq_out}" readonly>
            <label>Deposit ($):</label>
            <input type="number" name="deposit_${i}" step="100" value="${era.deposit}">
            <label>Deposit Frequency:</label>
            <input type="range" min=1 max=12 step=11 class=freq_sel value=${era.deposit_freq} name="deposit_freq_${i}">
            <input type="text" name="dep_freq_out_${i}" value="${era.dep_freq_out}" readonly>

        `;
        container.appendChild(box);
    }
}

// Behavior for changing num_eras
document.getElementById("num_eras").addEventListener("change", () => {
    const inputHandle = document.getElementById("num_eras");
    const num = parseInt(inputHandle.value);
    // Range checking
    if (num > 6) {
    inputHandle.value = 6;
    }
    else if (num < 0) {
    inputHandle.value = 0;
    }

    if (!isNaN(num)) {
    // Generate the new div
    generateEras(num);
    // Calculate based on new era
    calculate();
    }
});

// Update chart any time the details in eras changes
document.getElementById("eras_container").addEventListener("change", () => {
    //Input checking
    const eraBoxes = document.querySelectorAll(".era-box");
    const eras = Array.from(eraBoxes).map(box => {
    const inputs = box.querySelectorAll("input");
    // Years must be positive and a number
    if (inputs[0].value < 0 || isNaN(inputs[0].value))
    {
        inputs[0].value = 0;
    }
    // Interest rate must be a number
    if (isNaN(inputs[1].value))
    {
        inputs[1].value = 0;
    }
    // Compound Frequency
    (inputs[2].value == 1) ? inputs[3].value = "Yearly" : inputs[3].value = "Monthly";
    // Deposit
    if (isNaN(inputs[4].value))
    {
        inputs[4].value = 0;
    }
    // Deposit Frequency
    (inputs[5].value == 1) ? inputs[6].value = "Yearly" : inputs[6].value = "Monthly";
    });
    
    // Call calculate on the new data, which will then call updateChart
    calculate();
});

// Update chart if initial investment changes
document.getElementById("principal").addEventListener("change", () => {
    const inputHandle = document.getElementById("principal");
    const num = parseInt(inputHandle.value);
    // Input checking
    if (num > 10000000)
    {
    inputHandle.value = 10000000;
    }
    else if (num < 0)
    {
    inputHandle.value = 0;
    }

    if (!isNaN(num)) {
    calculate();
    } 
});

// Update the eras if the user clicks the "example" button
document.getElementById("example_button").addEventListener("click", () => {
    // Set initial investment to 0
    document.getElementById("principal").value = 0;
    // Get numEras and set the input
    const numErasHandle = document.getElementById("num_eras");
    numErasHandle.value = 3;
    const numEras = numErasHandle.value;

    // Go get the eras container
    const container = document.getElementById("eras_container");
    // Give example values
    const example_values = [
        {
            years: 25,
            rate: 10,
            compound_freq: 1, 
            comp_freq_out: 'Yearly',
            deposit: 1500,
            deposit_freq: 12,
            dep_freq_out: 'Monthly'
        },
        {
            years: 5,
            rate: 8,
            compound_freq: 1, 
            comp_freq_out: 'Yearly',
            deposit: 3000,
            deposit_freq: 12,
            dep_freq_out: 'Monthly'
        },        
        {
            years: 30,
            rate: 4.5,
            compound_freq: 12, 
            comp_freq_out: 'Monthly',
            deposit: -10000,
            deposit_freq: 12,
            dep_freq_out: 'Monthly'
        },
    ];

    // Clear and rebuild the container
    container.innerHTML = "";

    // Create the inputs and reused cached values if available
    for (let i = 0; i < numEras; i++) {
        const box = document.createElement("div");
        box.className = "era-box";
        box.style.backgroundColor = COLORS[i % COLORS.length];
        // Make the eras using the example values
        const era = example_values[i];

        box.innerHTML = `
            <h3>Era ${i + 1}</h3>
            <label>Years:</label>
            <input type="number" name="years_${i}" step="1" value="${era.years}">
            <label>Interest Rate (%):</label>
            <input type="number" name="rate_${i}" step="0.1" value="${era.rate}">
            <label>Compounding Frequency:</label>
            <input type="range" min=1 max=12 step=11 class=freq_sel value=${era.compound_freq} name="compound_freq_${i}">
            <input type="text" name="comp_freq_out_${i}" value="${era.comp_freq_out}" readonly>
            <label>Deposit ($):</label>
            <input type="number" name="deposit_${i}" step="100" value="${era.deposit}">
            <label>Deposit Frequency:</label>
            <input type="range" min=1 max=12 step=11 class=freq_sel value=${era.deposit_freq} name="deposit_freq_${i}">
            <input type="text" name="dep_freq_out_${i}" value="${era.dep_freq_out}" readonly>

        `;
        container.appendChild(box);
    }

    // Now recalc
    calculate();
});


async function calculate() {
    const principal = parseFloat(document.getElementById("principal").value);
    const eraBoxes = document.querySelectorAll(".era-box");
    const eras = Array.from(eraBoxes).map(box => {
    const inputs = box.querySelectorAll("input");
    return {
        years: inputs[0].value,
        rate: inputs[1].value,
        compound_freq: inputs[2].value,
        // inputs[3] is the text only "Monthly" or "Yearly"
        deposit: inputs[4].value,
        deposit_freq: inputs[5].value
        // inputs[6] is the same
    };
    });

    const res = await fetch("/calculate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ principal, eras })
    });

    const data = await res.json();
    document.getElementById("summary").innerText = 
    `Final Value: $${data.final_value.toLocaleString('currency')} — Total Gain: $${data.total_gain.toLocaleString('currency')}`;

    updateChart(data);
}

function updateChart(data) {
    // X axis labels
    const labels = data.time;

    // Build a dataset for each era
    const datasets = data.eras.map((era, i) => ({
        label: `Era ${i + 1}`,
        data: era.balance,
        borderColor: COLORS[i % COLORS.length],
        backgroundColor: COLORS[i % COLORS.length] + '33', // Transparent fill
        fill: true,
        tension: 0.4,
        pointRadius: 3,
        pointHoverRadius: 5
    }));

    const chartData = {
    labels: labels,
    datasets: datasets
    };

    const config = {
        type: 'line',
        data: chartData,
        options: {
            responsive: true,
            plugins: {
            legend: {
                position: 'top',
                display: false,
                labels: {
                    color: '#000000', // legend text color
                    font: {
                    size: 16,       // legend font size
                    weight: 'bold'  // bold for visibility
                    }
                }
            },
            // title: {
            //   display: true,
            //   text: 'Balance Over Time',
            //   font: {
            //     size: 32
            //   },
            //   color: '#000000',
            // }
            },
            scales: {
            x: {
                title: {
                    display: true,
                    text: 'Years from now',
                    color: '#000000',
                    font:{
                        size: 16,
                    },
                },
                ticks: {
                    color: '#000000', // X axis label color
                    font: {
                        size: 14
                    }
                },
                grid: {
                    color: 'rgba(0,0,0,0.1)' // faint grid lines
                }
            },
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Balance ($)',
                    font:{
                        size: 16,
                    },
                    color: '#000000',
                },
                ticks: {
                    color: '#000000', // Y axis label color
                    font: {
                        size: 14
                    }
                },
                grid: {
                    color: 'rgba(0,0,0,0.1)' // faint grid lines
                }
            }
            }
        }
    };

    if (chart) {
        chart.destroy();
    }

    const ctx = document.getElementById("chart").getContext("2d");
    chart = new Chart(ctx, config);
}

// Initialize
generateEras();
calculate();