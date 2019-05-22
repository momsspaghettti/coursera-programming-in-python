import socket
import time


class ClientError(Exception):
    pass


class ClientSocketError(ClientError):
    def __init__(self, text):
        self.text = text
        print(self.text)


class ClientProtocolError(ClientError):
    def __init__(self, text):
        self.text = text
        print(self.text)


class Client():

    def __init__(self, host, port, timeout=None):
        self.host = host
        self.port = port
        self.timeout = timeout

        try:
            self.connection = socket.create_connection((host, port), self.timeout)
        except socket.error:
            raise ClientSocketError("error create connection")

    def put(self, key, val, timestamp=None):
        if timestamp == None:
            timestamp = int(time.time())

        try:
            self.connection.sendall("put {0} {1} {2}\n".format(str(key), str(val), str(timestamp)).encode("utf8"))
        except socket.error:
            raise ClientSocketError("error sending")

        data = b""
        while not data.endswith(b"\n\n"):
            try:
                data += self.connection.recv(1024)
            except socket.error:
                raise ClientSocketError("error get data")

        if data.decode("utf8") == "error":
            raise ClientProtocolError("protocol error")

    def get(self, key):

        try:
            self.connection.sendall("get {0}\n".format(str(key)).encode("utf8"))
        except socket.error:
            raise ClientSocketError("error sending")

        data = b""
        while not data.endswith(b"\n\n"):
            try:
                data += self.connection.recv(1024)
            except socket.error:
                ClientSocketError("get data error")

        if data.decode("utf8") == "ok":
            return {}
        else:
            data_dict = {}
            data = data.decode("utf8")
            data = data[3:]
            data_arr = data.split("\n")

            for row in data_arr:
                if not row == "":
                    temp_mas = row.split(" ")
                    if temp_mas[0] in data_dict:
                        temp_tuple = (int(temp_mas[2]), float(temp_mas[1]))
                        data_dict[temp_mas[0]].append(temp_tuple)
                    else:
                        temp_tuple = (int(temp_mas[2]), float(temp_mas[1]))
                        data_dict[temp_mas[0]] = []
                        data_dict[temp_mas[0]].append(temp_tuple)

            return data_dict

    def close(self):
        try:
            self.connection.close()
        except socket.error:
            raise ClientSocketError("error closing connection")


if __name__ == '__main__':
    client = Client("127.0.0.1", 8181, timeout=5)
    client.put("test", 0.5, timestamp=1)
    client.put("test", 2.0, timestamp=2)
    client.put("test", 0.5, timestamp=3)
    client.put("load", 3, timestamp=4)
    client.put("load", 4, timestamp=5)
    print(client.get('*'))

    client.close()
