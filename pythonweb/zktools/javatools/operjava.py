#import jpype
import os.path
import logging.config
log = logging.getLogger(__name__)


def terminate_op_auth(ip, port, system_name, tmn_id, num, zk_url):
    """
    操作终端进行授权
    :param ip: 终端的IP
    :param port: 终端的端口
    :param system_name: 终端的的系统
    :param tmn_id: 终端id :ABS001
    :param num: 授权数据的记录条数
    :param zk_url: zookeeper的连接
    :return:
    """
    try:
        #jvm_path = jpype.getDefaultJVMPath()
        jar_path = os.path.join(os.path.abspath("."), "D:\\works\\python\\pythonweb\\zktools\\javatools\\JMXOPER.jar")
        #jpype.startJVM(jvm_path, "-ea", "-Djava.class.path=%s" % (jar_path))
        #JmxTools = jpype.JClass("com.guo.auth.JavaTools")
        #jmx_tools = JmxTools()
        num_str = str(num)
        #msg = jmx_tools.authService(tmn_id, zk_url, port, ip, num_str, system_name)
        #log.info("授权的结果:"+msg)
        #jpype.shutdownJVM()
    except Exception as e:
        #jpype.shutdownJVM()
        log.error('tmn_id:%s zk_url:%s port:%s ip:%s num_str:%s system_name:%s , %s', tmn_id, zk_url, port, ip, num,
                  system_name, e)


if __name__ == '__main__':
    terminate_op_auth('9.1.6.247', '1099', 'ABS', 'ABS002', '400', '9.1.5.22:2181')
