document.getElementById('device-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const description = document.getElementById('device-description').value;
    const data = { description: description };

    document.getElementById('loading-message-json').style.display = 'block';

    fetch('/api/device', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => {
        document.getElementById('loading-message-json').style.display = 'none';
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log("Device API Response:", data);
        document.getElementById('json-output').innerHTML = JSON.stringify(data, null, 2);
    })
    .catch((error) => {
        console.error('Error:', error);
        document.getElementById('json-output').innerHTML = `Error: ${error.message}`;
        document.getElementById('loading-message-json').style.display = 'none';
    });
});

let responseCounter = 0;

function createHazardBlock(hazard, responseId) {
    const hazardBlock = document.createElement('div');
    hazardBlock.classList.add('card', 'mb-3', 'hazard-block');
    hazardBlock.innerHTML = `
        <div class="card-body">
            <p><strong>Hazard:</strong> <input type="text" class="hazard-value form-control" value="${hazard.hazard || ''}"></p>
            <p><strong>Type:</strong> <input type="text" class="type-value form-control" value="${hazard.type || ''}"></p>
            <p><strong>Description:</strong> <textarea class="description-value form-control">${hazard.description || ''}</textarea></p>
            <p><strong>Detection Method:</strong> <textarea class="detection-method-value form-control">${hazard.detection_method || ''}</textarea></p>
            <p><strong>Mitigation Measure:</strong> <textarea class="mitigation-measure-value form-control">${hazard.mitigation_measure || ''}</textarea></p>
            <p><strong>Severity:</strong><input type="number" class="severity form-control" placeholder="Severity (0-1)" step="0.01" min="0" max="1" value="${hazard.severity || ''}"></p>
            <p><strong>Probability:</strong><input type="number" class="probability form-control" placeholder="Probability (0-1)" step="0.01" min="0" max="1" value="${hazard.probability || ''}"></p>
            <p><strong>Risk:</strong>
            <select class="risk form-control" name="risk">
                <option value="" selected disabled>Select Risk Level</option>
                <option value="SIL1" ${hazard.risk === 'SIL1' ? 'selected' : ''}>SIL1</option>
                <option value="SIL2" ${hazard.risk === 'SIL2' ? 'selected' : ''}>SIL2</option>
                <option value="SIL3" ${hazard.risk === 'SIL3' ? 'selected' : ''}>SIL3</option>
                <option value="SIL4" ${hazard.risk === 'SIL4' ? 'selected' : ''}>SIL4</option>
            </select></p>
        </div>
    `;
    document.getElementById(`hazard-content-${responseId}`).appendChild(hazardBlock);
    console.log(`Created hazard block for response ${responseId}:`, hazard);
}

function createResponseBlock(hazards, componentId) {
    const responseId = `response-${responseCounter}`;
    const responseBlock = document.createElement('div');
    responseBlock.classList.add('card', 'mb-3');
    responseBlock.id = responseId; // Ensure the response block has the correct ID
    responseBlock.innerHTML = `
        <div class="card-body">
            <h4 class="card-title">Hazard Analysis Response #${responseCounter + 1}</h4>
            <div id="hazard-content-${responseId}"></div>
            <button class="btn btn-primary mt-2" onclick="saveBestResponse(${componentId}, ${responseCounter})">Save Best Hazard Analysis Response</button>
        </div>
    `;
    document.getElementById(`hazard-output-${componentId}`).appendChild(responseBlock);

    hazards.forEach(hazard => createHazardBlock(hazard, responseId));
    console.log(`Created response block ${responseId} for component ${componentId} with hazards:`, hazards);

    responseCounter++;  // Increment the counter after creating the response block
}

function generateHazard(componentId) {
    const data = { component_id: componentId };

    fetch('/api/generate_hazard', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => { throw new Error(err.error); });
        }
        return response.json();
    })
    .then(data => {
        console.log("Generated Hazard Data:", data);
        if (data.hazards && Array.isArray(data.hazards)) {
            const hazards = JSON.parse(data.hazards[0].description.replace(/```json|```/g, '').trim());
            createResponseBlock(hazards, componentId);
        } else {
            console.error("Unexpected response format:", data);
            const hazardContent = document.getElementById(`hazard-content-${componentId}`);
            hazardContent.innerHTML = `<p class="text-danger">Unexpected response format: ${JSON.stringify(data)}</p>`;
        }
    })
    .catch((error) => {
        console.error('Error:', error);
        const hazardContent = document.getElementById(`hazard-content-${componentId}`);
        hazardContent.innerHTML = `<p class="text-danger">${error.message}</p>`;
    });
}

function saveBestResponse(componentId, responseIndex) {
    const responseId = `response-${responseIndex}`;
    const responseBlock = document.getElementById(responseId);
    if (!responseBlock) {
        console.error('Response block not found:', responseId);
        return;
    }
    const hazardBlocks = responseBlock.querySelectorAll('.hazard-block');

    console.log(`Found ${hazardBlocks.length} hazard blocks in response ${responseId}`);

    const bestResponse = Array.from(hazardBlocks).map((block, index) => {
        const severity = block.querySelector('.severity').value;
        const probability = block.querySelector('.probability').value;
        const risk = block.querySelector('.risk').value;

        const hazardData = {
            hazard: block.querySelector('.hazard-value').value.trim(),
            type: block.querySelector('.type-value').value.trim(),
            description: block.querySelector('.description-value').value.trim(),
            detection_method: block.querySelector('.detection-method-value').value.trim(),
            mitigation_measure: block.querySelector('.mitigation-measure-value').value.trim(),
            severity: severity || undefined,
            probability: probability || undefined,
            risk: risk || undefined
        };

        // Remove undefined keys
        Object.keys(hazardData).forEach(key => hazardData[key] === undefined && delete hazardData[key]);

        console.log(`Processed hazard block ${index} for response ${responseId}:`, hazardData);
        return hazardData;
    });

    const data = {
        component_id: componentId,
        best_response_index: responseIndex,
        best_response: bestResponse
    };

    console.log(`Data to be sent to the server:`, JSON.stringify(data));

    fetch('/api/save_best_hazard', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => { throw new Error(err.error); });
        }
        return response.json();
    })
    .then(data => {
        console.log("Saved Best Hazard Data:", data);
        alert('Best hazard analysis response saved successfully.');
        // Optional: Reset form and responses if needed
        // resetFormAndResponses();
    })
    .catch((error) => {
        console.error('Error:', error);
        alert(`Failed to save best hazard analysis response: ${error.message}`);
    });
}

function resetFormAndResponses() {
    document.getElementById('device-form').reset();
    document.getElementById('hazard-output-1').innerHTML = '';
    responseCounter = 0;
    console.log('Form and responses have been reset.');
}

function deleteItem(url) {
    fetch(url, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert(data.message);
            location.reload();
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}
