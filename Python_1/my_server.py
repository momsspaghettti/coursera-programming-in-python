import asyncio


def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        ClientServerProtocol,
        str(host), int(port)
    )

    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


class ClientServerProtocol(asyncio.Protocol):
    def __init__(self):
        self.transport = None

    data_dict = {}

    def connection_made(self, transport):
        self.transport = transport

    def process_data(self, message):
        command, data = str(message).split(" ", 1)

        if command == "put":
            data_arr = data.split("\n")

            for row in data_arr:
                if not row == "":
                    temp_mas = row.split(" ")
                    if temp_mas[0] in self.data_dict:
                        temp_tuple = (str(temp_mas[1]), str(temp_mas[2]))
                        if self.data_dict[temp_mas[0]].count(temp_tuple) == 0:
                            self.data_dict[temp_mas[0]].append(temp_tuple)
                    else:
                        temp_tuple = (str(temp_mas[1]), str(temp_mas[2]))
                        self.data_dict[temp_mas[0]] = [temp_tuple]

            return "ok\n\n"

        if command == "get":
            data = data[:-1]
            if data == "*":
                string = "ok\n"
                for key in self.data_dict:
                    for row in self.data_dict[key]:
                        string += "{0} {1}".format(key, ' '.join(row)) + "\n"
                return string + "\n\n"
            elif data in self.data_dict:
                string = "ok\n"
                for row in self.data_dict[data]:
                    string += "{0} {1}".format(data, ' '.join(row)) + "\n"
                return string + "\n"

            return "ok\n\n"

        return "error\nwrong command\n\n"

    def data_received(self, data):
        resp = self.process_data(data.decode("utf8"))
        self.transport.write(resp.encode("utf8"))


if __name__ == '__main__':
    run_server("127.0.0.1", 8888)