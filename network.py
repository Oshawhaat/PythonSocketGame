import os
import pickle
import socket
import glob


class Network:
    def __init__(self):
        self.client = socket.socket()
        self.server = "10.234.5.138" # "127.0.0.1"
        self.port = 9999
        self.address = (self.server, self.port)
        num_images, self.id = self.connect()
        print(self.id)

        try: os.mkdir("imgz")
        except FileExistsError: pass

        for file in glob.glob("imgz/*.*"):
            os.remove(file)

        for x in range(num_images):
            self.client.send(str.encode(f"ri{x}"))
            image = self.client.recv(4096000)
            self.client.send(str.encode(f"rn{x}"))
            image_name = self.client.recv(4096).decode()
            with open(f"imgz/{image_name}", "xb") as file:
                file.write(image)

    def connect(self):
        self.client.connect(self.address)
        ret = pickle.loads(self.client.recv(4096))
        print("Connected to server!")
        return ret

    def send(self, data):
        self.client.send(pickle.dumps(data))
        return pickle.loads(self.client.recv(4096))
