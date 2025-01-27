# !/usr/bin/python3
# -*-coding:utf-8-*-
# Author: len chen
# CreateDate: 2021/11/8 8:00 下午
# Description:
from utils.prometheus.prometheus import Prometheus


class ServiceKafkaCrawl(Prometheus):
    """
    查询 prometheus kafka 指标
    """
    def __init__(self, env, instance):
        self.ret = {}
        self.basic = []
        self.env = env              # 环境
        self.instance = instance    # 主机ip
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
               f"job='kafkaExporter'}}"
        self.ret['service_status'] = self.unified_job(*self.query(expr))

    def run_time(self):
        """运行时间"""
        expr = f"max(max_over_time(redis_uptime_in_seconds{{env='{self.env}'," \
               f"instance=~'{self.instance}'}}[5m]))"
        _ = self.unified_job(*self.query(expr))
        _ = float(_) if _ else 0
        minutes, seconds = divmod(_, 60)
        hours, minutes = divmod(minutes, 60)
        self.ret['run_time'] = f"{int(hours)}小时{int(minutes)}分钟{int(seconds)}秒"

    def cpu_usage(self):
        """kafka cpu使用率"""
        expr = f"rate(namedprocess_namegroup_cpu_seconds_total{{" \
               f"groupname=~'redis', instance=~'{self.instance}'," \
               f"mode='system'}}[5m]) * 100"
        val = self.unified_job(*self.query(expr))
        val = round(float(val), 4) if val else 0
        self.ret['cpu_usage'] = f"{val}%"

    def mem_usage(self):
        """kafka 内存使用率"""
        expr = f"100 * (redis_memory_used_bytes{{env=~'{self.env}'," \
               f"instance=~'{self.instance}'}}  / " \
               f"redis_memory_max_bytes{{env=~'{self.env}'," \
               f"instance=~'{self.instance}'}})"
        val = self.unified_job(*self.query(expr))
        val = round(float(val), 4) if val else 0
        self.ret['mem_usage'] = f"{val}%"

    def conn_num(self):
        """连接数量"""
        expr = f"redis_connected_clients{{env='{self.env}'," \
               f"instance=~'{self.instance}'}}"
        self.basic.append({
            "name": "conn_num", "name_cn": "连接数量",
            "value": self.unified_job(*self.query(expr))}
        )

    def max_memory(self):
        """最大内存"""
        expr = f"redis_memory_max_bytes{{env=~'{self.env}'," \
               f"instance=~'{self.instance}'}})"
        self.basic.append({
            "name": "max_memory", "name_cn": "最大内存",
            "value": self.unified_job(*self.query(expr))}
        )

    def run(self):
        """统一执行实例方法"""
        target = ['service_status', 'run_time', 'cpu_usage', 'mem_usage',
                  'conn_num', 'max_memory']
        for t in target:
            if getattr(self, t):
                getattr(self, t)()
