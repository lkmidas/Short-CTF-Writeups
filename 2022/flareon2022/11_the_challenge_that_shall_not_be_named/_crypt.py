import inspect

frame = inspect.stack()[13].frame
c = frame.f_code

for idx, obj in enumerate(c.co_consts):
    #if inspect.iscode(obj):
    print(idx, obj)