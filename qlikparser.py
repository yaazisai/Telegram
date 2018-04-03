import json

def GetDocList(handle):
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
    return data
def OpenDoc(handle,appName):
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
    return data
def CreateSessionObjectField(handle):
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
        return data
def GetLayout(handle):
        data = json.dumps({
                "jsonrpc": "2.0",
                "handle": handle,
                "method": "GetLayout",
                "params": []
                },
                sort_keys=True,
                indent=4,
                separators=(',', ': '))
        return data
def EvaluateEx(handle,expr):
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
    return data
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
def CreateSessionObjectColumn(handle,dim):
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
                                      dim
                                   ],
                                   "qFieldLabels": [
                                      dim
                                   ],
 
                                }


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

    
def CreateSessionObjectList(handle,expr,dim):
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
                                      dim
                                   ],
                                   "qFieldLabels": [
                                      dim
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
                                      "qExpr": expr
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
def GetListObject(handle,width=2,height=10):
        data = json.dumps({
                        "handle": handle,
                        "method": "GetListObjectData",
                        "params": {
                                "qPath": "/qListObjectDef",
                                "qPages": [
                                        {
                                                "qLeft": 0,
                                                "qTop": 0,
                                                "qWidth": width,
                                                "qHeight": height
                                        }
                                ]
                        }
                    },
            sort_keys=True,
            indent=4,
            separators=(',', ': '))
        return data
    
