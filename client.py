import pickle
import socket
import struct
import cv2

UDP_IP = "127.0.0.1"
UDP_PORT = 9999

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_STREAM) # UDP
sock.connect(('', UDP_PORT))
data = b""
payloadSize = struct.calcsize("Q")
print("PAYLOAD SIZE: ", payloadSize)
while True:
    print("DATA LENGTH:", len(data))
    while len(data) < payloadSize:
        packet = sock.recv(4 * 1024)
        # print("INCOMING PACKET:", packet)
        if not packet: break
        data+=packet
    print("Data", data)
    packedMessageSize = data[:payloadSize]
    # messageSize = float(packedMessageSize.decode())
    data = data[payloadSize:]
    messageSize = struct.unpack("Q", packedMessageSize)[0]

    while len(data) < messageSize:
        packet = sock.recv(4 * 1024)
        if not packet: break
        data += packet
    frameData = data[:messageSize]
    data = data[messageSize:]
    frame = pickle.loads(frameData)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('e'):
        break
sock.close()