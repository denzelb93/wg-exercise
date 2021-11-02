import os, sys
sys.path.append(
    os.path.abspath(
        os.path.join( __file__, '..')))
from constants import parseIndex, fileStat, response as resp

class GetController():
    def __init__(self, index):
        self.index = index
    
    def __call__(self):
        return self.__handle()
    
    def __handle(self):
        try:
            mountedPath = [__file__, '..', '..', 'user_files']

            if self.index:
                path, is_dir = parseIndex(self.index)
                path = os.path.join(*mountedPath, *path)
            else:
                path = os.path.join(*mountedPath)
                is_dir = True

            path = os.path.abspath(path)

            if is_dir:
                data = dict(files=[], directories=[])

                with os.scandir(path) as objects:
                    for obj in objects:
                        if obj.is_dir():
                            data['directories'].append(obj.name)
                        else:
                            report = dict(**fileStat(obj))
                            data['files'].append(report)
            else:
                data = dict(**fileStat(path))
                assert data['permissions'][0] != "d"

            return resp(200, data)
        except:
            return resp(404, dict(message="Item not found"))
        
        

        
        

    

        





