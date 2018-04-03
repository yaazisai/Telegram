from websocket import create_connection
import json
from fuzzywuzzy import process
import qlikparser as qp

qAppList = None
qFieldList = {}
qFieldList["items"] = []
qWildchar = []
qDimension = []
qFieldObj = {}
v_docName = "Utilization"

def openWs():
    ws = create_connection("ws://localhost:4848/app/")
    result =  ws.recv()
    print("connected to Qlik Sense")
    return ws


def getAppDesc(ws):
    data = qp.GetDocList(-1)
    ws.send(data)
    result1 =  ws.recv()
    result = json.loads(result1)
    return result

def openDoc(ws,appName):
    data = qp.OpenDoc(-1,appName)
    ws.send(data)
    result = json.loads(ws.recv())
    #print(appName)
    #print(result)
    return result["result"]["qReturn"]["qHandle"]


def getfields():
    ws = openWs()
    handle = openDoc(ws,v_docName)
    data = qp.CreateSessionObjectColumn(handle,"Description")
    ws.send(data)
    result = json.loads(ws.recv())   
    handle1 = result["result"]["qReturn"]["qHandle"]
    data1 = qp.GetListObject(handle1,1,20)
    ws.send(data1)
    result1 = json.loads(ws.recv())
    matrix = result1["result"]["qDataPages"][0]["qMatrix"]
    for i in matrix:
        qWildchar.append(i[0]["qText"])       
    ws.close()

def getdimension():
    ws = openWs()
    handle = openDoc(ws,v_docName)
    data = qp.CreateSessionObjectField(handle)
    ws.send(data)
    result = json.loads(ws.recv())
    
    handle1 = result["result"]["qReturn"]["qHandle"]
    data1 = qp.GetLayout(handle1)
    ws.send(data1)
    result1 = json.loads(ws.recv())
    for i in result1["result"]["qLayout"]["qFieldList"]["qItems"]:
        if "qIsSystem" not in i:
            if '$text' in i["qTags"]:
                qDimension.append(i["qName"])
    ws.close()

def evExp(ws,handle,expr):
    print("ee")
    print(expr)
    data = qp.EvaluateEx(handle,expr)
    ws.send(data)
    result = json.loads(ws.recv())
    return result["result"]["qValue"]["qText"]

def evList(ws,handle,expr,dim,frmt):
    #print(dim)
    dim1 = closeMatch(dim[0],"d")
    data = qp.CreateSessionObjectList(handle,expr,dim1[0])
    #print(data)
    ws.send(data)
    resultT = json.loads(ws.recv())
    #print(resultT)
    handle1 = resultT["result"]["qReturn"]["qHandle"]
    data1 = qp.GetListObject(handle1)
    ws.send(data1)

    resultT1 = json.loads(ws.recv())
    #print(resultT1)
    if frmt == 'f':
        op=""
        for i in resultT1["result"]["qDataPages"][0]["qMatrix"]:
            op += i[0]["qText"]+" : "+i[1]["qText"]+"\n"
    elif frmt == 'r':
        op = {}
        
        return op
        
def searchField(col):
    res = []
    for j in col:

        if len(j) > 0:
            opD = process.extractOne(j,qWildchar)
            opD = opD[0]
        else: opD = ""
        res.append(opD)
    return res

def closeMatch(col,flg):
    if flg == 'm':
        return process.extractOne(col,qWildchar)
    else:
        return process.extractOne(col,qDimension)

 
def evaluate(parameters):
    print("parm")
    print(parameters)
    dim = parameters["qs_dimension"]
    meas = parameters["qs_subject"]
    if(len(parameters["qs_operation"])>0):
        operation = parameters["qs_operation"]
    else: operation = "sum"
    d_dim = searchField(dim)
    d_meas = searchField(meas)
    expr = ""
    if len(d_meas) == 1:
        expr = operation[0]+"(["+d_meas[0]+"])"
    ws = openWs()
    handle = openDoc(ws,v_docName)
    

    if len(parameters["qs_dimension"]) > 0:
        result = evList(ws,handle,expr,parameters["qs_dimension"])
    else:result = evExp(ws,handle,expr)

    return result

getfields()
getdimension()
#print(qWildchar)
#print(qDimension)
