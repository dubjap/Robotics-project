import socket
from sense_hat import SenseHat
import pickle
import struct

print("start")

#create the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
s.bind(('0.0.0.0',9395))
s.listen(10)


sense = SenseHat()




def send(s, data):
    data= pickle.dumps(data)
    s.sendall(struct.pack('>i',len(data)))
    s.sendall(data)


def recv(s):
    data = s.recv(4, socket.MSG_WAITALL)
    data_len = struct.unpack('>i', data)[0]
    data = s.recv(data_len, socket.MSG_WAITALL)
    return pickle.loads(data)
    



while True:
    #accept a client
    conn,addr = s.accept()
    print("connected")
    #conn is now a "socket", if you write to it, the client receives that data
    #if you read from it, you get what the client sent you
    acc = sense.get_accelerometer_raw()
    gyr = sense.get_gyroscope_raw()

    myDict= {"acc" : acc, "gyr" : gyr}
    #Send
    send(conn,myDict)

    #Receive
    msg = recv(conn)
    print(msg)
    
    
    sense.clear()
    sense.set_pixel(int(msg[0]), int(msg[1]), 255, 0, 0)    
    
