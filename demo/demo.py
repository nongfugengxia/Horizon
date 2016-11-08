sample_list = ['a', 1, ('a', 'b')]

sample_list = ['a', 'b', 0, 1, 2, 3]

value_start = sample_list[0]
end_value = sample_list[-1]
print value_start
print end_value

del sample_list[0]
print sample_list

sample_list[0:0] = ['sample value']
print sample_list

print len(sample_list)

for element in sample_list:
    print element
    
num_inc_list = range(30)
print num_inc_list

initial_value = 0
list_length = 5
sample_list = [initial_value for i in range(10)]
sample_list = [initial_value]*list_length
print sample_list

L = range(1, 5)
print L

L = range(1, 10, 2)
print L

dict = {'ob1':'computer', 'ob2':'mouse', 'ob3':'printer'}





# def printRecursive(input_json):
#     key_value=''
#     if isinstance(input_json,dict):
#         for key in input_json.keys():
#             key_value = input_json.get(key)
#             if isinstance(key_value,dict):
#                 printRecursive(key_value)
#             elif isinstance(key_value,list):
#                 for json_array in key_value:
#                     printRecursive(json_array)
#             else:
#                 print str(key)+" = "+str(key_value)
#     elif isinstance(input_json,list):
#         for input_json_array in input_json:
#             printRecursive(input_json_array)
# 
# import simplejson as json                
# str = '{"b":{"a":[{"n1":"WIFI","lo":116.30744414106923,"t2":"1387873418.195T+08:00","p1":"com.tudou.ui.activity.HomeActivity","n2":840,"la":39.98049465154441,"l":false},{"n1":"WIFI","lo":116.30744414106923,"t2":"1387873415.880T+08:00","t1":"A1005","s1":"5da19f89080af666bc2cb8d8775706df","p1":"com.tudou.ui.activity.HomeActivity"}]},"h":{"i":{"o2":"4.3","o1":"Android","b2":"Nexus 7","m":"10:bf:48:c2:81:f5","h":1205,"w":800,"u":"f835c7f8-c331-4b47-a6a3-772021544aa9","b1":"google"}}}'
# json1 =  json.loads(str)
# print printRecursive(json1)


# import simplejson
# 
# date='[{"name":"Column_owner","point":"AKESH2880153908"},{"name":"Column_name","point":"wiken"}]';  
# jsonVal = simplejson.loads(date)  
#   
# for val in jsonVal:  
#     print val["name"]  
#     print val["point"]  



# import json
# 
# dict_ = {1:2, 3:4, "55":"66"}
# 
# # test json.dumps
# 
# print type(dict_), dict_
# json_str = json.dumps(dict_)
# print "json.dumps(dict) return:"
# print type(json_str), json_str
# 
# # test json.loads
# print "\njson.loads(str) return"
# dict_2 = json.loads(json_str)
# print type(dict_2), dict_2



# import json
#  
# adict={"xiaoqiangk":"xiaoqiangv","xiaofeik":"xiaofeiv","xiaofeis":{"xiaofeifk":"xiaofeifv","xiaofeimk":{"xiaoqik":"xiaoqiv","xiaogou":{"xiaolei":"xiaolei"}}},"xiaoer":{"xiaoyuk":"xiaoyuv"}}
#  
# def hJson(json1, i = 0):
#     if (isinstance(json1, dict)):
#         for item in json1:
#             if (isinstance(json1[item], dict)):
#                 print("****"*i+"%s : %s"%(item,json1[item]))
#                 hJson(json1[item], i=i+1)
#             else:
#                 print("****"*i+"%s : %s"%(item,json1[item]))
#     else:
#          print("json1  is not josn object!")
#                   
#   
#   
# hJson(adict,0)




# def fact(n):
#   if n==1:
#     return 1
#   return n * fact(n - 1)
# print  fact(3);
# 
# 
# import json
# 
# data = {
# 'name' : 'ACME',
# 'shares' : 100,
# 'price' : 542.23
# }
# 
# json_str = json.dumps(data)
# 
# # print json_str
# 
# data = json.loads(json_str)
# 
# # print data['name']
# for b in data:
#     if (b == 'name'):
#         print data['name']