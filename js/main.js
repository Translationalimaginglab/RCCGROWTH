document.addEventListener('DOMContentLoaded', () => {
    const startBtn = document.getElementById('start-btn');
    const questionnaireForm = document.getElementById('questionnaire-form');
    const resultsDiv = document.getElementById('results');

    if (startBtn) {
        startBtn.addEventListener('click', () => {
            window.location.href = 'questionnaire.html';
        });
    }

    if (questionnaireForm) {
        questionnaireForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const formData = new FormData(questionnaireForm);

            // Print raw input data
            console.log("Raw form data:", Array.from(formData.entries()));

            const inputData = processFormData(formData);

            const modelResults = await runModel(inputData);

            localStorage.setItem('results', JSON.stringify(modelResults));
            window.location.replace('results.html'); // change this line
        });
    }

    if (resultsDiv) {
        const results = JSON.parse(localStorage.getItem('results'));
        displayResults(results);
    }
});

function processFormData(formData) {
    // Process the form data and prepare it for your model
    // Replace this with your specific implementation
    const inputData = [];
    formData.forEach((value, key) => {
        inputData.push(parseFloat(value));
    });
    return inputData;
}

async function runModel(inputData) {
    const response = await fetch('http://localhost:5000/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ input: inputData })
    });

    const data = await response.json();
    return data.prediction;
}

function displayResults(results) {
    // Display the results
    // Replace this with your specific implementation
    const resultsDiv = document.getElementById('results');
    const resultElement = document.createElement('p');

    if (results === 1) {
        resultElement.textContent = 'High growth rate';
    } else if (results === 0) {
        resultElement.textContent = 'Low growth rate';
    }
    resultsDiv.appendChild(resultElement);
}