# Generated by Django 3.1.4 on 2022-02-25 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db_models', '0021_customscript'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlertRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('env_id', models.IntegerField(default=1, verbose_name='环境id')),
                ('expr', models.TextField(verbose_name='监控指标表达式，报警语法')),
                ('threshold_value', models.FloatField(verbose_name='阈值的数值')),
                ('compare_str', models.CharField(max_length=64, verbose_name='比较符')),
                ('for_time', models.CharField(max_length=64, verbose_name='持续一段时间获取不到信息就触发告警')),
                ('severity', models.CharField(max_length=64, verbose_name='告警级别')),
                ('alert', models.TextField(verbose_name='标题，自定义摘要')),
                ('service', models.CharField(max_length=255, verbose_name='指标所属服务名称')),
                ('status', models.IntegerField(default=0, verbose_name='启用状态')),
                ('name', models.CharField(max_length=255, null=True, verbose_name='内置指标名称')),
                ('quota_type', models.IntegerField(choices=[(0, 'builtins'), (1, 'custom'), (2, 'log')], default=0, verbose_name='指标的类型')),
                ('labels', models.JSONField(null=True, verbose_name='额外指定标签')),
                ('summary', models.TextField(null=True, verbose_name='描述, 告警指标描述')),
                ('description', models.TextField(null=True, verbose_name='描述, 告警指标描述')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='告警规则入库时间')),
                ('update_time', models.DateTimeField(auto_now_add=True, verbose_name='告警规则更新时间')),
            ],
            options={
                'verbose_name': '自定义告警规则',
                'verbose_name_plural': '自定义告警规则',
                'db_table': 'omp_alert_ruler',
            },
        ),
        migrations.CreateModel(
            name='Rule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='指标名称')),
                ('expr', models.TextField(verbose_name='监控指标表达式，报警语法')),
                ('service', models.CharField(max_length=255, verbose_name='服务名称')),
                ('description', models.TextField(null=True, verbose_name='描述')),
            ],
            options={
                'verbose_name': '规则表达式',
                'verbose_name_plural': '规则表达式',
                'db_table': 'omp_rule',
            },
        ),
    ]