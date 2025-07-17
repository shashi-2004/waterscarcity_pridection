document.getElementById('predictionForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    // User inputs collect chesa
    const city = document.getElementById('city').value;
    const rainfall = parseFloat(document.getElementById('rainfall').value);
    const population = parseFloat(document.getElementById('population').value);
    const demand = parseFloat(document.getElementById('demand').value);
    const reservoir = parseFloat(document.getElementById('reservoir').value);
    const groundwater = parseFloat(document.getElementById('groundwater').value);
    const temperature = parseFloat(document.getElementById('temperature').value);
    const year = parseInt(document.getElementById('year').value);

    // Validation - inputs empty unte skip
    if (!city || isNaN(rainfall) || isNaN(population) || isNaN(demand) || 
        isNaN(reservoir) || isNaN(groundwater) || isNaN(temperature) || isNaN(year)) {
        alert('Please fill all fields with valid numbers!');
        return;
    }

    // Input data array banavali
    const input_data = [rainfall, population, demand, reservoir, groundwater, temperature];

    // Backend ki data send chestunnam
    const response = await fetch('http://127.0.0.1:5000/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ city, input_data, year })
    });

    const result = await response.json();
    const resultDiv = document.getElementById('result');
    resultDiv.style.display = 'block';
    resultDiv.innerHTML = `${year} ${city} Scarcity Prediction: ${result.prediction.toFixed(2)}%`;
});
