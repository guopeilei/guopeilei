import paramiko
import logging
import sys
import os

# 加入日志
# 获取logger实例
logger = logging.getLogger("baseSpider")
# 指定输出格式
formatter = logging.Formatter('%(asctime)s\
              %(levelname)-8s:%(message)s')
# 文件日志
file_handler = logging.FileHandler("operation_theServer.log")
file_handler.setFormatter(formatter)
# 控制台日志
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)

# 为logge添加具体的日志处理器
logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.setLevel(logging.INFO)


class TheServerHelper:
    """
    初始化函数构造
    其中remote有两个作用，除了字面的服务器路径外
    还作为执行的语句
    """
    def __init__(self, server_ip, username, password, remote, local_dir='', ftp_type='', port=22):
        self.server_ip = server_ip
        self.username = username
        self.password = password
        self.port = port
        self.ftp_type = ftp_type
        self.remote = remote
        self.local_dir = local_dir

    # SSH连接服务器，用于命令执行
    def ssh_connection_server(self):
        try:
            # 创建SSH对象
            sf = paramiko.SSHClient()
            # 允许连接不在know_hosts文件中的主机
            sf.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # 连接服务器
            sf.connect(hostname=self.server_ip, port=self.port, username=self.username,
                       password=self.password)
            stdin, stdout, stderr = sf.exec_command(self.remote)
            result = stdout.read()
            print(result)
        except:
            logger.error("SSHConnection" +self.server_ip+"failed!")
            return False
        return True

    # FTP连接服务器，用于文件上传和下载
    def ftp_connection_server(self):
        try:
            # 创建ftp对象
            sf = paramiko.Transport(self.server_ip, self.port)
            sf.connect(username=self.username, password=self.password)
            sftp = paramiko.SFTPClient.from_transport(sf)
        except:
            logger.error("FTPConnection "+self.server_ip+" failed!")
            return False
        """定义参数ftpType：
                    ftpType=1    单个文件从其他服务器向本地下载
                    ftpType=2    单个文件向服务器上传
                    ftpType=3    文件夹下内容下载
                    ftpType=4    文件夹下内容上传"""
        local_path = os.path.dirname(self.local_dir)
        if self.ftp_type == 1:
            if not os.path.exists(local_path):
                os.makedirs(local_path)
                sftp.get(self.remote, self.local_dir)
                sf.close()
                return True
        elif self.ftp_type == 2:
            sftp.put(self.local_dir, self.remote)
            sf.close()
            return True
        else:
            logger.error("服务器路径："+self.remote+"本地路径："+self.local_dir)
            return False
