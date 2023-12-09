import logging

def try_get(func, default=None,return_exception=False):
    res,err=try_gete(func,default)
    if return_exception and err is not None:
        return err
    return res

def try_gete(func, default=None):
    try:
        return func() or default,None
    except Exception as e :
        logging.exception(e)
        return default,e

def try_geta(arr,func,skip_none=True,default_element=None):
    res=[]
    for elem in arr:
        x=try_get(lambda :func(elem),default=default_element)
        if x is None and skip_none: continue
        res.append(x)
    return res
def safe_lambda(lambd, default=None):
    res,err=safe_lambdae(lambd,default)
    return res
def safe_lambdae(lambd, default=None):
    try:
        return lambd()
    except Exception:
        loger.exception('lambda error:')
        return default
def apply_to_list(lst, func, filter_func=None,return_all=True):
    return [item for item in [try_get(func) for item in lst if filter_func is None or filter_func(item)] if return_all or item is not None ]

