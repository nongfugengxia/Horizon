#coding:utf-8

# def fact(n):
#   if n==1:
#     return 1
#   return n * fact(n - 1)
# print  fact(3);


# import sys

# reload(sys)
# sys.setdefaultencoding('utf-8')

# import json
import simplejson as json
from array import array


# def scan_ponint_boxes(input):
#     for b in input:
#         print b
#         if b == 'boxes':
#             box = input['boxes']
#             print box


# def hJson(json1, i = 0):
#     if (isinstance(json1, dict) or isinstance(json1, list)):
#         for item in json1:
#             if (isinstance(json1[item], dict)):
#                 print("****"*i+"%s : %s"%(item,json1[item]))
#                 hJson(json1[item], i=i+1)
#             else:
#                 print("****"*i+"%s : %s"%(item,json1[item]))
#     else:
#          print("json1  is not josn object!")
                 
#  
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


# def transfer(input_json, output):
#     if isinstance(input_json,dict):
#         for key in input_json.keys():
#             if key == "boxes":
#                 boxes = input_json.get(key) #list foreach
# #                 print type(boxes[0])
#                 for (d, x) in boxes[0].items():
#                     print "Key:" + d + ",value: " + str(x)
# #                 for m in range(len(boxes)):
# #                     print boxes[m]
# #                 if isinstance(key_value,dict):
# #                     transfer(key_value, output)
# #                 elif isinstance(key_value,list):
# #                     for json_array in key_value:
# #                         transfer(json_array, output)
# #                 else:
# #                     print str(key)+" = "+str(key_value)
#     elif isinstance(input_json,list):
#         for input_json_array in input_json:
#             transfer(input_json_array, output)

#  list 是不可哈希的，而 tuple 是可哈希的
def transfer(input_json, output):
    if isinstance(input_json, dict):
        for key in input_json.keys():
            if key == "boxes":
                result = ''                       # 保存person得value值
                boxes = input_json.get(key)
#                 print type(boxes)
                for box in boxes:
                    print type(box)
                    for (d, x) in box.items():     # 遍历获得每个dict属性
                        print "Key:" + d + ",value: " + str(x)
                        if key == 'rect':
                            strData = 'data' + str(x)
                            result = result + strData
                        if key == 'attrs':
                            strAttrs = 'attrs' + str(x)
                            result = result + strAttrs
                        if key == 'id':
                            strId = 'id' + str(x)
                            result = result + strId
                    for (d, x) in box.items():     # 将获得得dict属性拼接称list返回
                        if (d == 'type'):
                            strTrack_id = 'track_id' + '-1'
                            result = result + strTrack_id
                            resType =  str(x) + result
                            output = output + resType  # 将拼接得到得Dict加入到最终List中去
                            
                        for (d, x) in box.items():
                            if key == 'point':
                                result = ''
                                points = input_json.get(key)
                                for point in points:
                                    for (d, x) in point.items():
                                        if key == 'group':
                                            strData = 'data' + str(x)
                                            result = result + strData
                                        if key == 'num':
                                            strAttrs = 'num' + str(x)
                                            result = result + strAttrs
                                        if key == 'id':
                                            strId = 'id' + str(x)
                                            result = result + strId
                                    for (d, x) in point.items():
                                        if (d == 'type'):
                                            strTrack_id = 'track_id' + '-1'
                                            result = result + strTrack_id
                                            resType =  str(x) + result
                                            output = output + resType  # 将拼接得到得Dict加入到最终List中去
                    output = output + transfer(box, output);
    elif isinstance(input_json,list):
        for input_json_array in input_json:
            for key in input_json_array.keys():
                if key == "boxes":
                    result = ''                       # 保存person得value值
                    boxes = input_json.get(key)
                    for box in boxes:
                        for (d, x) in box.items():     # 遍历获得每个dict属性
    #                         print "Key:" + d + ",value: " + str(x)
                            if key == 'rect':
                                strData = 'data' + str(x)
                                result = result + strData
                            if key == 'attrs':
                                strAttrs = 'attrs' + str(x)
                                result = result + strAttrs
                            if key == 'id':
                                strId = 'id' + str(x)
                                result = result + strId
                        for (d, x) in box.items():     # 将获得得dict属性拼接称list返回
                            if (d == 'type'):
                                strTrack_id = 'track_id' + '-1'
                                result = result + (strTrack_id,)
                                resType =  str(x) + result
                                output = output + resType  # 将拼接得到得Dict加入到最终List中去
                            
                        for (d, x) in boxes.items():
                            if key == 'point':
                                result = ''
                                points = input_json.get(key)
                                for point in points:
                                    for (d, x) in point.items():
                                        if key == 'rect':
                                            strData = 'data' + str(x)
                                            result = result + strData
                                        if key == 'attrs':
                                            strAttrs = 'attrs' + str(x)
                                            result = result + strAttrs
                                        if key == 'id':
                                            strId = 'id' + str(x)
                                            result = result + strId
                                    for (d, x) in point.items():
                                        if (d == 'type'):
                                            strTrack_id = 'track_id' + '-1'
                                            result = result + (strTrack_id,)
                                            resType =  str(x) + result
                                            output = output + resType  # 将拼接得到得Dict加入到最终List中去
                        output = output + transfer(box, output);
    return output



def trans(input, output, father_type, father_id):
    for b in input.get('boxes'):
        typ =  b.get('type')
        id = b.get('id')
        if (output.get(typ) == None):
            output[typ] = dict()
        lis = [{
            'data':b.get('rect'),
            'attrs':b.get('attrs'),
            'id':b.get('id'),
            'track_id':-1,
        }];
        output[typ] = lis;
        if father_id != -1:
            output['belong_to'] = [
                str(father_type) + ':' + str(father_id) + '|' + str(typ) + ':' + str(id)
            ]
        
        if b.get('points') != None :
            for p in b.get('points'):
                ptyp = p.get('type')
                if (output.get(ptyp) == None):
                    output[ptyp] = dict()
                p_group = list()
                for pg in p.get('group'):
                    p_g = [pg[1], pg[2]]
                    p_group.append(p_g)
                lis = [{
                    'data':p_group,
                    'id':p.get('id'),
                    'num':p.get('num'),
                    'track_id':-1
                }];
                output[ptyp] = lis;
                
                if father_id != -1:
                    output['belong_to'] = [
                        str(father_type) + ':' + str(father_id) + '|' + str(typ) + ':' + str(id)
                    ]
        trans(b, output, typ, id)
    return output
    


f = open('log3', 'r')
fr = f.read()

line1 = fr[13:694]
# print line1
json1 =  json.loads(line1)

# outputTuple = ();
# output = ''
# outputList = transfer(json1, output)
# print output

output = dict()
output = trans(json1, output, -1, -1)
output['image_key'] = 'a'
output['video_name'] = 1
output['video_index'] = 1
output['height'] = 1
output['width'] = 1
print output


# output = dict
# output = transfer(json1, dict)
# output = transfer(json1)
# print output










line2 = fr[711:1425]
# print line2
json2 = json.loads(line2)
# print json2








info={}
info["code"]=1
info["id"]=1900
info["name"]='张三'  
info["sex"]='男'

list=[info,info,info]

data={}
data["code"]=1
data["id"]=1900
data["name"]='张三'  
data["sex"]='男'
data["info"]=info
data["data"]=list

jsonStr = json.dumps(data)

# print "jsonStr:",jsonStr



# http://blog.csdn.net/daqingwow/article/details/17993881