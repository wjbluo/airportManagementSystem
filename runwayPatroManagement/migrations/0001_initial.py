# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-12-20 17:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='runwaysDamageData',
            fields=[
                ('damageNo', models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='异常')),
                ('runwayType', models.CharField(max_length=1, verbose_name='道面类型')),
                ('damageType', models.CharField(max_length=2, verbose_name='损害类型')),
                ('partitionCode', models.CharField(max_length=10, verbose_name='分区编号')),
                ('Row', models.CharField(max_length=10, verbose_name='板块行编号')),
                ('Col', models.CharField(max_length=10, verbose_name='板块列编号')),
                ('X', models.CharField(max_length=10, verbose_name='X坐标')),
                ('Y', models.CharField(max_length=10, verbose_name='Y坐标')),
                ('location', models.CharField(max_length=50, verbose_name='位置区域')),
                ('damageLength', models.DecimalField(decimal_places=0, default=0, max_digits=5, verbose_name='损害长度')),
                ('damageWidth', models.DecimalField(decimal_places=0, default=0, max_digits=5, verbose_name='损害宽度')),
                ('damageArea', models.DecimalField(decimal_places=2, default=0, max_digits=5, verbose_name='损害面积')),
                ('desc', models.CharField(max_length=200, verbose_name='备注说明')),
            ],
            options={
                'verbose_name': '跑滑巡视异常记录',
                'verbose_name_plural': '跑滑巡视异常记录',
            },
        ),
        migrations.CreateModel(
            name='runwaysPatroData',
            fields=[
                ('taskNo', models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='任务编号')),
                ('weather', models.CharField(max_length=100, verbose_name='天气')),
                ('patroDate', models.CharField(max_length=4, verbose_name='巡视日期')),
                ('patroCount', models.CharField(max_length=10, verbose_name='巡视次数')),
                ('patroMainCar', models.CharField(max_length=10, verbose_name='巡视主车')),
                ('mainCarPerson', models.CharField(max_length=100, verbose_name='主车人员')),
                ('mainCarDirection', models.CharField(max_length=10, verbose_name='主车方向')),
                ('mainCarTrail', models.CharField(max_length=100, verbose_name='主车巡视轨迹')),
                ('sideCar', models.CharField(max_length=10, verbose_name='巡视副车')),
                ('sideCarPerson', models.CharField(max_length=100, verbose_name='副车人员')),
                ('sideCarDirection', models.CharField(max_length=10, verbose_name='副车方向')),
                ('sideCarTrail', models.CharField(max_length=100, verbose_name='副车巡视轨迹')),
                ('carryGoods', models.CharField(max_length=10, verbose_name='携带物品')),
                ('notifiedTowerTime', models.CharField(max_length=50, verbose_name='通知塔台时间')),
                ('notifiedFlyingTime', models.CharField(max_length=50, verbose_name='通知飞管时间')),
                ('entryTime', models.CharField(max_length=10, verbose_name='进入巡视时间')),
                ('exitWaitingPosition', models.CharField(max_length=10, verbose_name='退出等待位置')),
                ('exitWaitingTime', models.CharField(max_length=50, verbose_name='退出等待时间')),
                ('Re_entryTime', models.CharField(max_length=10, verbose_name='再次进入巡视时间')),
                ('exitNotifiedTowerTime', models.CharField(max_length=50, verbose_name='退出通知塔台时间')),
                ('exitNotifiedFlyingTime', models.CharField(max_length=50, verbose_name='退出通知飞管时间')),
                ('exitTime', models.CharField(max_length=10, verbose_name='结束巡视时间')),
                ('noPatroReason', models.CharField(max_length=200, verbose_name='未巡视原因')),
                ('flag', models.CharField(max_length=1, verbose_name='标志位')),
                ('runways', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.runway_baseData', verbose_name='巡视跑道')),
            ],
            options={
                'verbose_name': '跑滑巡视记录',
                'verbose_name_plural': '跑滑巡视记录',
            },
        ),
        migrations.AddField(
            model_name='runwaysdamagedata',
            name='Patro',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='runwayPatroManagement.runwaysPatroData', verbose_name='巡视记录'),
        ),
    ]
