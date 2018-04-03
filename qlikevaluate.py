import json
import qlikserv as qs

v_docName = "Utilization"

def parseExp(op_format,filters,exp,date):
    exp1 = ""
    mon = ""
    com = ""
    mon1=""
    date = [x.strip(' ') for x in date]
    print(filters)
    if len(date)>=2:
        mon = "Month={\">$(=date('"+date[0]+"'))<$(=date('"+date[1]+"'))\"}"
        com = ","
        mon1 = "{1<"+mon+">}"
    
    if len(filters)>0:
        if op_format == 'minus': #Minus expression
            j =0
            for i in filters:
                dim1 = qs.closeMatch(i["qs_dimension"],'d')
                filter1 = "{1<"+dim1[0]+"={'"+(i["qs_filter_val"]).strip()+"'}"+com+mon+">}"
                if j>=1:
                    exp1 = exp1+"-"
                exp1 = exp1+exp.replace("<f>",filter1)
                j = j+1
        else: ############################expression with filter
            dim1 = qs.closeMatch(filters[0]["qs_dimension"],'d')
            filter1 = "{1<"+dim1[0]+"={'"+(filters[0]["qs_filter_val"]).strip()+"'}"+com+mon+">}"
            exp1 = exp.replace("<f>",filter1)
    else:
        exp1 = exp.replace("<f>",mon1)
    #print(exp1)
            
    return exp1
        
        

def getExp(measure,ws,handle,filters,op_format,date):
    print(measure[0])
    desc = qs.closeMatch(measure[0],'m')
    exp = "only({1<Description={'"+desc[0]+"'}>}formula)"
    exp1 = qs.evExp(ws,handle,exp)
    #print(exp1)
    parse_exp = parseExp(op_format,filters,exp1,date)
    return parse_exp

def getExpDim(dimension,operation,filters,date):
    if operation == "count":
        dim = qs.closeMatch(dimension[0],'d')
        exp = "count(<f>"+dim[0]+")"
        parse_exp = parseExp("",filters,exp,date)
        return parse_exp
    else: return "999"        
    
    
def evaluate(parameters):
    measure = parameters["qs_measure"]
    dimension = parameters["qs_dimension"]
    date = parameters["date-period"].split("/")
    op_format = parameters["qs_format"]
    restrict = parameters["qs_restrict"]
    operation = parameters["qs_operation"]
    filters = parameters["qs_filter"]
    available = parameters["qs_filter_available"]
    if len(available) >0 :
        temp = {}
        temp["qs_filter_val"] = available
        temp["qs_dimension"] = "available"
        filters.append(temp)

    ws = qs.openWs()
    handle = qs.openDoc(ws,v_docName)

    if (len(parameters["qs_dimension"]) > 0 and operation != "count") or ("list" in op_format):
        expr = getExp(measure,ws,handle,filters,op_format,date)
        print("A"+expr)
        result = qs.evList(ws,handle,expr,parameters["qs_dimension"],"f")
    elif (len(dimension) > 0 and operation == "count" and len(measure)==0):
        expr = getExpDim(dimension,operation,filters,date)
        print("B"+expr)
        result = qs.evExp(ws,handle,expr)
    elif "percentage" in op_format:
        temp = []
        for i in measure:
            temp.append(i+" "+op_format)
        expr = getExp(temp,ws,handle,filters,op_format,date)
        print("D"+expr)
        result = str(float(qs.evExp(ws,handle,expr))*100)+"%"
    else:
        expr = getExp(measure,ws,handle,filters,op_format,date)
        print("C"+expr)
        result = qs.evExp(ws,handle,expr)
    ws.close()
    return result


def evaluate_chart(parameters):
    measure = parameters["qs_measure"]
    dimension = parameters["qs_dimension"]
    date = parameters["date-period"].split("/")
    op_format = parameters["qs_format"]
    restrict = parameters["qs_restrict"]
    operation = parameters["qs_operation"]
    filters = parameters["qs_filter"]
    available = parameters["qs_filter_available"]

    
    ws = qs.openWs()
    handle = qs.openDoc(ws,v_docName)
    expr = getExp(measure,ws,handle,filters,op_format,date)
    print("A"+expr)
    result = qs.evList(ws,handle,expr,parameters["qs_dimension"],"r")
    
