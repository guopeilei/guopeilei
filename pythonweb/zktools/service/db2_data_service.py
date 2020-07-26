from sqlalchemy import create_engine
from sqlalchemy.orm import *
from zktools.orm.ServiceAuth import *
from zktools.orm.ServiceConfig import *
from zktools.orm.ServiceDefine import *
from zktools.orm.ServiceReg import *
from zktools.orm.ServiceIdenfy import *
from zktools.orm.terminate_info import *

import logging


log = logging.getLogger(__name__)


class DB2Data:

    def __init__(self, url, name):
        self.url = url
        self.name = name
        self.dbSession = None
        self.sList = []

    def conn_db(self,):
        try:
            connStr = self.url
            log.info("数据库连接串%s", connStr)
            dbHandle = create_engine(connStr)
            if dbHandle:
                dbSess = sessionmaker(bind=dbHandle)
                self.dbSession = dbSess()
                log.info("创建%s数据库连接成功", self.name)
        except Exception as e:
            raise e

    # 服务定义配置表获取关联服务id
    def get_service_define(self, sList=[]):
        try:
            # 从数据库中查出所有的服务定义数据
            sdAll = self.dbSession.query(ServiceDefine)
            if sList[0] == 'ALL':
                for sid in sdAll:
                    self.sList.append(sid.SERVICE_ID)
                sds = sdAll.all()
            else:
                self.sList = sList
                sds = sdAll.filter(ServiceDefine.SERVICE_ID.in_(self.sList)).all()
            if sds:
                return sds
        except Exception as e:
            log.exception("db2查询错误:")
            raise e

    # 拆组包配置表获取关联服务id
    def get_service_config(self, sList = []):
        try:
            cps = self.dbSession.query(ServiceConfig).filter(ServiceConfig.SERVICE_ID.in_(self.sList)).all()
            if cps:
                return cps
        except Exception as e:
            log.exception("db2查询错误: %s", self.name)
            raise e

    # 服务注册配置表获取关联服务id
    def get_service_reg(self, sList = []):
        try:
            srs = self.dbSession.query(ServiceReg).filter(ServiceReg.SERVICE_ID.in_(sList)).all()
            if srs:
                return srs
        except Exception as e:
            log.exception("db2查询错误:")
            raise e
        # 服务注册配置表获取关联服务id

    # 服务授权配置表获取关联服务id
    def get_service_auth(self, sList=[]):
        try:
            if sList == "ALL":
                srs=self.dbSession.query(ServiceAuth).all()
            else:
                srs = self.dbSession.query(ServiceAuth).filter(ServiceAuth.SERVICE_CODE.in_(sList)).all()
            if srs:
                return srs
        except Exception as e:
            log.exception("db2查询错误:")
            raise e

    # 服务识别配置表获取关联服务id
    def get_service_identify_invoke(self, sList=[]):
        try:
            if sList == "ALL":
                siis = self.dbSession.query(ServiceIdenfyInvoke).all()
            else:
                siis = self.dbSession.query(ServiceIdenfyInvoke).filter(ServiceIdenfyInvoke.IDENTIFY_KEY.in_(sList)).all()
            if siis:
                return siis
        except Exception as e:
            log.exception("db2查询错误:")
            raise e

    def get_service_identify(self, sList=[]):
        try:
            eids = self.dbSession.query(ServiceIdenfyInvoke.INVOKE_ID). \
                filter(ServiceIdenfyInvoke.IDENTIFY_KEY.in_(sList)).all()
            print(eids)
            for eid in eids:
                print(eid.INVOKE_ID)
                print(type(eid))
            sids = self.dbSession.query(ServiceIdenfy).filter(ServiceIdenfy.INVOKE_ID.in_(eids)).all()
            if sids:
                print(sids)
                return sids
        except Exception as e:
            log.exception("db2查询错误:")
            raise e

    # 获取服务的配置所有数据
    def get_service_all_data(self, service_ids):
        sData={}
        svcList = service_ids
        try:
            # 查询服务定义到数据字典中
            sData['sDef'] = self.get_service_define(svcList)
            svcList = self.sList
            log.info("全部服务码:%s", svcList)
            # 查询服务拆组包到数据字典中
            sData['sCP'] = self.get_service_config(svcList)
            # 查询服务注册到数据字典中
            sData['sReg'] = self.get_service_reg(svcList)
            # 查询服务授权到数据字典中
            sData['sAuth'] = self.get_service_auth(svcList)
            # 查询服务拆组包到数据字典中
            sData['sIdenInv'] = self.get_service_identify_invoke(svcList)
            # sData['sIden'] = self.getServiceIdentify(svcList)
            log.info("导出数据:%s", sData)
        except Exception as e:
            log.exception("获取数据错:")
            raise e
        return sData

    def set_service_all_data(self, data={}):
        for key in data.keys():
            try:
                if data[key]:
                    for row in data[key]:
                        if key == "sDef":
                            # 如果存在数据，则删除现在的数据，覆盖数据
                            myrow = self.dbSession.query(ServiceDefine.SERVICE_ID, ServiceDefine.SYSTEM_ID)\
                                .filter(ServiceDefine.SERVICE_ID == row.SERVICE_ID, ServiceDefine.SYSTEM_ID == row.SYSTEM_ID).delete()
                        if key == "sCP":
                            myrow = self.dbSession.query(ServiceConfig.SERVICE_ID, ServiceConfig.SYSTEM_ID, ServiceConfig.TYPE, ServiceConfig.MODEL) \
                                .filter(ServiceConfig.SERVICE_ID == row.SERVICE_ID, ServiceConfig.SYSTEM_ID == row.SYSTEM_ID, ServiceConfig.TYPE == row.TYPE,
                                        ServiceConfig.MODEL == row.MODEL).delete()
                        if key == "sReg":
                            myrow = self.dbSession.query(ServiceReg.SERVICE_ID) \
                                .filter(ServiceReg.SERVICE_ID == row.SERVICE_ID).delete()

                        if key == "sAuth":
                            myrow = self.dbSession.query(ServiceAuth.CHANNEL_SYSTEM, ServiceAuth.PACKAGE_TYPE, ServiceAuth.SERVICE_CODE, ServiceAuth.SERVICE_SYSTEM) \
                                .filter(ServiceAuth.CHANNEL_SYSTEM == row.CHANNEL_SYSTEM, ServiceAuth.PACKAGE_TYPE == row.PACKAGE_TYPE, ServiceAuth.SERVICE_CODE == row.SERVICE_CODE,
                                        ServiceAuth.SERVICE_SYSTEM == row.SERVICE_SYSTEM).all()
                            if len(myrow):
                                continue
                        if key == "sIdenInv":
                            myrow = self.dbSession.query(ServiceIdenfyInvoke.IDENTIFY_KEY, ServiceIdenfyInvoke.IDENTIFY_VALUE, ServiceIdenfyInvoke.IDENTIFY_STATE, ServiceIdenfyInvoke.INVOKE_ID) \
                                .filter(ServiceIdenfyInvoke.IDENTIFY_KEY == row.IDENTIFY_KEY, ServiceIdenfyInvoke.IDENTIFY_VALUE == row.IDENTIFY_VALUE,
                                        ServiceIdenfyInvoke.IDENTIFY_STATE == row.IDENTIFY_STATE, ServiceIdenfyInvoke.INVOKE_ID == row.INVOKE_ID).all()
                            if len(myrow):
                                continue
                        sql = self.dbSession.merge(row)
            except Exception as e:
                log.exception("数据更新错误:")
                raise e
        self.dbSession.commit()

    def get_terminate_info_by_system_name(self, system_name):
        """
        根据系统名查询终端信息
        :param system_name:
        :return:
        """
        try:
            terminate_info_list = self.dbSession.query(TerminateInfo.TERMINAL_PORT, TerminateInfo.TERMINAL_ID, TerminateInfo.TERMINAL_ADDRESS, TerminateInfo.TERMINAL_SYSTEM) \
                                    .filter(TerminateInfo.TERMINAL_SYSTEM == system_name,
                                            TerminateInfo.TERMINAL_STATUS == 'run').all()
        except Exception as e:
            log.exception('查询终端信息报错')
            raise e
        self.dbSession.commit()
        return terminate_info_list

    def dis_connect(self,):
        if self.dbSession:
            log.info("关闭环境数据库连接%s", self.name)
            self.dbSession.close()
