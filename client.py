import pickle
import socket
import struct
import cv2

UDP_IP = "127.0.0.1"
UDP_PORT = 9997

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_STREAM) # UDP
sock.connect(('', UDP_PORT))
data = b""
payloadSize = struct.calcsize("Q")
while True:
    while len(data) < payloadSize:
        packet = sock.recv(4096)
        if not packet: break
        data+=packet
    packedMessageSize = data[:payloadSize]
    data = data[payloadSize:]
    messageSize = struct.unpack("Q", packedMessageSize)[0]

    while len(data) < messageSize:
        data += sock.recv(4096)
    frameData = data[messageSize]
    data = data[messageSize]
    frame = pickle.loads(frameData)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('e'):
        break
sock.close()