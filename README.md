# NIDRS - Network Intrusion Detection and Response System

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.124-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

A real-time network intrusion detection system powered by machine learning. NIDRS captures live network traffic, analyzes it using an Isolation Forest anomaly detection model, and provides a web-based dashboard for monitoring and alerting.

## 🌟 Features

- **Real-time Packet Capture** - Live network traffic monitoring using PyShark/Wireshark
- **ML-based Anomaly Detection** - Isolation Forest algorithm to detect unusual network behavior
- **Attack Chain Detection** - Identifies multi-stage attacks (reconnaissance → exploitation → data exfiltration)
- **Alert Correlation** - Groups related alerts to reduce noise and identify patterns
- **Dynamic Alert Scoring** - Prioritizes alerts based on severity, frequency, and context
- **Log Ingestion** - Imports and analyzes external log files (Windows Event Logs, Syslog, etc.)
- **Web Dashboard** - Interactive React-based dashboard with real-time charts and statistics
- **REST API** - Full API for querying traffic data, alerts, and managing blocked IPs
- **IP Blocking** - Block suspicious IP addresses with automatic tracking

## 📁 Project Structure

```
NIDRS/
├── backend/
│   ├── main.py              # FastAPI application & API endpoints
│   ├── capture.py           # Network packet capture using PyShark
│   ├── detector.py          # ML anomaly detection (Isolation Forest)
│   ├── engine.py            # Main processing engine
│   ├── features.py          # Feature extraction from packets
│   ├── database.py          # SQLAlchemy models & database operations
│   ├── state.py             # In-memory state management
│   ├── response.py          # Response handling
│   ├── alert_scoring.py     # Dynamic alert priority scoring
│   ├── attack_chain.py      # Multi-stage attack detection
│   ├── correlation.py       # Alert correlation engine
│   └── log_ingestion.py     # External log file processing
├── dashboard-react/         # React-based dashboard
│   ├── src/
│   │   ├── App.js
│   │   └── components/      # React components
│   └── build/               # Production build
├── data/
│   └── traffic.db           # SQLite database
├── test_attack.py           # Attack simulation for testing
├── benchmark_accuracy.py    # Detection accuracy benchmarking
├── requirements.txt         # Python dependencies
└── README.md
```

## 🚀 Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/HeetPatel8126/NIDRS.git
   cd NIDRS
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv env
   .\env\Scripts\Activate.ps1   # Windows
   source env/bin/activate       # Linux/macOS
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the server**
   ```bash
   uvicorn backend.main:app --reload
   ```

5. **Access the dashboard**
   - Dashboard: `http://localhost:8000`
   - API Docs: `http://localhost:8000/docs`

## 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/status` | GET | System status |
| `/stats` | GET | Live packet statistics |
| `/alerts` | GET | Get live alerts |
| `/api/alerts/correlated` | GET | Get correlated alert groups |
| `/api/attack-chains` | GET | Get detected attack chains |
| `/api/blocked-ips` | GET | List blocked IPs |
| `/api/block-ip/{ip}` | POST | Block an IP address |

## 🧪 Testing

Run the attack simulation to test detection:
```bash
python test_attack.py
```

Run accuracy benchmarks:
```bash
python benchmark_accuracy.py
```

## ⚠️ Requirements

- **Python 3.12+**
- **Wireshark** (with tshark) - [Download](https://www.wireshark.org/download.html)
- **Administrator Privileges** for packet capture

## 📝 License

This project is licensed under the MIT License.
