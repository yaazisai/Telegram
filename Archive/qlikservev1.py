from websocket import create_connection
import json
from fuzzywuzzy import process

qAppList = None
qFieldList = {}
qFieldList["items"] = []
qFieldObj = {}

def openWs():
    ws = create_connection("ws://localhost:4848/app/")
    result =  ws.recv()
    print("connected to Qlik Sense")
    return ws


def getAppDesc(ws):
    data=json.dumps({
                "jsonrpc": "2.0",
                "id": 0,	
                "handle": -1,
                "method": "GetDocList",
                "params": [],
                },
                sort_keys=True,
                indent=4,
                separators=(',', ': '))
    ws.send(data)
    result1 =  ws.recv()
    result = json.loads(result1)
    return result

def openDoc(ws,appName):
    data=json.dumps({
                "jsonrpc": "2.0",
                "id": 0,
                "handle": -1,
                "method": "OpenDoc",
                "params": {
		"qDocName": appName,
		"qUserName": "",
		"qPassword": "",
		"qSerial": "",
		"qNoData": False}
                },
                sort_keys=True,
                indent=4,
                separators=(',', ': '))
    ws.send(data)
    result = json.loads(ws.recv())
    #print(appName)
    #print(result)
    return result["result"]["qReturn"]["qHandle"]


def getfields():
    ws = openWs()
    apps = getAppDesc(ws)
    ws.close()
    for doc in apps["result"]["qDocList"]:
        ws = openWs()
        handle = openDoc(ws,doc["qDocName"])
        data = json.dumps({
                "jsonrpc": "2.0",
                "handle": handle,
                "method": "CreateSessionObject",
                "params": [{
                  "qInfo": {
                    "qId": "",
                    "qType": "FieldList"
                  },
                  "qFieldListDef": {
                    "qShowSystem": True,
                    "qShowHidden": True,
                    "qShowSemantic": True,
                    "qShowSrcTables": True
                  }}]
                },
                sort_keys=True,
                indent=4,
                separators=(',', ': '))
        ws.send(data)
        result = json.loads(ws.recv())
        
        handle1 = result["result"]["qReturn"]["qHandle"]

        data1 = json.dumps({
                "jsonrpc": "2.0",
                "handle": handle1,
                "method": "GetLayout",
                "params": []
                },
                sort_keys=True,
                indent=4,
                separators=(',', ': '))
        ws.send(data1)
        result1 = json.loads(ws.recv())
        qFieldObj[doc["qDocName"]] = result1["result"]["qLayout"]["qFieldList"]
        qFieldListtemp={}

        qFieldListtemp["name"]= doc["qDocName"]
        qFieldListtemp["fields"] = []
        for i in result1["result"]["qLayout"]["qFieldList"]["qItems"]:
            if "qIsSystem" not in i:
                qFieldListtemp["fields"].append(i["qName"])
        qFieldList["items"].append(qFieldListtemp)
        ws.close()
        #counties = [item for item in data["features"] 
        #if item["classifiers"][0]["subcategory"] == "County"]
        
def searchField(dim,meas):
    
    opMax = (None,0,None,0,None,0.0000)
    opD = (None,0)
    opM = (None,0)
    opA = 0
    #print(str(len(dim))+'-'+str(len(meas)))
    for i in qFieldList["items"]:
        if len(dim) > 0:
            opD = process.extractOne(dim,i["fields"])
        if len(meas) > 0:
            opM = process.extractOne(meas,i["fields"])

        opA = (opM[1]+opD[1])/2
        if opA > opMax[5]:
            opMax = (opD[0],opD[1],opM[0],opM[1],i["name"],opA)
    return opMax

def evExp(ws,handle,expr):
    print("ee")
    #print(expr)
    data = json.dumps({
            "jsonrpc": "2.0",
            "handle": handle,
            "method": "EvaluateEx",
            "params": {
                "qExpression": expr

                }
            },
            sort_keys=True,
            indent=4,
            separators=(',', ': '))
    ws.send(data)
    result = json.loads(ws.recv())
    return result["result"]["qValue"]["qText"]

def createListString(handle,dimension,exp,sort=-1,first=10):
    data = json.dumps({
                        "jsonrpc": "2.0",
                        "handle": handle,
                        "method": "CreateSessionObject",
                        "params": [
                          {
                             "qInfo": {
                                "qId": "",
                                "qType": "ListObject"
                             },
                             "qListObjectDef": {
                                "qStateName": "$",
                                "qLibraryId": "",
                                "qDef": {
                                   "qGrouping": "N",
                                   "qFieldDefs": [
                                      dimension
                                   ],
                                   "qFieldLabels": [
                                      dimension
                                   ],
                                   "qSortCriterias": [
                                      {
                                         "qSortByState": 0,
                                         "qSortByFrequency": 0,
                                         "qSortByNumeric": 0,
                                         "qSortByAscii": 0,
                                         "qSortByLoadOrder": 1,
                                         "qSortByExpression": 0,
                                         "qExpression": {
                                            "qv": exp
                                         }
                                      }
                                   ],
                                   "qNumberPresentations": [
                                      {
                                         "qType": "U",
                                         "qnDec": 10,
                                         "qUseThou": 0,
                                         "qFmt": "",
                                         "qDec": ".",
                                         "qThou": " "
                                      }
                                   ]
                                },
                                "qAutoSortByState": {
                                   "qDisplayNumberOfRows": -1
                                },
                                "qFrequencyMode": "EQ_NX_FREQUENCY_NONE",
                                "qShowAlternatives": True,
                                "qInitialDataFetch": [
                                   {
                                      "qTop": 0,
                                      "qLeft": 0,
                                      "qHeight": first,
                                      "qWidth": 1
                                   }
                                ],
                                "qExpressions": [
                                   {
                                      "qExpr": exp
                                   }
                                ]
                             }
                          }
                        ],
                        "outKey": -1,
                        "id": 4
                        },
            sort_keys=True,
            indent=4,
            separators=(',', ': '))
    return data

