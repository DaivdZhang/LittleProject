import socket
import threading
from queue import Queue


port_list = [x for x in range(1, 65536)]


def port_scan(target, port):
    flag = 0
    s_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s_tcp.settimeout(4)
    s_udp.settimeout(4)
    try:
        s_tcp.connect((target, port))
        s_tcp.close()
        flag += 1
    except socket.error:
        pass
    try:
        s_udp.connect((target, port))
        s_udp.close()
        flag += 2
    except socket.error:
        pass
    return flag


def producer():
    while True:
        try:
            work_queue.put(port_list.pop(0))
        except IndexError:
            break


def consumer(target):
    while work_queue.empty() is False:
        port = work_queue.get()
        try:
            flag = port_scan(target, port)
        finally:
            if flag == 1:
                print("%s:%s tcp" % (target, port), "is open")
            elif flag == 3:
                print("%s:%s tcp/udp" % (target, port), "is open")
            work_queue.task_done()


if __name__ == "__main__":
    target_host = input("input the host:\n")
    work_queue = Queue()
    producer_thread = threading.Thread(target=producer)
    producer_thread.start()
    consumer_threads = []
    for i in range(16):
        consumer_threads.append(threading.Thread(target=consumer, args=(target_host,)))
    for t in consumer_threads:
        t.setDaemon(True)
        t.start()
    work_queue.join()
