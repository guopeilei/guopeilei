from zktools.zookeeper.zkClient import ZkClient
from zktools.authservice.DBAuthService import DBAuthService
from zktools.authservice.Authxml import AuthXml
from xml.dom.minidom import parseString
from jmxquery import JMXConnection, JMXQuery
from zktools.orm.authxmlinfo import AuthXmlInfo
import logging.config
log = logging.getLogger(__name__)
def get_zk_service(service_id, zk_url):
    zk_client = ZkClient(zk_url)
    zk_client.get_cfg_service(service_id)
    print("abcb")


def write_auth_data_to_zk(zk_url, zk_data):
    zk_client = ZkClient(zk_url)
    zk_client.set_zookeeper_data(zk_data)
    zk_client.close()


def modify_auth_data(service_ids, db_url):
    """
    更改数据库服务的授权状态
    :return:
    """
    db_auth_service = DBAuthService(db_url)
    db_auth_service.conn_db()
    db_auth_service.modify_auth_service_status(service_ids)
    db_auth_service.dis_connect()


def get_db_auth_data(service_ids, db_url):
    db_auth_service = DBAuthService(db_url)
    db_auth_service.conn_db()
    db_auth_lists = db_auth_service.get_auth_info(service_ids)
    db_auth_service.dis_connect()
    return db_auth_lists


def get_db_auth_data_by_service_code(service_code, db_url):
    db_auth_service = DBAuthService(db_url)
    db_auth_service.conn_db()
    db_auth = db_auth_service.get_auth_info_by_service_code(service_code)
    db_auth_service.dis_connect()
    return db_auth


def get_auth_xml_data(db_auth_data_lists):
    auth_xml = AuthXml()
    # 得到授权的数据
    return auth_xml.getAuthXmlData(db_auth_data_lists)


def modify_service_auth_file(auth_file_data_s, auth_db_data, system_name):
    """
    根据数据库的授权信息，修改zookeeper的授权文件
    :param auth_file_data_s:  一个zookeeper 中的授权文件
    :param system_name:
    :param auth_db_data:  一条数据库中的授权记录, 根据服务码查询出来的授权信息是个数组
    :return:
    """
    try:
        if not bool(auth_db_data):
            return None
        if not bool(auth_file_data_s):
            return None

        auth_file = None
        new_path = ''
        for key in auth_file_data_s:
            new_path = key
            auth_file = auth_file_data_s[key]
        service_code = auth_db_data.SERVICE_CODE
        service_version = auth_db_data.VERSION_NO
        package_type = auth_db_data.PACKAGE_TYPE
        auth_file_str = str(auth_file).replace("'", "\"")
        start_index = auth_file_str.index("<?")
        file_content = auth_file_str[start_index: len(auth_file_str)-1]
        file_content = file_content.replace("\\n", "")
        if service_code in file_content:
            num = get_num_in_system_name_of_service_code(file_content)
            return AuthXmlInfo(None, num)

        dom_tree = parseString(file_content)
        root_node = dom_tree.documentElement
        consumer = root_node.getElementsByTagName('consumer')
        # 创建服务节点
        service_node = dom_tree.createElement('service')
        service_node.setAttribute('serviceId', service_code)
        service_node.setAttribute('serviceVersion', service_version)
        service_node.setAttribute('packageMode', package_type)
        service_node.setAttribute('dataRouter', '')
        service_node.setAttribute('valid', '')

        # 文档根元素
        consumer[0].appendChild(service_node)
        data = {}
        new_file_content = dom_tree.toxml().encode()
        data[new_path] = new_file_content
        num = 0
    except Exception as e:
        log.exception('解析xml报错')
        raise e
    return AuthXmlInfo(data, num)


def get_num_in_system_name_of_service_code(file_content):
    """
    获取系统中授权的服务的个数
    :param file_content: xml的内容
    :return:
    """
    dom_tree = parseString(file_content)
    root_node = dom_tree.documentElement
    consumer = root_node.getElementsByTagName('consumer')
    num = consumer[0].childNodes.length
    return num


def jmx_oper(terminate_url, terminate_port):
    jmx_url = "service:jmx:rmi:///jndi/rmi://%s:%d/jmxrmi" % (terminate_url, terminate_port)
    jmx_connection = JMXConnection(jmx_url)    # 这里写对应使用的jdk路径
    ## memory
    type_str = "Memory"
    bean_name_str = "ServiceAuthMBean:name=ServiceAuth".format(type_str)
    jmx_connection.query()


if __name__ == '__main__':
    """
    将某个环境上的服务授权
    1.授权所有的未授权的服务
    2.授权单个服务
    """
    ip = '9.1.6.247'
    port = 1799
    jmx_oper(ip, port)
