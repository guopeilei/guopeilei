from django.shortcuts import render
from django.shortcuts import HttpResponse
import json
from zktools.service import esbservice
import logging.config
from zktools.orm.serviceEnv import ServiceEnv
from zktools.javatools.operjava import *

from django.views.decorators.clickjacking import xframe_options_sameorigin

log = logging.getLogger(__name__)


def zk_tools(request):
    return render(request, 'zk_tools.html')


def all_env(request):
    global service_env
    if service_env is None:
        service_env = esbservice.init()
    env_list = []
    count = 1
    for env in service_env.envs:
        if count == 1:
            env_info = {"id": count, "text": env.name, "selected": "true"}
        else:
            env_info = {"id": count, "text": env.name}
        count = count+1
        env_list.append(env_info)
    env_list = json.dumps(env_list)
    return HttpResponse(env_list)


def get_all_flow_env(request):
    global service_env
    if service_env is None:
        service_env = esbservice.init()
    env_list = [
        {"id": "0", "text": "选择全部环境", "selected": "true"}]
    count = 1
    for env in service_env.envs:
        env_info = {"id": count, "text": env.name}
        count = count+1
        env_list.append(env_info)
    env_list = json.dumps(env_list)
    return HttpResponse(env_list)


service_env = None


@xframe_options_sameorigin
def syn_commit(request):
    """
    将一个环境上的服务同步到其他
    :param request:
    :return:
    """
    request.encoding = 'utf-8'
    global service_env
    if service_env is None:
        service_env = esbservice.init()
    service_env = esbservice.init()
    master_env = request.GET.get('master_envs')
    flow_env_list_str = request.GET.get('follow_envs')
    flow_env_list = []
    service_codes_list = []
    if flow_env_list_str is not None:
        flow_env_list = flow_env_list_str.split(",")
    service_codes_str = request.GET.get('service_codes')
    if service_codes_str is not None:
        service_codes_list = service_codes_str.split(",")
    my_master_env = None
    my_flow_env_list = []
    flag = False
    if flow_env_list_str is not None and '选择全部环境' in flow_env_list_str:
        flag = True
    for my_env in service_env.envs:
        if master_env in my_env.name:
            my_master_env = my_env
        if flag:
            my_flow_env_list.append(my_env)
            continue
        else:
            for my_follow_name in flow_env_list:
                if my_follow_name in my_env.name:
                    my_flow_env_list.append(my_env)
                    break
    service_data = esbservice.get_master_data(my_master_env, service_codes_list)
    esbservice.move_data(my_flow_env_list, service_data, my_master_env)
    # 服务授权
#    esbservice.service_auth(env_list=my_flow_env_list, service_ids=service_codes_list)
    result = {"status": "success", "message": "执行成功"}
    result_json = json.dumps(result)
    return HttpResponse(result_json)






