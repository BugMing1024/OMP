# !/usr/bin/python3
# -*-coding:utf-8-*-
# Author: len chen
# CreateDate: 2021/11/8 8:00 下午
# Description:
import json
from utils.plugin.salt_client import SaltClient
from utils.prometheus.prometheus import Prometheus


class ServiceRocketmqCrawl(Prometheus):
    """
    查询 prometheus rocketmq 指标
    """
    def __init__(self, env, instance):
        self.ret = {}
        self.basic = []
        self.env = env              # 环境
        self.instance = instance    # 主机ip
        self._obj = SaltClient()
        Prometheus.__init__(self)

    @staticmethod
    def unified_job(is_success, ret):
        """
        实例方法 返回值统一处理
        :ret: 返回值
        :is_success: 请求是否成功
        """
        if is_success:
            if ret.get('result'):
                return ret['result'][0].get('value')[1]
            else:
                return 0
        else:
            return 0

    def service_status(self):
        """运行状态"""
        expr = f"up{{env='{self.env}', instance='{self.instance}', " \
               f"job='rocketmqExporter'}}"
        self.ret['service_status'] = self.unified_job(*self.query(expr))

    def run_time(self):
        """运行时间"""
        self.ret['run_time'] = '-'

    def cpu_usage(self):
        """cpu使用率"""
        self.ret['cpu_usage'] = f"-"

    def mem_usage(self):
        """内存使用率"""
        self.ret['mem_usage'] = f"-"

    def broker_tps(self):
        """生产消息数量/s"""
        expr = f"rocketmq_broker_tps{{env=~'{self.env}'," \
               f"instance=~'{self.instance}'}}"
        self.basic.append({
            "name": "broker_tps", "name_cn": "生产消息数量/s",
            "value": self.unified_job(*self.query(expr))}
        )

    def broker_qps(self):
        """消费消息数量/s"""
        expr = f"rocketmq_broker_qps{{env=~'{self.env}'," \
               f"instance=~'{self.instance}'}}"
        self.basic.append({
            "name": "broker_qps", "name_cn": "消费消息数量/s",
            "value": self.unified_job(*self.query(expr))}
        )

    def message_accumulation(self):
        """消息堆积量"""
        expr = f"rocketmq_message_accumulation{{env=~'{self.env}'," \
               f"instance=~'{self.instance}'}}"
        self.basic.append({
            "name": "message_accumulation", "name_cn": "消息堆积量",
            "value": self.unified_job(*self.query(expr))}
        )

    def salt_json(self):
        try:
            self._obj.salt_module_update()
            ret = self._obj.fun(self.instance, "rocketmq_check.main")
            if ret and ret[0]:
                ret = json.loads(ret[1])
            else:
                ret = {}
        except:
            ret = {}

        self.ret['cpu_usage'] = ret.get('cpu_usage', '-')
        self.ret['mem_usage'] = ret.get('mem_usage', '-')
        self.ret['run_time'] = ret.get('run_time', '-')
        self.ret['log_level'] = ret.get('log_level', '-')
        self.basic.append({"name": "max_memory", "name_cn": "最大内存",
                           "value": ret.get('max_memory', '-')})

    def run(self):
        """统一执行实例方法"""
        target = ['service_status', 'run_time', 'cpu_usage', 'mem_usage',
                  'thread_num', 'max_memory', 'salt_json']
        for t in target:
            if getattr(self, t):
                getattr(self, t)()
