#coding:utf8
import os,sys, getopt
import json
import re 
import ConfigParser  
from func_pycurl import funcCurl
reload(sys)
# sys.setdefaultencoding( "utf-8" )

class hds_tools( ): 

    def __init__(self):
        self.err = open( "../tools/HDS_TOOLS/log/err.log", "a")
        pass
 
    def usage(self):
        print >> sys.stderr, "-u user name"	
        print >> sys.stderr, "-p password"	
        print >> sys.stderr, "-s : check status of task[download/upload] ,     command is : -s -i task_id "	
        print >> sys.stderr, "-l : list %s\t"%self.list_type ," command is : -l project|datalist|data -i null|project_id|data_list_id"	
        print >> sys.stderr, '''-d : download label result with or without images, use -n with images 
\t1. -d  -i  data_list_id  [-n]                : download lastest version 
\t2. -d  -i  data_list_id  -v version [-n] 
\t3. -d  -i  data_list_id  -c class   [-n]     : download class in [%s] of lastest version 
\t4. -d  -r  project_id    -c class   [-n]     : download all datalist in project  with class in [%s] of lastest version'''%("a","a")
        print >> sys.stderr, "-a :  add label result of data_list_id as a new version, command is :  -a -i data_list_id -f file_path -m data_describe" 
    
    def confParser( self, argv ):
        self.list_type_value = None
        self.list_id = None
        self.project_id = None
        self.content = None
        self.data_version = None
        self.download_flag= None
        self.upload_flag= None
        self.status_flag= None
        self.file_path = None
        self.data_des= None
        self.need_image= False 

        self.conf = ConfigParser.ConfigParser() 
#         sys.path.append('../conf')
#         print os.path.abspath('.')
        self.conf.read("../tools/HDS_TOOLS/conf/hdf_tools.conf") 
#         self.conf.read("/home/ubuntu/Install/eclipse/workspace/Horizontal/data_train/tools/HDS_TOOLS/conf/hdf_tools.conf")  
        self.url = self.conf.get("api_common", "url")  
        self.version = self.conf.get("api_common", "version")  
        self.list_type = self.conf.get("list", "type").strip().split(",") 
 
        opts, args = getopt.getopt( argv[1:], "hadnsl:i:o:p:u:r:c:v:f:m:")
        ops = {}
        for op, value in opts:
            ops[op] = value
            if op == "-l":
                self.list_type_value = value
            elif op == "-i":
                self.list_id = value 
            elif op == "-r":
                self.project_id = value 
            elif op == "-c":
                self.content = value 
            elif op == "-v":
                self.data_version = value 
            elif op == "-d":
                self.download_flag= True
            elif op == "-a":
                self.upload_flag = True
            elif op == "-s":
                self.status_flag= True
            elif op == "-f":
                self.file_path = value
            elif op == "-m":
                self.data_des = value
            elif op == "-n":
                self.need_image = "yes"
            elif op == "-h":
                self.usage()
                sys.exit()

        if "-u" in ops.keys():
            self.user= ops['-u']
        else:
            self.user= self.conf.get("api_common", "user")
        if "-p" in ops.keys():
            self.password= ops['-p']
        else:
            print >> sys.stderr, "user is %s, use -p input password"%self.user
            sys.exit(0)

    def run(self): 
        data = {}
        data['version'] = self.version
        data['user'] = self.user
        data['user_password'] = self.password
        
        if self.list_type_value in self.list_type :
            ret = self.list( data, self.list_type_value, self.list_id ) 
        elif self.status_flag and self.list_id:
            ret = self.status(data, self.list_id) 
        elif self.download_flag:
            ret = self.download( data, self.list_id, self.project_id, self.content, self.data_version ) 
        elif self.upload_flag and self.list_id and self.file_path and os.path.isfile( self.file_path) and self.data_des:
            ret = self.upload( data, self.list_id, self.file_path,self.data_des) 
        else:
            self.usage()
            sys.exit(-1)
        
        try: 
            result = json.loads( ret)
            if result['status'] != 0:
                print >> sys.stderr,result['message']
                return result['message'] ## Added by dong
                return False 
            else:
                self.var_dump( result['ret'], result['ret_format'] ) 
                return True
        except Exception as e:
            print >> sys.stderr, "[ERROR] encode json result error"
            print >> self.err.write( "\n[ERROR]\n%s\n%s"%(e,ret))
            return False 

    def chinese_str_len(self,str):  
        try:  
            row_l=len(str)
            utf8_l=len(str.decode('utf-8'))  
            return (row_l-utf8_l)/2 
        except:  
            return None  
        return None
    
    def var_dump( self, ret_json, ret_format):
        flag = True
        format_str = ""
        title_str = []
        count = 0
        for i in sorted( ret_format, key=lambda x:x[0]):
            format_str += "{0[%s]:<%s}|"%(count,i[2])
            title_str.append( i[1])
            count += 1
        print format_str.format( title_str)
        for i in ret_json:
            format_str = ""
            title_str = []
            count = 0
            for j in sorted( ret_format, key=lambda x:x[0]):
                lena =  self.chinese_str_len( str(i[j[1]]) )
                format_str += "{0[%s]:<%s}|"%(count ,j[2] - lena)
                title_str.append( i[j[1]])
                if re.search( "ou", str(i[j[1]])):
                    #print str(i[j[1]]),title_str,count
                    break
                count += 1
            if count == len( title_str):
                try:
                    print format_str.format( title_str)
                except:
                    print >> self.err.write("\n[ERROR]\n"+"\t".join([ str(t) for t in title_str])+"\n")

    def list( self, data,  key, value = None):
        op = funcCurl() 
        c = op.initCurl()
        data['type'] = "list" 
        data['list_type'] = key 
        data['list_type_value'] = value
        return op.PostData(c, self.url, data)
         
    def status( self, data, task_id):
        op = funcCurl() 
        c = op.initCurl()
        data['type'] = "status" 
        data['list_id'] = task_id 
        return op.PostData(c, self.url, data)
         
    def download( self, data,  list_id, project_id, content, version):
        op = funcCurl() 
        c = op.initCurl()
        data['type'] = "download" 
        data['project'] = project_id 
        data['data_id'] = list_id 
        data['contenttype'] = content 
        data['data_version'] = version 
        data['need_image'] = self.need_image 
        return op.PostData(c, self.url, data)
         
    def upload( self, data,list_id, file_path,data_des):
        op = funcCurl() 
        c = op.initCurl()
        data['type'] = "upload" 
        data['data_id'] = list_id 
        data['data_des'] = data_des 
        return op.PostFile(c, self.url, data, file_path)


if __name__ == "__main__":
    op = hds_tools()
    op.confParser( sys.argv )
    op.run()
