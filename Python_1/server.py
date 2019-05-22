import socket
import threading
import multiprocessing
import os


def process_request(conn, addr):
    conn.settimeout(5)
    print("connected client", addr)
    with conn:
        while True:
            try:
                data = conn.recv(1024)
            except socket.timeout:
                print("close connection by timeout")

            if not data:
                break
            print(data.decode("utf8"))
            conn



def worker(sock):
    while True:
        conn, addr = sock.accept()
        print("pid", os.getpid())
        th = threading.Thread(target=process_request, args=(conn, addr))
        th.start()


if __name__ == '__main__':
    with socket.socket() as sock:
        sock.bind(("", 10001))
        sock.listen()

        workers_count = 3
        workers_list = [multiprocessing.Process(target=worker, args=(sock, ))
                        for _ in range(workers_count)]

        for w in workers_list:
            w.start()

        for w in workers_list:
            w.join()