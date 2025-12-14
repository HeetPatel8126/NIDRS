from capture import packet_stream

print("Capture started")

for pkt in packet_stream():
    print(pkt)
    break

print("Capture stopped cleanly")
