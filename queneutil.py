# -*- coding: utf-8 -*-


import queue

if __name__ == '__main__':

    q = queue.Queue()

    for i in range(100):
        q.put(i)

    while not q.empty():
        print(q.get())
        q.task_done()
        print(q.get())
        q.task_done()
        print("size: " + str(q.qsize()))
    pass
