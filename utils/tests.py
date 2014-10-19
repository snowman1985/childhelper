from utils.serialization import *

def testjson_serialize():
    data = {"hehe1":"hehe1", "hehe2":"jeje2"}
    data = [{"hehe":"xxx","jeje":"yyy"},{"hehe":"xxx2","jeje":"yyy2"}]
    ret = json_serialize("OK", "hehe")
    print(ret)
    
testjson_serialize()
 