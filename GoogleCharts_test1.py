#!/usr/bin/python

import gviz_api
import sys
import imgkit

page_template = """
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <script type="text/javascript" src="https://www.google.com/jsapi"></script>

        <script type="text/javascript">
            function init() {
                google.load("visualization", "1.1", { packages:["corechart"], callback: 'drawCharts' });
            }

            function drawCharts() {
                drawAccountImpressions('chart-account-impressions');
            }
            
            function drawAccountImpressions(containerId) {
			%(data)s

        var options = {'title':'How Much Pizza I Ate Last Night',
                       'width':400,
                       'height':300};
        var chart = new google.visualization.PieChart(document.getElementById(containerId));
        chart.draw(data, options);
            }
        </script>
    </head>
    
    <body onload="init()">
    	<div id="chart-account-impressions"></div>
    </body>
</html>
"""

def main():
  # Creating the data
  description = {"topping": ("string", "Topping"),
                 "slices": ("number", "Slices")}
  data = [{"topping": "Mushrooms", "slices": 3},
          {"topping": "Onions", "slices": 2},
          {"topping": "Olives", "slices": 1},
          {"topping": "Zucchini", "slices": 1},
          {"topping": "Pepperoni", "slices": 8}]

  # Loading it into gviz_api.DataTable
  data_table = gviz_api.DataTable(description)
  data_table.LoadData(data)

  # Create a JavaScript code string.
  data = data_table.ToJSCode("data",
                               columns_order=("topping", "slices"),
                               order_by="slices")
  # Create a JSON string.
  json = data_table.ToJSon(columns_order=("topping", "slices"),
                           order_by="slices")

  # Put the JS code and JSON string into the template.
  #print ("Content-type: text/html")
  #print
  #print (page_template % vars())

  html = open("C:\\Users\\sdcuser.US2B4QER0H\\Desktop\\test.html","w")
  html.write(page_template % vars())
  html.close()
  optionss = {          
      'javascript-delay':1000
   }


  imgkit.from_file(r'C:\Users\sdcuser.US2B4QER0H\Desktop\test.html', r'C:\Users\sdcuser.US2B4QER0H\Desktop\test.jpg',options=optionss)
  #imgkit.from_string(page_template % vars(),r'C:\Users\sdcuser.US2B4QER0H\Desktop\test.jpg',options=optionss)
  print("Done")

  


if __name__ == '__main__':
  main()
