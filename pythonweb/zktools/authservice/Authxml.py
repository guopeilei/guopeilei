import xmltodict



class AuthXml():

    xmlHeader = '<?xml version=\"1.0\" encoding=\"utf-8\"?>\n'
    nodeNameList = []
    authData = {}

    def getAuthXmlData(self, consumerAuthDbDataLists):
        """
        拼接向zookeeper中插入数据的授权数据
        1.根据服务名获取数据，拼接xml内容数据
        2.将xml写入文件，
        3.返回xml数据内容
        :param consumerAuthDbDataLists:
        :return:
        """
        for consumerAuthDbData in consumerAuthDbDataLists:
            xmlstr = self.xmlHeader
            xmlstr = xmlstr + '\n'
            xmlstr = xmlstr + '<Authoritys>\n'
            xmlstr = xmlstr + '  <consumer id="'+consumerAuthDbData.consumerName + '" name="">\n'
            for consumerAuthService in consumerAuthDbData.consumerData:
                version_no = consumerAuthService.VERSION_NO
                if version_no is None:
                    version_no = ""
                xmlstr = xmlstr+'    <service serviceId="' + consumerAuthService.SERVICE_CODE + \
                         '" serviceVersion="' + version_no + \
                         '" packageMode="' + consumerAuthService.PACKAGE_TYPE + '" dataRouter="" valid=""/>\n'
            xmlstr = xmlstr + '  </consumer>\n'
            xmlstr = xmlstr + '</Authoritys>'
            filename = './files/'+consumerAuthDbData.consumerName + '.xml'
            # 将授权文件写到本地
            self.writeContextToXml(filename, xmlstr)
            xmlstr = bytes(xmlstr, encoding='utf-8')
            # 获取将要写入zookeeper中的授权数据
            self.setAuthData(consumerAuthDbData.consumerName, xmlstr)
        return self.authData

    def setAuthData(self, serverName, content):

        nodeName = "tmnl"+serverName+"001";
        if nodeName  in self.nodeNameList:
            nodeName = "tmnl"+serverName+"002"
        if nodeName  in self.nodeNameList:
            nodeName = "tmnl"+serverName+"003"
        self.nodeNameList.append(nodeName)
        zkPath = "/configs/"+nodeName+"/consumer/authCtrl/"+serverName
        self.authData[zkPath] = content

    def writeContextToXml(self, fileName, context):
        file_object = open(fileName, 'w', encoding='utf-8')
        file_object.write(context)
        file_object.close()


