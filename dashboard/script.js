const API_BASE = 'http://127.0.0.1:8000';

// Color palette for protocols
const colors = [
    '#74b9ff', '#a29bfe', '#fd79a8', '#ffeaa7', '#55efc4',
    '#81ecec', '#fab1a0', '#ff7675', '#dfe6e9', '#b2bec3'
];

let protocolChart = null;

// Initialize Chart
function initChart() {
    const ctx = document.getElementById('protocolChart').getContext('2d');
    protocolChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: [],
            datasets: [{
                data: [],
                backgroundColor: colors,
                borderWidth: 0,
                hoverOffset: 10
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right',
                    labels: {
                        color: '#fff',
                        padding: 15,
                        font: { size: 12 }
                    }
                }
            },
            cutout: '60%'
        }
    });
}

// Update stats
async function fetchStats() {
    try {
        const response = await fetch(`${API_BASE}/stats`);
        const data = await response.json();
        
        // Update status
        document.getElementById('status-badge').className = 'status-badge online';
        document.getElementById('status-text').textContent = 'System Active';
        
        // Update packet count
        document.getElementById('total-packets').textContent = 
            data.total_packets.toLocaleString();
        
        // Update protocols
        const protocols = data.protocols;
        const protocolNames = Object.keys(protocols);
        const protocolValues = Object.values(protocols);
        
        document.getElementById('total-protocols').textContent = protocolNames.length;
        
        // Update chart
        if (protocolChart) {
            protocolChart.data.labels = protocolNames;
            protocolChart.data.datasets[0].data = protocolValues;
            protocolChart.update('none');
        }
        
        // Update protocol list
        updateProtocolList(protocols);
        
    } catch (error) {
        document.getElementById('status-badge').className = 'status-badge offline';
        document.getElementById('status-text').textContent = 'Connection Lost';
    }
}

// Update protocol bar list
function updateProtocolList(protocols) {
    const container = document.getElementById('protocol-list');
    const total = Object.values(protocols).reduce((a, b) => a + b, 0);
    
    if (total === 0) {
        container.innerHTML = '<div style="text-align: center; color: rgba(255,255,255,0.5); padding: 20px;">No data yet</div>';
        return;
    }
    
    const sorted = Object.entries(protocols)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 5);
    
    container.innerHTML = sorted.map(([name, count], i) => {
        const percent = ((count / total) * 100).toFixed(1);
        return `
            <div class="protocol-item">
                <span class="name">${name}</span>
                <div class="bar-container">
                    <div class="bar" style="width: ${percent}%; background: ${colors[i % colors.length]}">
                        ${percent}%
                    </div>
                </div>
            </div>
        `;
    }).join('');
}

// Fetch alerts
async function fetchAlerts() {
    try {
        const response = await fetch(`${API_BASE}/alerts`);
        const alerts = await response.json();
        
        document.getElementById('total-alerts').textContent = alerts.length;
        document.getElementById('alert-count').textContent = `${alerts.length} alert${alerts.length !== 1 ? 's' : ''}`;
        
        const container = document.getElementById('alerts-list');
        
        if (alerts.length === 0) {
            container.innerHTML = '<div class="no-alerts">No alerts detected<br><small>System is secure</small></div>';
            return;
        }
        
        container.innerHTML = alerts.slice(-20).reverse().map(alert => `
            <div class="alert-item">
                <div class="alert-type">${alert.type}</div>
                <div class="alert-details">
                    <span>🌐 ${alert.src_ip}</span>
                    <span>📡 ${alert.protocol}</span>
                </div>
            </div>
        `).join('');
        
    } catch (error) {
        console.error('Failed to fetch alerts:', error);
    }
}

// Update timestamp
function updateTimestamp() {
    const now = new Date();
    document.getElementById('last-update').textContent = now.toLocaleTimeString();
}

// Initialize and start polling
document.addEventListener('DOMContentLoaded', () => {
    initChart();
    
    // Initial fetch
    fetchStats();
    fetchAlerts();
    updateTimestamp();
    
    // Poll every 2 seconds
    setInterval(() => {
        fetchStats();
        fetchAlerts();
        updateTimestamp();
    }, 2000);
});
