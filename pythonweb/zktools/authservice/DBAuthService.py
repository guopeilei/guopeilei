from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from zktools.orm.ServiceAuth import ServiceAuth


class DBAuthService:
    """
    1查询授权表中的授权文件
    """
    def __init__(self, url):
        self.url = url
        self.dbSession = None
        self.sList = []

    def conn_db(self,):
        try:
            conn_str = self.url
            db_handle = create_engine(conn_str)
            if db_handle:
                db_sess = sessionmaker(bind=db_handle)
                self.dbSession = db_sess()
        except Exception as e:
            raise e

    def get_auth_info_by_service_code(self, service_code):
        """
        1.service_ids 查询授权文件
        2.查询所有的授权信息
        :param service_code: 服务ID
        :return:
        """
        if service_code is None:
            return None
            # 按服务码查询，查出来的数据肯定只有一条
        db_data = self.dbSession.query(ServiceAuth).filter(ServiceAuth.SERVICE_CODE == service_code).all()
        return db_data

    def get_auth_info(self, service_ids):
        """
        1.service_ids 查询授权文件
        2.查询所有的授权信息
        :param service_ids: 服务ID数组
        :return:
        """
        consumer_auth_db_data = []
        if service_ids is None:
            service_ids = []
        if len(service_ids):
            # 按照serviceId查询
            # 按服务码查询，查出来的数据肯定只有一条
            db_data = self.dbSession.query(ServiceAuth).filter(ServiceAuth.SERVICE_CODE.in_(service_ids)).all()
            service_name = db_data[0].CHANNEL_SYSTEM
            consumer_data = ConsumerAuthData(service_name, db_data)
            consumer_auth_db_data.append(consumer_data)
        else:
            # 查询所有的授权文件
            consumer_auth_service_name_lists = self.get_consumer_auth_service()
            for consume_auth_serivice_name in consumer_auth_service_name_lists:
                db_data = self.dbSession.query(ServiceAuth)\
                    .filter(ServiceAuth.CHANNEL_SYSTEM == consume_auth_serivice_name[0]).all()
                if db_data is None:
                    continue
                consumer_data = ConsumerAuthData(consume_auth_serivice_name[0], db_data)
                consumer_auth_db_data.append(consumer_data)
        return consumer_auth_db_data

    def get_consumer_auth_service(self):
        """
        1.在授权表中查询所有的消费方服务
        :return:
        """
        db_data = self.dbSession.query(ServiceAuth.CHANNEL_SYSTEM).all()
        db_data_set = list(set(db_data))
        return db_data_set

    def dis_connect(self,):
        if self.dbSession:
            self.dbSession.close()

    def modify_auth_service_status(self, service_ids=[]):
        """
        修改数据数据表数据的状态
        :return:
        """
        if len(service_ids):
            # 将数据状态全部改为已授权状态
            self.dbSession.query(ServiceAuth).filter(ServiceAuth.SERVICE_CODE.in_(service_ids))\
                .update({ServiceAuth.STATUS: '1'}, synchronize_session=False)
        else:
            self.dbSession.query(ServiceAuth).update(ServiceAuth.STATUS == "1")
        self.dbSession.commit()


class ConsumerAuthData:
    def __init__(self, consumer_name, consumer_data):
        self.consumer_name = consumer_name
        self.consumer_data = consumer_data
