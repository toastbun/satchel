import json


class ModelEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__