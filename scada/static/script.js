function toggleLights(action) {
    fetch('/toggle', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: `action=${action}`
    }).then(res => res.json()).then(data => {
        if (data.status === 'success') {
            fetchStatus();
        } else {
            alert(data.message || 'Error');
        }
    });
}

function fetchStatus() {
    fetch('/status')
    .then(response => response.json())
    .then(data => {
        const statusElement = document.getElementById('runway_lights_state');
        if (data.runway_lights_state) {
        statusElement.textContent = 'ON';
        statusElement.className = 'status-on';
        } else {
        statusElement.textContent = 'OFF';
        statusElement.className = 'status-off';
        }
    })
    .catch(err => console.error('Status fetch failed:', err));
}

fetchStatus();
setInterval(fetchStatus, 3000);