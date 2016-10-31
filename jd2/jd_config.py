# -*- coding: utf-8 -*-

# 开启睡眠
is_sleep = False
# 单个任务最小睡眠时间(单位:秒)
sleep_time_min = 5
# 单个任务最大睡眠时间(单位:秒)
sleep_time_max = 10

# 任务线程数
thread_num = 10

# 结果保存路径
result_save_path = '/Users/Lan/TestDir/jd_20161031.txt'
# 运行结果日志
log_save_path = '/Users/Lan/TestDir/jd_20161031_log.txt'

# redis任务表
redis_task_key = 'jd_20161031'
# redis成功与失败记录表
redis_succeed_count_key = 'jd_20161031_succeed'
# redis成功与失败记录表
redis_failed_count_key = 'jd_20161031_failed'
