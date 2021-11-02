
class Result:
    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.testCases = []
        self.passed = 0
        self.failed = 0
        self.errors = {}
        self.body = ['status', 'body']
        self.data = ['file_name', 'owner', 'size', 'permissions']
        self.dirBody = ['directories', 'files']
        self.success_code = 200
        self.fail_code = 404

    def __checkDataSuccess(self, expected, data, errors):
        for key in expected:
            if not data.get(key):
                errors.append("Expected data '{0}'".format(key))

        return errors

    def checkSuccess(self, response, dirRequest=False):
        data = {}
        errors = []

        if response.status_code != self.success_code:
            errors.append("Expected status code {0}, got: {1}".format(
                self.success_code,
                response.status_code))
        else:
            result = response.json()
            for key in self.body:
                if not result.get(key):
                    errors.append("Expected response '{0}'".format(key))

            if result.get(self.body[1]):
                data = result[self.body[1]]

                if not dirRequest:
                    errors = self.__checkDataSuccess(self.data, data, errors)
                else:
                    prevErrCount = len(errors)
                    errors = self.__checkDataSuccess(self.dirBody, data, errors)
                    
                    if len(errors) == prevErrCount:
                        if not data[self.dirBody[0]]:
                            errors.append("Expected listed directory names")

                        for fileData in data[self.dirBody[1]]:
                            for key in self.data:
                                if not fileData.get(key):
                                    errors.append("Expected file data '{0}'".format(key))

        return data, errors
    
    
    def checkFail(self, response):
        errors = []

        if response.status_code != self.fail_code:
            errors.append("Expected status code {0}, got: {1}".format(
                self.success_code,
                response.status_code))

        return errors


    def collectResult(self, test_case, errors):
        if errors:
            self.failed += 1
            self.errors[test_case] = errors
        else:
            self.testCases.append(test_case)
            self.passed += 1

    def showResult(self):
        print('''\n%s -\n\tPASSED: %s\n\tFAILED: %s''' \
            % (self.endpoint, self.passed, self.failed))

        if self.errors:
            for testcase, error in self.errors.items():
                print('\n' + testcase)
                for e in error:
                    print('\t - ' + str(e))
        else:
            for tc in self.testCases:
                print('\n* ' + tc)

