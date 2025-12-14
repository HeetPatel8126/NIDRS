from backend.capture import packet_stream
from backend.state import stats
from backend.detector import process
from backend.features import extract_features
from backend.database import get_session, save_traffic, save_alert
import json


def start_engine():
    print("[ENGINE] Started")
    
    session = get_session()
    batch_count = 0
    BATCH_SIZE = 100  # Commit every 100 packets for efficiency

    try:
        for packet in packet_stream():
            stats["total_packets"] += 1
            stats["protocols"][packet["protocol"]] += 1

            # Save traffic to database
            save_traffic(session, packet)
            batch_count += 1

            features = extract_features(packet)
            result = process(features)

            if result == "ANOMALY":
                alert_data = {
                    "type": "ML_ANOMALY",
                    "severity": "high",
                    "src_ip": packet["src_ip"],
                    "dst_ip": packet.get("dst_ip"),
                    "protocol": packet["protocol"],
                    "description": f"Anomalous traffic detected from {packet['src_ip']}"
                }
                
                # Save alert to database
                save_alert(session, alert_data)
                
                # Also keep in memory for real-time dashboard
                stats["alerts"].append(alert_data)

            # Batch commit for performance
            if batch_count >= BATCH_SIZE:
                session.commit()
                batch_count = 0

    except KeyboardInterrupt:
        print("[ENGINE] Stopping...")
        session.commit()  # Final commit
        session.close()
        print("[ENGINE] Stopped")
