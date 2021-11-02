from flask import jsonify
from stat import filemode
from pwd import getpwuid
from os import stat

def response(status_code, body={}):
    response = jsonify(dict(
        body=body,
        status=status_code))
    response.status_code = status_code

    return response

def parseIndex(path):
    is_dir = True if path[len(path) - 1] == "/" else False
    path = [obj for obj in path.split('/') if obj]

    return path, is_dir

def fileStat(file_object):
    if isinstance(file_object, str):
        st = stat(file_object)
        pathList = file_object.split('/')

        if len(pathList) == 1:
            fileName = pathList[0]
        else:
            fileName = pathList[len(pathList) - 1]
    else:
        st = file_object.stat()
        fileName = file_object.name
        
    info = {}
    info['file_name'] = fileName
    info['owner'] = getpwuid(st.st_uid).pw_name
    info['size'] = st.st_size
    info['permissions'] = filemode(st.st_mode)
    
    return info
    
