import os
import json
import logging.config
from zktools.orm import *
from zktools.zookeeper.zkClient import *
from zktools.authservice.serviceauthservice import *
from zktools.service.db2_data_service import DB2Data
from zktools.javatools.operjava import *
import sys
f = open('default.log', 'a')
sys.stdout = f
sys.stderr = f

log = logging.getLogger(__name__)


def init_logging(default_path="./Config.json", default_level=logging.INFO):
    """
    初始化日志
    :param default_path:
    :param default_level:
    :return:
    """
    if os.path.exists(default_path):
        with open(default_path, "r", encoding="utf-8") as file:
            config = json.load(file)
            logging.config.dictConfig(config)
            return config
    else:
        logging.basicConfig(level=default_level)
        return None
    pass


def sure_check(main_win):
    main_win.destroy()


def export_db_data(master_env, service_ids):
    # 导出数据到dict中，创建数据库连接
    db_worker = DB2Data(master_env.db_url, master_env.name)
    db_worker.conn_db()
    # 查询数据库中的数据
    db_data = db_worker.get_service_all_data(service_ids)
    db_worker.dis_connect()
    return db_data


def export_zk_data(env, service_ids):
    zk_worker = ZkClient(env.zk_url)
    if service_ids[0] == "ALL":
        zk_data = zk_worker.get_allcfg_service()
    else:
        # 获取zookeeper中的配置数据
        zk_data = zk_worker.get_cfg_service(service_ids)
    zk_worker.close()
    return zk_data


def get_zk_data_by_system_name(env, system_name):
    """
    根据单个系统名称查询zookeeper中的授权配置信息
    :param env:
    :param system_name:
    :return:
    """
    zk_worker = ZkClient(env.zk_url)
    zk_data = zk_worker.get_cfg_service_auth_by_system_name(system_name)
    zk_worker.close()
    return zk_data


def import_zk_data(zkurl, name, zk_data):
    """
    将数据导入zookeeper中
    :param zkurl: zookeeper的路径
    :param zk_data: 需要导入的数据
    :param name: 环境名称
    :return: None
    """
    log.info("|||||======开始向%s导入zk配置======|||||", name)
    zk_other = ZkClient(zkurl)
    zk_other.set_service_data(zk_data)
    log.info("|||||======%s导入zk配置成功,新增%d条,更新%d条======|||||", name, zk_other.addCont, zk_other.upCont)
    zk_other.close()


def import_db_data(db2_url, name, db_data):
    log.info("|||||======开始向%s导入DB数据======|||||", name)
    db_other = DB2Data(db2_url, name)
    db_other.conn_db()
    db_other.set_service_all_data(db_data)
    db_other.dis_connect()
    log.info("|||||======向%s导入DB数据完成======|||||", name)


def get_master_data(master_env, service_ids):
    zk_data = export_zk_data(master_env, service_ids)
    db_data = export_db_data(master_env, service_ids)
    service_data = ServiceData(zk_data, db_data)
    return service_data


def move_data(flow_env_list, service_data, master_env):
    """
    将主节点的配置同步到 其他服务器上
    :return: None
    """
    try:
        log.info("开始从主节点进行数据导出...")
        # 开始循环导入
        for env in flow_env_list:
            if env.name == master_env.name:
                continue
            name = env.name
            zkurl = env.zk_url
            db2url = env.db_url
            import_zk_data(zkurl, name, service_data.zk_data)
            import_db_data(db2url, name, service_data.db_data)
            log.info('======环境：'+name+'数据同步成功')
    except Exception as e:
        msg = "程序运行异常:\n"+str(e)
        log.error("error"+msg)
        sys.exit()


def init():
    cfg = init_logging(default_path="./zktools/service/app.json")
    if cfg is not None:
        log.info("===========配置加载成功===========")
        pass
    return ServiceEnv(cfg)


def service_auth(env_list, service_ids):
    """
    服务授权，
    1.先从zookeeper 上下载数据文件，
    2.再将自己的信息写入文件，
    3.将更新号的文件写入zookeeper
    :return:
    """
    for env in env_list:
        # 从数据库中查询授权数据
        for service_code in service_ids:
            db_auth_list = get_db_auth_data_by_service_code(service_code, env.db_url)
            for db_auth_info in db_auth_list:
                system_name = db_auth_info.CHANNEL_SYSTEM
                service_code = db_auth_info.SERVICE_CODE
                zk_data = get_zk_data_by_system_name(env, system_name)
                new_zk_data = modify_service_auth_file(zk_data, db_auth_info, system_name)
                log.info('%s,%s 写入授权数据', env.zk_url, system_name)
                if new_zk_data.xml_content is None:
                    log.info('%s,%s 服务已经在系统 %s 总存在', env.zk_url, service_code, system_name)
                else:
                    write_auth_data_to_zk(env.zk_url, new_zk_data.xml_content)

                # 对终端进行授权
                # 不管终端是否已经在zookeeper中存在， 终端重新进行一次授权
                service_terminate_auth(env.db_url, system_name, new_zk_data.service_num, env.zk_url)
                log.info('更新zookeeper 授权数据成功，更新的系统：%s', system_name)


def get_terminate_info(db2_url, system_name):
    try:
        db2 = DB2Data(db2_url, '')
        db2.conn_db()
        terminate_info = db2.get_terminate_info_by_system_name(system_name)
        db2.dis_connect()
    except Exception as e:
        raise e
    return terminate_info


def service_terminate_auth(db2_url, system_name, num, zk_url):
    """
    对终端进行授权
    :param db2_url:
    :param system_name:
    :param num:
    :param zk_url:
    :return:
    """
    terminate_info_list = get_terminate_info(db2_url=db2_url, system_name=system_name)
    for terminate_info in terminate_info_list:
        terminate_id = terminate_info.TERMINAL_ID
        terminate_ip = terminate_info.TERMINAL_ADDRESS
        terminate_port = terminate_info.TERMINAL_PORT
        terminate_op_auth(ip=terminate_ip, port=terminate_port, system_name=system_name, tmn_id=terminate_id,
                          num=num, zk_url=zk_url)
