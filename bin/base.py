
class c_confparser:
    def __init__( self, argv ):
        self.conf = ConfigParser.ConfigParser() 
        self.conf.read(argv[1])  

        self.__user = self.conf.get('user','user')
        self.__passwd = self.conf.get('user','password')

        self.__test_data = self.get_conf_data('test_data')
        self.__train_data = self.get_conf_data('train_data')

    def get_conf_data( self, data_name):
        data_dict = {}
        for i in ['path_type','data_path','data_id','split_pro','data_type','use_ignore']:
            data_dict[i] = self.conf.get( data_name,i)
        return data_dict
 
    def get_user(self):
        return self.__user,self.__passwd


        ''' 
        opts, args = getopt.getopt( argv[1:], "hadnsl:i:o:p:u:r:c:v:f:m:")
        ops = {}
        for op, value in opts:
            ops[op] = value
            if op == "-l":
                self.list_type_value = value
            elif op == "-h":
                self.usage()
                sys.exit()
	'''


class base
    def __init__:
        pass

    def data:
        pass
