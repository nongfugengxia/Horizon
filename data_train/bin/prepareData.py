from ConfigParser import SafeConfigParser
import ConfigParser
import commands
import fileinput
import linecache
import logging
import os
import random
import re
import shutil
import sys
import tarfile
import time
import urllib


class Data:
    configPath = ''
    idVersionMap2FolderName = {}
    cp = ConfigParser.SafeConfigParser()
    modelType = ''
    
    testArr = []
    test_path_type = ''
    test_data_src = ''
    test_data_id = ''
    test_split_pro = ''
    trainArr = []
    train_path_type = ''
    train_data_src = ''
    train_data_id = ''
    train_split_pro = ''
    
    map = {}
    
    
    def __initLogging(self):
        logging.basicConfig(level=logging.DEBUG,
          format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
          datefmt='%m-%d %H:%M',
          filename='../log/my.log',
          filemode='w')
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)
        logging.info('info information')
        logging.debug('debug information')
        logging.warning('warning information')
        logging.error('error information')
    
    
    def __init__(self, configPath):
        self.configPath = configPath
    
    def verifyConfigFile(self): # path is the only parameter
        self.cp.read(self.configPath)
        items = self.cp.items('main')
        for item in items:
            if item[0] == 'model_type':
                model_type = item[1]
        haveModel = 0
        for item in self.cp.sections():
            if item == model_type:
                haveModel = 1;
                logging.info("We have the model: \"" +  model_type + "\"")
                self.modelType = model_type
                modelTypeDir = '../train_env/' + self.modelType
                isExists=os.path.exists(modelTypeDir)
                if not isExists:
                    os.makedirs(modelTypeDir)       # make directory according model type in '../train_env/
                    os.makedirs(modelTypeDir + "/input/")
                    os.makedirs(modelTypeDir + "/output/")
                    os.makedirs(modelTypeDir + "/input/test_data")
                    os.makedirs(modelTypeDir + '/input/train_data')
                else:
                    logging.warn('Directory \"' + modelTypeDir + '\" is existed, and not make directory')
        if haveModel == 0:
            logging.error('we lose model in datasystem.conf, and system exit.')
            return 0;
        
        itemsTest = self.cp.items('test_data')
        itemsTrain = self.cp.items('train_data')
        
        for test_i in itemsTest:
            if test_i[0] == 'path_type':
                self.test_path_type = test_i[1]
            if test_i[0] == 'data_path':
                self.test_data_src = test_i[1]
            if test_i[0] == 'data_id':
                self.test_data_id = test_i[1]
            if test_i[0] == 'split_pro':
                self.test_split_pro = test_i[1]
        if self.test_path_type == '':
            logging.error('\"path_type\" is not exist in \"test_data\" configuration.  [' + configPath + '], and program exit.')
            return 0
        if self.test_data_src == '':
            logging.error('\"data_path\" is not exist in \"test_data\" configuration.  [' + configPath + '], and program exit.')
            return 0
        if self.test_data_id == '':
            logging.error('\"data_id\" is not exist in \"test_data\" configuration.  [' + configPath + '], and program exit.')
            return 0
        if self.test_split_pro == '':
            logging.error('\"split_pro\" is not exist in \"test_data\" configuration.  [' + configPath + '], and program exit.')
            return 0
        
        for train_i in itemsTrain:
            if train_i[0] == 'path_type':
                self.train_path_type = train_i[1]
            if train_i[0] == 'data_path':
                self.train_data_src = train_i[1]
            if train_i[0] == 'data_id':
                self.train_data_id = train_i[1]
            if train_i[0] == 'split_pro':
                self.train_split_pro = train_i[1]
        if self.train_path_type == '':
            logging.error('\"path_type\" is not exist in \"train_data\" configuration.  [' + configPath + '], and program exit.')
            return 0
        if self.train_data_src == '':
            logging.error('\"data_path\" is not exist in \"train_data\" configuration.  [' + configPath + '], and program exit.')
            return 0
        if self.train_data_id == '':
            logging.error('\"data_id\" is not exist in \"train_data\" configuration.  [' + configPath + '], and program exit.')
            return 0
        if self.train_split_pro == '':
            logging.error('\"split_pro\" is not exist in \"train_data\" configuration.  [' + configPath + '], and program exit.')
            return 0
        return 1
    
            
    def __getFileList(self, path):
        for home, dirs, files in os.walk(path):
            for filename in files:
                yield os.path.join(home, filename)
    
    
    def __analysisConf(self):
        self.cp.read(configPath)

        self.testArr = self.test_data_id.split(',')
        self.trainArr = self.train_data_id.split(',')
        
        self.map['test'] = []
        self.map['train'] = []
        self.map['same'] = []
        for train_i in self.trainArr:
            self.map['train'].append(train_i) 
        for test_i in self.testArr:
            self.map['test'].append(test_i)
            if test_i in self.map['train']:
                self.map['same'].append(test_i)
                self.map['test'].remove(test_i)
                self.map['train'].remove(test_i)
            else:
                self.map['test'].append(test_i)
    
    
    def __copyData(self, process_id):
        if self.test_path_type == 'db' and self.train_path_type == 'db' and len(self.map['same']) > 0:
            logging.info('The test_data and train_data has same data id and version')
            modelPath = '../train_env/' + self.modelType
            for test_i in self.map['test']:
                logging.info('test: ' + test_i)
                testDataId = test_i.split('|')[0]
                testDataVersion = test_i.split('|')[1]
                testSrcPath = '../data/' + str(process_id) + '/' + self.idVersionMap2FolderName[str(testDataId) + '_' + str(testDataVersion)]
                testDstPath = modelPath + '/input/train_data/' + self.idVersionMap2FolderName[str(testDataId) + '_' + str(testDataVersion)]
                shutil.copytree(testSrcPath, testDstPath) 
            for train_i in self.map['train']: 
                logging.info('train: ' + train_i)
                trainDataId = train_i.split('|')[0]
                trainDataVersion = train_i.split('|')[1]
                trainSrcPath = '../data/' + str(process_id) + '/' + self.idVersionMap2FolderName[str(trainDataId) + '_' + str(trainDataVersion)]
                trainDstPath = modelPath + '/input/train_data/' + self.idVersionMap2FolderName[str(trainDataId) + '_' + str(trainDataVersion)]
                shutil.copytree(trainSrcPath, trainDstPath) 
            for rand_i in self.map['same']:
                logging.info('rand: ' + rand_i)
                randDataId = rand_i.split('|')[0]
                randDataVersion = rand_i.split('|')[1]
                randSrcPath = '../data/' + str(process_id) + '/' + self.idVersionMap2FolderName[str(randDataId) + '_' + str(randDataVersion)]
                
                randTestDstPath = modelPath + '/input/test_data/' + self.idVersionMap2FolderName[str(randDataId) + '_' + str(randDataVersion)]
                shutil.copytree(randSrcPath, randTestDstPath)
                for fullname in self.__getFileList(randTestDstPath):
                    testDataLines = len(open(fullname, 'rU').readlines())
                    selectTestNum = (int)((float)(self.test_split_pro)*((int)(testDataLines)))
                    testRandSelect =  random.sample(range(testDataLines), selectTestNum) # begins 0
                    selectedList = []
                    for selectedLineNum in testRandSelect:
                        selectLine = open(fullname).readlines()[selectedLineNum]
                        selectedList.append(selectLine)
                    os.remove(fullname)
                    randSelectedFp = open(fullname, 'w')
                    for selectedItem in selectedList:
                        randSelectedFp.write(selectedItem)
                
                randTrainDstPath = modelPath + '/input/train_data/' + self.idVersionMap2FolderName[str(randDataId) + '_' + str(randDataVersion)]
                shutil.copytree(randSrcPath, randTrainDstPath)
                for fullname in self.__getFileList(randTrainDstPath):
                    trainDataLines = len(open(fullname, 'rU').readlines())
                    selectTrainNum = (int)((float)(self.train_split_pro)*((int)(trainDataLines)))
                    trainRandSelect =  random.sample(range(trainDataLines), selectTrainNum) # begins 0
                    selectedList = []
                    for selectedLineNum in trainRandSelect:
                        selectLine = open(fullname).readlines()[selectedLineNum]
                        selectedList.append(selectLine)
                    os.remove(fullname)
                    randSelectedFp = open(fullname, 'w')
                    for selectedItem in selectedList:
                        randSelectedFp.write(selectedItem)
            return
        
        if self.test_path_type == 'local' or self.test_path_type == 'db':
            for test_i in self.testArr:
                testDataId = test_i.split('|')[0]
                testDataVersion = test_i.split('|')[1]
                test_data_dst = modelPath + '/input/test_data/' + self.idVersionMap2FolderName[str(testDataId) + '_' + str(testDataVersion)]
                shutil.copytree(self.test_data_src, test_data_dst)
            logging.info('Copy test data success!')
        
        if self.train_path_type == 'local' or self.train_path_type == 'db':
            for train_i in self.trainArr:
                trainDataId = train_i.split('|')[0]
                trainDataVersion = train_i.split('|')[1]
                train_data_dst = modelPath + '/input/train_data/' + self.idVersionMap2FolderName[str(testDataId) + '_' + str(testDataVersion)]
                shutil.copytree(self.train_data_src, train_data_dst)
            logging.info('Copy test data success!')
    
        
    def __Schedule(self, a, b, c):
        percentage = 100.0 * a * b / c
        if (percentage > 100) :
            percentage = 100
        logging.info('Downloading %.2f%%', percentage)
    
    
    def __downloadFromRemoteByIdVersion(self, id, version, process_id):
        # move to process_id folder
        downloadFileDir = '../data/' + str(process_id)
        isExists=os.path.exists(downloadFileDir)
        if not isExists:
            os.makedirs(downloadFileDir)
        
        import sys
        sys.path.append('..')
        import tools.HDS_TOOLS.bin.run as run
        
        # python bin/run.py -p horizon-test -d -i 206 -v 11
        # [Download]  output id is [60043],  message: 20, 206, 11,False
        checkDownloadFinishedCount = 0;
        
        op = run.hds_tools()
        argList = ['','-p', 'horizon-test', '-d', '-i', id, '-v', version]
        op.confParser( argList)
        runMessage = op.run()
        logging.info(runMessage)
        pattern = r"(\[.*?\])";
        downloadID = re.findall(pattern,runMessage ,re.M)
        if len(downloadID)>0 :
            downloadID = downloadID[1]
            downloadID = downloadID.replace('[','').replace(']','')
            logging.info('Download id: ' + downloadID)
            
        while True:
            # python bin/run.py -p horizon-test -s -i 60012
            op = run.hds_tools()
            argList = ['','-p', 'horizon-test', '-s', '-i', downloadID]
            op.confParser( argList)
            runMessage = op.run()
            logging.info(runMessage)
            if 'URL' in runMessage:
                break
            checkDownloadFinishedCount = checkDownloadFinishedCount+1
            if checkDownloadFinishedCount > 60*60:
                logging.error('Download data from remote failed')
                sys.exit()
        
        indexURL = runMessage.index('URL')
        URL = runMessage[indexURL+6 : len(runMessage)-2]
        URL = URL.replace('\\', '')
        logging.info('Download URL: ' + URL)
        urlArr = URL.split('/')
        downloadFileName = urlArr[len(urlArr)-1]
        downloadFolderName = downloadFileName[0: len(downloadFileName)-4]
        logging.info('Download file name: ' + downloadFileName)
        
        logging.info('Download file id = ' + str(id) + ', version = ' + str(version))
        self.idVersionMap2FolderName[str(id) + '_' + str(version)] = downloadFolderName
        local = os.path.join('../data/', str(process_id), downloadFileName)
        urllib.urlretrieve(URL, local, self.__Schedule)
        logging.info('file download finished')
        tar = tarfile.open('../data/' + str(process_id) + '/' + downloadFileName)
        fileNames = tar.getnames()
        for fileName in fileNames:
            tar.extract(fileName, '../data/' + str(process_id))
        tar.close()
        logging.info('extract finished')
        os.remove("../data/" + str(process_id) + '/' + downloadFileName)

    
    def downloadFromeRemote(self, process_id):
        for test_i in self.map['test']:
            testDataId = test_i.split('|')[0]
            testDataVersion = test_i.split('|')[1]
            self.__downloadFromRemoteByIdVersion(testDataId, testDataVersion, process_id)
            
        for train_i in self.map['train']:
            trainDataId = train_i.split('|')[0]
            trainDataVersion = train_i.split('|')[1]
            self.__downloadFromRemoteByIdVersion(trainDataId, trainDataVersion, process_id)
                
        for same_i in self.map['same']:
            sameDataId = same_i.split('|')[0]
            sameDataVersion = same_i.split('|')[1]
            self.__downloadFromRemoteByIdVersion(sameDataId, sameDataVersion, process_id)
            
    
    def prepareData(self, process_id):
        self.__initLogging()
        if self.verifyConfigFile() == 0:
            sys.exit(1)
        self.__analysisConf() 
        self.downloadFromeRemote(process_id)
        self.__copyData(process_id)



configPath = '../conf/datasystem.conf'
data = Data(configPath);
data.prepareData(1024)  # process_id