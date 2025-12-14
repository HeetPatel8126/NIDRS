from collections import defaultdict
import time

traffic = defaultdict(lambda: {"count": 0, "bytes": 0, "start": time.time()})

def extract_features(packet):
    ip = packet["src_ip"]
    traffic[ip]["count"] += 1
    traffic[ip]["bytes"] += packet["length"]

    duration = time.time() - traffic[ip]["start"]
    rate = traffic[ip]["count"] / max(duration, 1)

    return [
        traffic[ip]["count"],   # packet count
        traffic[ip]["bytes"],   # total bytes
        rate                    # packets/sec
    ]
