import asyncio

async def tcp_echo_client(message, loop):
    reader, writer = await asyncio.open_connection("127.0.0.1", 10001, loop=loop)

    print("send: {0}".format(message))
    writer.write(message.encode())
    writer.close()
    print(reader.readuntil())


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    message = "Hello World!"
    loop.run_until_complete(tcp_echo_client(message, loop))
    loop.close()