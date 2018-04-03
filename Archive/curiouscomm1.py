import qlikserv
import time
import json
import apiaiconn

def qsglobal(parameters,contexts):
    if "Application" in parameters["object"]:
        return qlikserv.appList(parameters["subject"],parameters["operation"])

def qsquery (parameters,contexts):
    op = qlikserv.evaluate(parameters)
    return op

def input(action,parameters,contexts,fullfillment):
    if action[1]=="global":
        return qsglobal(parameters,contexts)
    elif action[1] == "measure-dimension":
        return qsquery(parameters,contexts)
    else: return fullfillment

def communicate(session_id,CLIENT_ACCESS_TOKEN,resp):
    raw = apiaiconn.getAction(session_id,CLIENT_ACCESS_TOKEN,resp)
    fullfillment = raw["result"]["fulfillment"]["speech"]
    parameters = raw["result"]["parameters"]
    contexts = raw["result"]["contexts"]
    if len(raw["result"]["metadata"]) > 0:
        intentName = raw["result"]["metadata"]["intentName"]
    action = raw["result"]["action"].split(".")
    #print(action)
    res = "I don't understand"
    if action[0] == 'input':
        res = input(action,parameters,contexts,fullfillment)
    else:
        res = fullfillment
       
    return res


    """
    return {
        'input': input(action,parameters,contexts),
        'time':time.asctime( time.localtime(time.time()) )
        }.get(action[0],fullfillment)
    """
