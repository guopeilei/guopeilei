from kazoo.client import KazooClient
from kazoo.retry import KazooRetry
import logging

log = logging.getLogger(__name__)


class ZkClient:
    def __init__(self, url):
        self.upCont = 0
        self.addCont = 0
        self.url = url

        try:
            connection_retry = KazooRetry(max_tries=3, delay=0.1)
            command_retry = KazooRetry(max_tries=3, delay=0.1)
            self.zk = KazooClient(hosts=url, timeout=10.0,
                                  connection_retry=connection_retry,
                                  command_retry=command_retry,
                                  logger=None)
            if self.zk:
                self.zk.start(timeout=60)
                log.info("连接zk服务器%s成功", url)
                # 设置ACL
                self.zk.add_auth("digest", "SmartESC:startesc123")
        except Exception as e:
            raise e

    def close(self):
        if self.zk:
            self.zk.stop()
            self.zk.close()
            log.info("断开zk连接...")

    def writeData(self, path, data):
        try:
            self.zk.set(path, data)
        except Exception as e:
            log.exception("数据写入错误")
            raise e

    def set_zookeeper_data(self, data={}):
        """
        父节点的数据不存在时，则创建父节点
        data数据中需要包含路径
        :param data:
        :return:
        """
        for path in data.keys():
            try:
                if self.zk.exists(path):
                    self.zk.set(path, data[path])
                    self.upCont += 1
                else:
                    self.zk.create(path, data[path], makepath=True)
                    self.addCont += 1
            # log.info("路径:%s",path)
            except Exception as e:
                log.exception("数据%s写入错误", path)
                raise e

    def set_service_data(self, data={}):
        """
        父节点的数据不存在时，不创建父节点
        data中包含zookeeper的路径，
        :param data:
        :return:
        """
        for path in data.keys():
            try:
                if self.zk.exists(path):
                    self.zk.set(path, data[path])
                    self.upCont += 1
                else:
                    self.zk.create(path, data[path])
                    self.addCont += 1
                # log.info("路径:%s",path)
            except Exception as e:
                log.exception("数据%s写入错误", path)
                raise e

    def get_onecfg_service(self,sCode):
        data={}
        try:
            meta=self.zk.get_children("/metadata")
            for st in meta:
                if sCode in st:
                    path="/metadata/%s"%(st)
                    data[path],stat=self.zk.get(path)
            cons = self.zk.get_children("/metadata/consumer")
            for st in cons:
                if sCode in st:
                    path = "/metadata/consumer/%s" % (st)
                    data[path], stat = self.zk.get(path)
            prvd = self.zk.get_children("/metadata/provider")
            for st in prvd:
                if sCode in st:
                    path = "/metadata/provider/%s" % (st)
                    data[path], stat = self.zk.get(path)
            return data
        except Exception as e:
            log.exception("zk数据读取错误:")
            raise e

    def get_cfg_service(self,sCodeList=[]):
        """
        在zookeeper中查找服务,获取zookeeper中服务的数据
        :param sCodeList:
        :return:
        """
        data = {}
        for sCode in sCodeList:
            try:
                meta = self.zk.get_children("/metadata")
                for st in meta:
                    if sCode in st:
                        path = "/metadata/%s" % (st)
                        data[path], stat = self.zk.get(path)
                cons = self.zk.get_children("/metadata/consumer")
                for st in cons:
                    if sCode in st:
                        path = "/metadata/consumer/%s" % (st)
                        data[path], stat = self.zk.get(path)
                prvd = self.zk.get_children("/metadata/provider")
                for st in prvd:
                    if sCode in st:
                        path = "/metadata/provider/%s" % (st)
                        data[path], stat = self.zk.get(path)
            except Exception as e:
                log.exception("zk数据读取错误:")
                raise e
        return data

    def get_cfg_service_by_service_code(self, service_code):
        """
        在zookeeper中查找服务,获取zookeeper中服务的数据
        :param service_code:
        :return:
        """
        data = {}
        try:
            meta = self.zk.get_children("/metadata")
            for st in meta:
                if service_code in st:
                    path = "/metadata/%s" % (st)
                    data[path], stat = self.zk.get(path)
            cons = self.zk.get_children("/metadata/consumer")
            for st in cons:
                if service_code in st:
                    path = "/metadata/consumer/%s" % (st)
                    data[path], stat = self.zk.get(path)
            prvd = self.zk.get_children("/metadata/provider")
            for st in prvd:
                if service_code in st:
                    path = "/metadata/provider/%s" % (st)
                    data[path], stat = self.zk.get(path)
        except Exception as e:
            log.exception("zk数据读取错误:")
            raise e
        return data

    def get_cfg_service_auth_by_system_name(self, system_name):
        """
        在zookeeper中查找服务的授权信息
        :param system_name: 系统名称
        :return:
        """
        data = {}
        new_path = ''
        try:
            meta = self.zk.get_children("/configs")
            for file_name in meta:
                if system_name in file_name:
                    path = "/configs/%s" % (file_name)
                    new_path = path+"/consumer/authCtrl/"+system_name
                    if self.zk.exists(new_path):
                        data[new_path], stat = self.zk.get(new_path)
        except Exception as e:
            log.exception("zk数据读取授权数据错误:%s", new_path)
            raise e
        return data

    def get_allcfg_service(self):
        data={}
        try:
            meta=self.zk.get_children("/metadata")
            for st in meta:
                path="/metadata/%s"%(st)
                data[path],stat=self.zk.get(path)
            cons = self.zk.get_children("/metadata/consumer")
            for st in cons:
                path = "/metadata/consumer/%s" % (st)
                data[path], stat = self.zk.get(path)
            prvd = self.zk.get_children("/metadata/provider")
            for st in prvd:
                path = "/metadata/provider/%s" % (st)
                data[path], stat = self.zk.get(path)
            return data
        except Exception as e:
            log.exception("zk数据读取错误:")
            raise e




