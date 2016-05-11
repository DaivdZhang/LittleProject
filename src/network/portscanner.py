import socket
import threading
from multiprocessing import Pool
from queue import Queue
import os
import time


def port_scan(target, port):
    flag = 0
    s_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s_tcp.settimeout(2)
    s_udp.settimeout(2)
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


def data_producer(q, ports):
    while True:
        try:
            q.put(ports.pop(0))
        except IndexError:
            break


def data_consumer(target, q):
    while q.empty() is False:
        port = q.get()
        try:
            flag = port_scan(target, port)
        finally:
            if flag == 1:
                print("%s:%s tcp" % (target, port), "is open")
            elif flag == 3:
                print("%s:%s tcp/udp" % (target, port), "is open")
            q.task_done()


def work(port_list, target, cpus):
    # put the data into the queue
    work_queue = Queue()
    data_producer(q=work_queue, ports=port_list)
    # create thread pool according to the number of cpus
    threads = []
    for i in range(1, cpus+1):
        threads.append(threading.Thread(target=data_consumer, args=(target, work_queue)))
    for t in threads:
        t.setDaemon(True)
        t.start()
    work_queue.join()


if __name__ == "__main__":
    target_host = input("input the host>")
    cpu_num = os.cpu_count()
    task = [x for x in range(1, 1024)]
    temp = []
    n = len(task)//cpu_num+1
    for j in range(cpu_num):
        temp.append(task[j*n:(j+1)*n])
    # create the process pool
    process_pool = Pool(cpu_num)
    for j in range(1, cpu_num+1):
        process_pool.apply_async(func=work, args=(temp.pop(0), target_host, cpu_num))
    process_pool.close()
    t0 = time.time()
    process_pool.join()
    t1 = time.time()
    print("cost %.3fs" % (t1-t0))
