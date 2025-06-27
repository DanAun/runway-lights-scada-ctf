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
        const statusElement = document.getElementById('status-RWY-01');
        const state = data.runway_lights_state;

        if (typeof state === 'boolean') {
            if (state) {
                statusElement.textContent = 'ON';
                statusElement.className = 'status-on';
            } else {
                statusElement.textContent = 'OFF';
                statusElement.className = 'status-off';
            }
        } else if (typeof state === 'string') {
            statusElement.textContent = state;
            statusElement.className = 'status-flag';
            const alarmCell = document.querySelector('td.alarm');
            if (alarmCell) {
            alarmCell.textContent = '—';
            alarmCell.classList.remove('alarm');
            }

        } else {
            statusElement.textContent = 'UNKNOWN';
            statusElement.className = 'error';
}
    })
    .catch(err => console.error('Status fetch failed:', err));
}

fetchStatus();
setInterval(fetchStatus, 3000);