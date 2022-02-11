# -*- coding: utf-8 -*-
# Project: tools
# Author: jon.liu@yunzhihui.com
# Create time: 2022-02-08 16:04
# IDE: PyCharm
# Version: 1.0
# Introduction:

"""
实用工具数据库表结构
原始小工具校验前地址：omp/package_hub/tool/verify_tar/
原始小工具tar包地址：omp/package_hub/tool/tar/
小工具解压后包地址: omp/package_hub/tool/folder/
上传的文件地址: omp/package_hub/tool/upload_data/
运行产生的的文件地址: omp/package_hub/tool/download_data/
"""
import os

from django.db import models

from db_models.mixins import TimeStampMixin
from utils.plugin.public_utils import timedelta_strftime


class ToolInfo(TimeStampMixin):
    """ 实用工具基本信息记录表 """

    objects = None

    KIND_MANAGEMENT = 0
    KIND_CHECK = 1
    KIND_SECURITY = 2
    KIND_OTHER = 3
    TOOL_KIND_CHOICES = (
        (KIND_MANAGEMENT, "管理工具"),
        (KIND_CHECK, "检查工具"),
        (KIND_SECURITY, "安全工具"),
        (KIND_OTHER, "其他工具")
    )

    SCRIPT_TYPE_PYTHON3 = 0
    SCRIPT_TYPE_SHELL = 1
    SCRIPT_TYPE_CHOICES = (
        (SCRIPT_TYPE_PYTHON3, "python3"),
        (SCRIPT_TYPE_SHELL, "shell")
    )

    OUTPUT_TERMINAL = 0
    OUTPUT_FILE = 1
    OUTPUT_TYPE_CHOICES = (
        (OUTPUT_TERMINAL, "终端输出"),
        (OUTPUT_FILE, "文件输出")
    )

    name = models.CharField(
        max_length=128, null=False,
        blank=False, help_text="实用工具名称")
    kind = models.IntegerField(
        "实用工具分类", choices=TOOL_KIND_CHOICES,
        default=0, help_text="实用工具分类")
    script_type = models.IntegerField(
        "脚本类型", choices=SCRIPT_TYPE_CHOICES,
        default=0, help_text="脚本类型")
    # 脚本执行的目标对象，主机为host，服务为服务名称
    target_name = models.CharField(
        "脚本执行的目标对象",
        max_length=128,
        default='host',
        help_text="脚本执行的目标对象")
    # 原始脚本包MD5值，预留字段
    source_package_md5 = models.CharField(
        "源码包md5值", max_length=32,
        blank=True, null=True, help_text="源码包md5值")
    # 原始tar包相对路径，package_hub/tool/tar/{kafka_tool.tar.gz}
    source_package_path = models.CharField(
        "源码包相对路径", max_length=128, null=False)
    # 存储实用工具目录路径，如package_hub/tool/folder/{kafka-package_md5}
    tool_folder_path = models.CharField(
        "实用工具目录相对路径", max_length=128,
        null=False, blank=False, help_text="实用工具目录相对路径")
    # 存储脚本路径，如kafka.py
    script_path = models.CharField(
        "脚本相对路径", max_length=128,
        null=False, blank=False, help_text="脚本相对路径")
    send_package = models.JSONField(
        "需要发送的文件相对路径", max_length=128,
        default=list, help_text="需要发送的文件相对路径")
    # 存储readme的内容
    readme_info = models.TextField(
        "readme信息", null=True, blank=True, help_text="readme信息")
    # 如果脚本需要模板文件，那么该模板文件的相对路径需要存储到下面字段中
    # 此字段存储列表类型数据
    template_filepath = models.JSONField(
        "模板文件相对路径", default=list, help_text="模板文件相对路径")
    # 在执行对象为服务时需要获取除ServiceConnectInfo中以外的信息
    # ["service_port", "metrics_port"]
    obj_connection_args = models.JSONField("目标对象连接信息", default=list, )
    # 存储脚本执行参数，存储列表类型数据
    # 在入库时需要对每个参数的类型进行校验（前端展示效果）
    script_args = models.JSONField("脚本执行参数", default=list)
    # 脚本输出的类型，终端/文件
    output = models.IntegerField(
        "脚本的输出类型", choices=OUTPUT_TYPE_CHOICES,
        default=0, help_text="脚本的输出类型")
    desc = models.TextField("描述信息", help_text="描述信息")

    class Meta:
        """元数据"""
        db_table = "omp_tool_info"
        verbose_name = verbose_name_plural = "实用工具基本信息表"

    def load_default_form(self):
        return "runuser, timeout, task_name, target_name"

    # 目前支持的参数类型
    # "select"：单选, "select_multiple"：多选, "file"：文件, "input"：单行文本

    @property
    def logo(self):
        # http://10.0.0.1:19001/tool/{logo_path}
        return os.path.join(self.tool_folder_path, "logo.svg")


