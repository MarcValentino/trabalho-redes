import pickle
import socket
import cv2
import struct
UDP_IP = "127.0.0.1"
UDP_PORT = 9999
MESSAGE = b"Hello, World!"
CHUNK_SIZE = 1024
print("UDP target IP: %s" % UDP_IP)
print("UDP target port: %s" % UDP_PORT)
print("message: %s" % MESSAGE)

# video = open('Aruanas.S01E01.720p.mp4', 'rb', CHUNK_SIZE)

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_STREAM) # UDP
hostName = socket.gethostname()
hostIp = socket.gethostbyname(hostName)
print("ENDEREÇO IP: ", hostIp)

socketAddress = ('', UDP_PORT)

sock.bind(socketAddress)

sock.listen(5)
print("ESCUTANDO")
# chunk = video.read(CHUNK_SIZE)

while True:
    clientSocket, address = sock.accept()
    print("CONEXÃO DE:", address)
    if clientSocket:
        videoCapture = cv2.VideoCapture('./arquivo.mp4')
        while videoCapture.isOpened():
            ret, frame = videoCapture.read()
            if ret:
                pickledFrame = pickle.dumps(frame)
                print("PICKLED FRAME:", pickledFrame)
                message = struct.pack("Q", len(pickledFrame))+pickledFrame
                clientSocket.sendall(message)
                cv2.imshow('TRANSIMITINDO', frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    clientSocket.close()

    # sock.sendto(chunk, (UDP_IP, UDP_PORT))
    # chunk = video.read(CHUNK_SIZE)