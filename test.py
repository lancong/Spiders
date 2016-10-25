def hello():
    return 'lan', 'luo'


if __name__ == '__main__':
    # result = 10 / 3
    # print(result)

    # for index in range(3):
    #     print(index)

    # names = ['lan1', 'lan2', 'lan3', 'lan4']
    names = ['lan1', 'lan2', 'lan3', 'lan4', 'lan5', 'lan6', 'lan7', 'lan8', 'lan9', 'lan10', 'lan11']

    # taskall = []
    # task = []
    #
    # count = 0
    #
    # for index in range(len(names)):
    #     task.append(names[index])
    #     count += 1
    #     if count == 3:
    #         taskall.append(task)
    #         task = []
    #         count = 0
    #
    # taskall.append(task)
    #
    # print(len(taskall))and len(tasklists) < threadnum - 1:
    #
    # for t in taskall:
    #     print(t)

    # import captureutil
    #
    # tasks = captureutil.dispatchtask(names, 3)
    #
    # for task in tasks:
    #     print(task)

    res = hello()
    print(type(res))

    print(res[0],res[1])
    pass
