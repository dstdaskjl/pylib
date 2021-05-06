import sys, inspect, psutil, os, pathlib, datetime

log_dir = str(pathlib.Path.home()) + '/Documents/memory_profile/'
if not os.path.isdir(log_dir):
    os.mkdir(log_dir)
filename = 'result.txt'
log_dir = log_dir + filename


process = psutil.Process(os.getpid())

def log_usage_diff(cls_name, func):
    def decorate(*args, **kwargs):
        old_usage = format(process.memory_info().rss / (1024 ** 2), '.4f')
        func_ret = func(*args, **kwargs)
        new_usage = format(process.memory_info().rss / (1024 ** 2), '.4f')
        if old_usage != new_usage:
            dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-2]
            log = '[' + dt + '] ' +  str(old_usage) + ' -> ' + str(new_usage) + ' ' + cls_name + ' ' + func.__name__ + '\n'
            with open(log_dir, 'a') as outfile:
                outfile.write(log)
        return func_ret
    return decorate

def apply_to_all():
    cls_members = inspect.getmembers(sys.modules[__name__], inspect.isclass)
    for cls_name, cls in cls_members:
        '''
        Add conditions to exclude the imported libraries
        '''
        func_members = inspect.getmembers(cls, inspect.isfunction)
        for func_name, func in func_members:
            if func_name in cls.__dict__:
                setattr(cls, func_name, log_usage_diff(cls_name, func))