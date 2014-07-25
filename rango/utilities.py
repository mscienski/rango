__author__ = 'idfl'


def urlencoding(param):
    param = param.__str__()
    if '_' in param:
        return param.replace('_', ' ')
    elif ' ' in param:
        return param.replace(' ', '_')
    else:
        return param