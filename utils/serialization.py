import json

def json_serialize(status, result = {}):
    ret = {"status":status, "result":result}
    return json.dumps(ret, ensure_ascii=False)
