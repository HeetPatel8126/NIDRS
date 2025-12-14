import pyshark
import asyncio

pyshark.tshark.tshark_path = r"C:\Program Files\Wireshark\tshark.exe"
INTERFACE = "Wi-Fi"

def packet_stream():
    # Create a new event loop for this thread (required by pyshark)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    capture = pyshark.LiveCapture(interface=INTERFACE)
    try:
        for packet in capture.sniff_continuously():
            try:
                yield {
                    "src_ip": packet.ip.src,
                    "dst_ip": packet.ip.dst,
                    "protocol": packet.highest_layer,
                    "length": int(packet.length)
                }
            except:
                continue
    except GeneratorExit:
        pass
    finally:
        capture.close()
