import tkinter.messagebox
import os


class EnvInfo:
    def __init__(self, zk_url, db_url, name):
        self.zk_url = zk_url
        self.db_url = db_url
        self.name = name


class ServiceEnv:
    def __init__(self, cfg):
        self.envs = []
        envs_json = cfg["envs"]
        for env in envs_json:
            name = envs_json[env]["name"]
            zk_url = envs_json[env]["zkurl"]
            db_url = envs_json[env]["db2url"]
            env_info = EnvInfo(zk_url, db_url, name)
            self.envs.append(env_info)



