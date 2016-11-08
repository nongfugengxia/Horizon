#coding:utf8
import sys
import pycurl
import time
import StringIO
import urllib 

'''
class Test:
    def __init__(self):
        self.contents = ''
    def body_callback(self, buf):
        self.contents = self.contents + buf
sys.stderr.write("Testing %sn" % pycurl.version)
start_time = time.time()
url = 'http://www.dianping.com/hangzhou'
t = Test()
c = pycurl.Curl()
c.setopt(c.URL, url)
c.setopt(c.WRITEFUNCTION, t.body_callback)
c.perform()
end_time = time.time()
duration = end_time - start_time
print c.getinfo(pycurl.HTTP_CODE), c.getinfo(pycurl.EFFECTIVE_URL)
c.close()
print 'pycurl takes %s seconds to get %s ' % (duration, url)
print 'lenth of the content is %d' % len(t.contents)
#print(t.contents)
'''

class funcCurl():
        #------------------------自动处理cookile的函数----------------------------------#
        def initCurl(self):
        #初始化一个pycurl对象，
        #尽管urllib2也支持 cookie 但是在登录cas系统时总是失败，并且没有搞清楚失败的原因。
        #这里采用pycurl主要是因为pycurl设置了cookie后，可以正常登录Cas系统
                c = pycurl.Curl()
                c.setopt(pycurl.COOKIEFILE, "cookie_file_name")#把cookie保存在该文件中
                c.setopt(pycurl.COOKIEJAR, "cookie_file_name")
                c.setopt(pycurl.FOLLOWLOCATION, 1) #允许跟踪来源
                c.setopt(pycurl.MAXREDIRS, 5)
                #设置代理 如果有需要请去掉注释，并设置合适的参数
                #c.setopt(pycurl.PROXY, ‘http://11.11.11.11:8080′)
                #c.setopt(pycurl.PROXYUSERPWD, ‘aaa:aaa’)
                return c
        #-----------------------------------get函数-----------------------------------#
        def GetDate(self,curl, url):
        #获得url指定的资源，这里采用了HTTP的GET方法
                head = ['Accept:*/*',
                        'User-Agent:Mozilla/5.0 (Windows NT 6.1; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0']
                buf = StringIO.StringIO()
                curl.setopt(pycurl.WRITEFUNCTION, buf.write)
                curl.setopt(pycurl.URL, url)
                curl.setopt(pycurl.HTTPHEADER,  head)
                curl.perform()
                the_page =buf.getvalue()
                buf.close()
                return the_page
        #-----------------------------------post函数-----------------------------------#
        def PostData(self,curl, url, data):
                buf = StringIO.StringIO()
                curl.setopt(pycurl.WRITEFUNCTION, buf.write)
                curl.setopt(pycurl.POSTFIELDS,  urllib.urlencode(data))
                curl.setopt(pycurl.URL, url)
                curl.perform()
                the_page = buf.getvalue()
                buf.close()
                return the_page
        #-----------------------------------post函数-----------------------------------#
        def PostFile(self,curl, url, data,mypic):
                buf = StringIO.StringIO()
                values = [("file", (pycurl.FORM_FILE, mypic))]
                for i in data:
                    values.append( ( i,data[i]))
                curl.setopt(pycurl.WRITEFUNCTION, buf.write)
                #curl.setopt(pycurl.POSTFIELDS,  urllib.urlencode(data))
                curl.setopt(pycurl.URL, url)
                curl.setopt(pycurl.HTTPPOST, values)
                curl.perform()
                the_page = buf.getvalue()
                buf.close()
                return the_page

 
if __name__ == "__main__":
        op = funcCurl() 
        c = op.initCurl()
        html = op.GetDate(c, 'http://10.19.19.23/liaojie-online/web/index.php?r=api/list-api&type=data&value=263')
        print html
