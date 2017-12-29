from django.db import models

# Create your models here.
# 用户表   已改为django 自带表
# class LoginUsers(models.Model):
#     userId = models.CharField(max_length=13, verbose_name='员工编号')
#     userName = models.CharField(max_length=10, verbose_name='员工姓名')
#     registerTime = models.CharField(max_length=10, verbose_name='注册时间')
#     lastLandingTime = models.DateTimeField(auto_now_add=True)
#     psd = models.CharField(max_length=128, verbose_name='密码')
#
#
#     def __str__(self):
#         return self.userId+self.userName
#
#     class Meta:
#         verbose_name='用户'
#         verbose_name_plural = verbose_name
#         ordering = ['userId']