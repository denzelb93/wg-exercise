import os, sys
import requests as req
from result import Result

class GetControllerTest(Result):
    def __init__(self):
        super().__init__("GetController")
        self.host = "http://localhost"
    
    def getFile(self):
        def getFileSuccess():
            def rootPath():
                filename = 'testfile.txt'
                res = req.get('{0}/{1}'.format(self.host, filename))
                data, errors = self.checkSuccess(res)
                
                if data and data.get('file_name') != filename:
                    errors.append("Expected data file_name '{0}', got: {1}".format(
                        filename,
                        data.get('file_name')))

                self.collectResult("Get file information from root file path", errors)
            
            def directoryPath():
                filename = 'dirfile0.txt'
                filepath = 'testdir/dirfile0.txt'
                res = req.get('{0}/{1}'.format(self.host, filepath))
                data, errors = self.checkSuccess(res)

                if data and data.get('file_name') != filename:
                    errors.append("Eexpected data file_name '{0}', got: {1}".format(
                        filename,
                        data.get('file_name')))

                self.collectResult("Get file information from directory file path", errors)

            return rootPath(), directoryPath()
            
        def getFileFail():
            filename = 'notfound.txt'
            res = req.get('{0}/{1}'.format(self.host, filename))
            errors = self.checkFail(res)
            
            self.collectResult("Cannot get information of a file that doesn't exist", errors)
        
        return getFileSuccess(), getFileFail()
    
    def getFolder(self):
        def getFolderSuccess():
            def rootPath():
                res = req.get('{0}/'.format(self.host))
                data, errors = self.checkSuccess(res, True)

                self.collectResult("List all items in a 'root' directory", errors)
            
            def directoryPath():
                dirname = 'testdir/'
                res = req.get('{0}/{1}'.format(self.host, dirname))
                data, errors = self.checkSuccess(res, True)

                self.collectResult("List all items in a specific directory", errors)
            
            return rootPath(), directoryPath()
        
        def getFolderFail():
            dirname = 'notfound_testdir/'
            res = req.get('{0}/{1}'.format(self.host, dirname))
            errors = self.checkFail(res)

            self.collectResult("Cannot list contents of a folder that doesn't exist", errors)
    
        return getFolderSuccess(), getFolderFail()

test = GetControllerTest()
test.getFile()
test.getFolder()
test.showResult()