class ToolExecuteMainHistory(models.Model):
    """ 实用工具执行记录 """

    objects = None

    STATUS_READY = 0
    STATUS_RUNNING = 1
    STATUS_SUCCESS = 2
    STATUS_FAILED = 3
    STATUS_TYPE_CHOICES = (
        (STATUS_READY, "待执行"),
        (STATUS_RUNNING, "执行中"),
        (STATUS_SUCCESS, "执行成功"),
        (STATUS_FAILED, "执行失败"),
    )

    tool = models.ForeignKey(
        ToolInfo, on_delete=models.CASCADE, help_text="实用工具对象")
    task_name = models.CharField(
        "任务标题", max_length=128, null=True, help_text="任务标题")
    operator = models.CharField(
        "操作人", max_length=128, null=True, blank=True, help_text="操作人")
    status = models.IntegerField(
        "main执行状态", choices=STATUS_TYPE_CHOICES,
        default=0, help_text="main执行状态")
    start_time = models.DateTimeField(
        "开始时间", null=True, auto_now_add=True, help_text="开始时间")
    end_time = models.DateTimeField(
        "结束时间", null=True, auto_now=True, help_text="结束时间")
    form_answer = models.JSONField("任务表单提交结果", default=dict)

    class Meta:
        """元数据"""
        db_table = "omp_tool_execute_main_history"
        verbose_name = verbose_name_plural = "实用工具执行记录"

    def duration(self):
        if not all([self.end_time, self.start_time]):
            return "-"
        return timedelta_strftime(self.end_time - self.start_time)


class ToolExecuteDetailHistory(TimeStampMixin):
    """ 实用工具执行详情记录 """

    objects = None

    STATUS_READY = 0
    STATUS_RUNNING = 1
    STATUS_SUCCESS = 2
    STATUS_FAILED = 3
    STATUS_TYPE_CHOICES = (
        (STATUS_READY, "待执行"),
        (STATUS_RUNNING, "执行中"),
        (STATUS_SUCCESS, "执行成功"),
        (STATUS_FAILED, "执行失败"),
    )

    main_history = models.ForeignKey(
        ToolExecuteMainHistory, on_delete=models.CASCADE,
        help_text="实用工具对象")
    # 脚本需要在某台主机上执行，此处代表该主机的ip地址
    target_ip = models.CharField(
        "目标IP地址", max_length=64,
        null=False, blank=False, help_text="目标IP地址")
    time_out = models.IntegerField("超时时间", default=60)
    run_user = models.CharField("执行用户", max_length=64, default="")
    status = models.IntegerField(
        "detail执行状态", choices=STATUS_TYPE_CHOICES,
        default=0, help_text="detail执行状态")
    # 脚本执行的参数详情信息
    execute_args = models.JSONField(
        "执行参数信息", default=dict, help_text="执行参数信息")
    execute_log = models.TextField("执行日志", help_text="执行日志")
    # 脚本有输出时使用,{"message": "", "file": ["a.txt", "b.log"]}
    # 执行脚本有返回写message，有receive_files写file，只写文件名
    output = models.JSONField("脚本输出内容", default=dict)

    class Meta:
        """元数据"""
        db_table = "omp_tool_execute_detail_history"
        verbose_name = verbose_name_plural = "实用工具执行详情表"

    def get_cmd_str(self):
        """
        获取执行命令
        :return: 命令字符串
        """
        return "/data/omp_salt_agent/env/bin/python3 --server " \
               " 10.0.14.157:9092 --role consumer" \
               " --input /data/omp_packages/tool/kafka/input.txt" \
               " --output /data/omp_packages/tool/kafka/output.txt"

    def get_send_files(self):
        """
        获取需要发送的文件
        :return: local_files：需要发送的文件，send_to：发送的位置
        """
        return {
            "local_files": ["/data/omp/package_hub/tool/upload_data/input.txt"],
            "send_to": "/data/omp_packages/tool/kafka/"
        }

    def get_receive_files(self):
        """
        获取需要接受的文件
        :return: output_files：需要接受的文件，receive_to：接收文件的存放位置
        """
        return {
            "output_files": ["/data/omp_packages/tool/kafka/output.txt", ],
            "receive_to": "/data/omp/package_hub/tool/download_data/"
        }
