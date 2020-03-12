from django.shortcuts import render

# Create your views here.
from django.http import Http404,HttpResponse
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from django.core import serializers
from django.conf import settings
import json




from django.views.decorators.csrf import csrf_exempt

@api_view(["POST"])
def IdealWeight(heightdata):
	try:
		height=json.loads(heightdata.body)
		weight-str(height*10)
		return JsonResponse("ideal weight:"+weight+" Kg",safe=False)
	except ValueError as e:
		return Response(e.args[0],status.HTTP_400_BAD_REQUEST)

def  Hello(request) :
	context={}
	html = "<html><body><h1>Hello world</h1></body></html>"
	return HttpResponse(html)



import mysql.connector
import json
from mysql.connector import Error
from mysql.connector import errorcode



import datetime



host="citdoc.clayanyx9uke.ap-south-1.rds.amazonaws.com"
passwd="India_1024"
user="admin"
database="Cit_Hms"
def converter(o):
	if isinstance(o, (datetime.datetime,datetime.date,datetime.timedelta)):
		return o.__str__()
	if isinstance(o, decimal.Decimal):
		return float(o)	
s3_url="https://citzon-images.s3.ap-south-1.amazonaws.com/category_images/"      
def getservices(inputs):
    try:
         mydb = mysql.connector.connect(host=host,user=user,passwd=passwd,database=database)
         mycursor = mydb.cursor()
         print(inputs.GET.keys(),'inputs')
         if inputs.GET=={}:
          print('yes')
         if inputs.GET=={}:
             mycursor.execute('select * from services ;')
    
             columns = [col[0] for col in mycursor.description]
             json_data = [dict(zip(columns, row)) for row in mycursor.fetchall()]
            #  for i in range(0,len(json_data)):
                    
            #          if json_data[i]['ImageURLs']!=None:
            #                     json_data[i]['ImageURLs']=s3_url + json_data[i]['ImageURLs']
                      
             return HttpResponse(json.dumps({"Status":1,"Services":json_data},default=converter),content_type='application/json')
    
         
         elif 'serviceId' in inputs.GET.keys():
            
                 string="select * from services where serviceId="+inputs.GET['serviceId']+";"
                 print(string)
                 mycursor.execute(string)
                 columns = [col[0] for col in mycursor.description]
                 json_data = [dict(zip(columns, row)) for row in mycursor.fetchall()]
                 
                 return HttpResponse(json.dumps({"Status":1,"Services":json_data},default=converter),content_type='application/json')
    
    except mysql.connector.Error as error :
                   print("Failed inserting date object into MySQL table {}".format(error))
    finally :
                if(mydb.is_connected()):
                        mycursor.close()
                        mydb.close()
                        print("MySQL connection is closed") 
@csrf_exempt                       
def insertservices(params):
    try :
                connection = mysql.connector.connect(host=host,user=user,passwd=passwd,database=database,autocommit=True)
                cursor = connection.cursor()
                print('here******************************')
                
                json_data = json.loads(params.body.decode('utf-8'))
                print(json_data)
                values = (json_data['type'], json_data['measure'],json_data['description'],json_data['imgURL'])
                insert = """INSERT INTO services(`type`,`measure`,`description`,`imgURL`) values(%s,%s,%s,%s);"""
                result = cursor.execute(insert,values)
                print("effected rows:",cursor.rowcount)
                return HttpResponse(json.dumps({"Status":1,"Message":"service added succesfully"}),content_type='application/json')
    
                
                
                            
    except mysql.connector.Error as error :
                   print("Failed inserting date object into MySQL table {}".format(error))
    finally :
                if(connection.is_connected()):
                        cursor.close()
                        connection.close()
                        print("MySQL connection is closed")
                        
@csrf_exempt                         
def updateservices(request,ServiceId):
    try :     
         mydb = mysql.connector.connect(host=host,user=user,passwd=passwd,database=database,autocommit=True)
         mycursor = mydb.cursor(buffered=True)
        

         
         
         event = json.loads(request.body.decode('utf-8'))
         print(event) 
           
         type ="type=type" if 'type' not in event.keys() else "type='"+event['type']+"'"
                  
         measure ="measure=measure" if 'measure' not in event.keys() else "measure='"+event['measure'] +"'"
                  
         description = "description=description" if 'description' not in event.keys() else "description='"+event['description'] +"'"
                  
         imgURL = "imgURL=imgURL" if 'imgURL' not in event.keys() else "imgURL='"+event['imgURL'] +"'"
          
        
              
         string="select * from services where serviceId="+str(ServiceId)+";"
         mycursor.execute(string)
         if mycursor.rowcount==0:
                  return HttpResponse(json.dumps({"Status":1,"Message":"service doesnot exists"}),content_type='application/json')
    
         else :
                 SQL = "update services set "+type+","+measure+","+description+","+imgURL+" where serviceId = '" + str(ServiceId)+"';"
                 
                 mycursor.execute(SQL)
                 
                 return HttpResponse(json.dumps({"Status":1,"Message":"service updated succesfully"}),content_type='application/json')
    
    except mysql.connector.Error as error :
                   print("Failed inserting date object into MySQL table {}".format(error))
    finally :
                if(mydb.is_connected()):
                        mycursor.close()
                        mydb.close()
                        print("MySQL connection is closed") 
@csrf_exempt                         
def deleteservices(request,ServiceId):
    try:
         
         mydb = mysql.connector.connect(host=host,user=user,passwd=passwd,database=database,autocommit=True)
         mycursor = mydb.cursor(buffered=True)
         string="update services set Status=0 where serviceId="+str(ServiceId)+";"
         mycursor.execute(string)
         print ("number of affected rows: {}".format(mycursor.rowcount))
         if mycursor.rowcount==0:
                 return HttpResponse(json.dumps({"Status":1,"Message":"service doesnot exists"}),content_type='application/json')
    
                 
         else:       
                 return HttpResponse(json.dumps({"Status":1,"Message":"service deleted succesfully"}),content_type='application/json')
    
    except mysql.connector.Error as error :
                   print("Failed inserting date object into MySQL table {}".format(error))
    finally :
                if(mydb.is_connected()):
                        mycursor.close()
                        mydb.close()
                        print("MySQL connection is closed")
                        
                       
def lambda_handler(event,context) :
        
        print    
        if event['httpMethod'] == 'GET' :
          
          inputs = event['queryStringParameters']
          print("get method")
          response = getservices(inputs)
          return response
          
        if event['httpMethod'] == 'POST' :
              #body = event['body']
              body=json.loads(event['body'])
              print(body,"body")
              print("Post method")
              print(event)
              response = insertservices(body)
              return response
              
        if event['httpMethod'] == 'PUT' :
          #body = event['body']
          inputs= event['pathParameters']
          print(inputs)
          body=json.loads(event['body'])
          print("PUT Method")
          print(event)
          response = updateservices(body,inputs)
          return response 
          
        if event['httpMethod'] == 'DELETE' :
          inputs= event['pathParameters']
        
          print("DELETE Method")
          print(event)
          print('inputs:',inputs)
          response = deleteservices(inputs)
          return response 
          
