# Generated by Django 3.1.4 on 2021-12-13 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db_models', '0006_merge_20211206_1833'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeploymentPlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan_name', models.CharField(help_text='部署计划名称', max_length=32, verbose_name='部署计划名称')),
                ('host_num', models.IntegerField(default=0, help_text='主机数量', verbose_name='主机数量')),
                ('product_num', models.IntegerField(default=0, help_text='产品数量', verbose_name='产品数量')),
                ('service_num', models.IntegerField(default=0, help_text='服务数量', verbose_name='服务数量')),
                ('create_user', models.CharField(help_text='创建用户', max_length=16, verbose_name='创建用户')),
                ('operation_uuid', models.CharField(help_text='部署操作uuid', max_length=36, verbose_name='部署操作uuid')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='创建时间', null=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '部署计划',
                'verbose_name_plural': '部署计划',
                'db_table': 'omp_deployment_plan',
            },
        ),
    ]