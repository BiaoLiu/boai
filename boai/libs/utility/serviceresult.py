# coding:utf-8

service_result = {
    'data': None,
    'ruleviolations': []
}


class ServiceResult:
    def __init__(self, data=None):
        self.data = data
        self.ruleviolations = []

    @property
    def error_is_empty(self):
        return not len(self.ruleviolations)>0


class RuleViolation:
    def __init__(self, parameter_name, error_message):
        self.parameter_name = parameter_name
        self.error_message = error_message