def evList(ws,handle,expr,dim):
    print("el")
    data = json.dumps({
                        "jsonrpc": "2.0",
                        "handle": handle,
                        "method": "CreateSessionObject",
                        "params": [
                          {
                             "qInfo": {
                                "qId": "",
                                "qType": "ListObject"
                             },
                             "qListObjectDef": {
                                "qStateName": "$",
                                "qLibraryId": "",
                                "qDef": {
                                   "qGrouping": "N",
                                   "qFieldDefs": [
                                      "COUNTRY"
                                   ],
                                   "qFieldLabels": [
                                      "COUNTRY"
                                   ],
                                   "qSortCriterias": [
                                      {
                                         "qSortByState": 0,
                                         "qSortByFrequency": 0,
                                         "qSortByNumeric": 0,
                                         "qSortByAscii": 0,
                                         "qSortByLoadOrder": 1,
                                         "qSortByExpression": 0,
                                         "qExpression": {
                                            "qv": ""
                                         }
                                      }
                                   ],
                                   "qNumberPresentations": [
                                      {
                                         "qType": "U",
                                         "qnDec": 10,
                                         "qUseThou": 0,
                                         "qFmt": "",
                                         "qDec": ".",
                                         "qThou": " "
                                      }
                                   ]
                                },
                                "qAutoSortByState": {
                                   "qDisplayNumberOfRows": -1
                                },
                                "qFrequencyMode": "EQ_NX_FREQUENCY_NONE",
                                "qShowAlternatives": True,
                                "qInitialDataFetch": [
                                   {
                                      "qTop": 0,
                                      "qLeft": 0,
                                      "qHeight": 20,
                                      "qWidth": 1
                                   }
                                ],
                                "qExpressions": [
                                   {
                                      "qExpr": "sum(SALES)"
                                   }
                                ]
                             }
                          }
                        ],
                        "outKey": -1,
                        "id": 4
                        },
            sort_keys=True,
            indent=4,
            separators=(',', ': '))
    ws.send(data)
    resultT = json.loads(ws.recv())
    #print(resultT)
    handle1 = resultT["result"]["qReturn"]["qHandle"]

    data1 = json.dumps({
                        "handle": handle1,
                        "method": "GetListObjectData",
                        "params": {
                                "qPath": "/qListObjectDef",
                                "qPages": [
                                        {
                                                "qLeft": 0,
                                                "qTop": 0,
                                                "qWidth": 2,
                                                "qHeight": 10
                                        }
                                ]
                        }
                    },
            sort_keys=True,
            indent=4,
            separators=(',', ': '))
    ws.send(data1)

    resultT1 = json.loads(ws.recv())
    #print(resultT1["result"]["qDataPages"][0]["qMatrix"])
    op=""
    for i in resultT1["result"]["qDataPages"][0]["qMatrix"]:
        op += i[0]["qText"]+" : "+i[1]["qText"]+"\n"
    return op
        
    
 
def evaluate(parameters):
    print("parm")
    print(parameters)
    dim = parameters["qs_dimension"]
    meas = parameters["qs_subject"]
    if(len(parameters["qs_operation"])>0):
        operation = parameters["qs_operation"]
    else: operation = "sum"
    field = searchField(dim,meas)
    print("field")
    print(field)
    expr = operation+"("+field[2]+")"
    ws = openWs()
    handle = openDoc(ws,field[4])
    

    if len(parameters["qs_dimension"]) > 0:
        result = evList(ws,handle,expr,parameters["qs_dimension"])
    else:result = evExp(ws,handle,expr)

    return result


def appList(search=None,operation=None):
    ws = openWs()
    result = getAppDesc(ws)
    result = result["result"]
    rText = ""
    count =0
    for doc1 in result["qDocList"]:
        if search:
            for sObj in search:
                if sObj in doc1["qMeta"]["description"]:
                    rText += doc1["qDocName"]+"\n"
                    count += 1
                    break
        else:
            rText += doc1["qDocName"]+"\n"
            count += 1
    if operation == "count":
        #print(rText)
        #print(count)

        temp = rText
        rText = "Apps count : "+str(count)+"\n\n"+temp        

    return rText

getfields()
#print(qFieldList)
