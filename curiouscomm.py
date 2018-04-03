import qlikevaluate as qe
import time
import json
import apiaiconn

def communicate(session_id,CLIENT_ACCESS_TOKEN,resp):
    raw = apiaiconn.getAction(session_id,CLIENT_ACCESS_TOKEN,resp)

    if len(raw["result"]["fulfillment"]["messages"]) > 0:
        fullfillment = raw["result"]["fulfillment"]["messages"][0]["speech"]
    else:
        fullfillment = raw["result"]["fulfillment"]["speech"]
    parameters = raw["result"]["parameters"]
    contexts = raw["result"]["contexts"]
    if len(raw["result"]["metadata"]) > 0:
        intentName = raw["result"]["metadata"]["intentName"]
    action = raw["result"]["action"].split(".")
    #print(action)
    res = "I don't understand"
    if action[0] == 'input':
        if action[1]=='unknown':
            res = fullfillment
        else:
            res = qe.evaluate(parameters)
    if action[0] == 'chart':
        if action[1] == 'piece':
            res = qe.ev
            
        
    else:
        res = fullfillment
       
    return res

