from django.shortcuts import render,render_to_response,HttpResponse,HttpResponseRedirect
from utils import transFor_md5
from .models import *
from utils import check_code
from io import BytesIO
import json
from main.models import airport_baseData
from datetime import datetime
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib import auth
# Create your views here.

def create_code_img(request):
    f = BytesIO()  # 直接在内存开辟一点空间存放临时生成的图片

    img, code = check_code.create_validate_code()  # 调用check_code生成照片和验证码
    request.session['check_code'] = code  # 将验证码存在服务器的session中，用于校验
    img.save(f, 'PNG')  # 生成的图片放置于开辟的内存中
    return HttpResponse(f.getvalue())  # 将内存的数据读取出来，并以HttpResponse返回


def login(request):
    ret = {'status': False, 'message': '', 'data': None,'next_to':''}
    if request.method=='POST': # 当表单提交时
        try:
            input_code = request.POST['check_code']
            userId =  request.POST['account']
            password =  request.POST['psd']
            if(input_code.upper() == request.session['check_code'].upper()):
                user = auth.authenticate(username=userId, password=password)
                # password_md5 = transFor_md5.transfor_md5(password)
                # user = LoginUsers.objects.filter(userId=userId,psd=password_md5)
                if user and user.is_active:
                    ret['status']=True
                    # user.update(lastLandingTime=datetime.now())

                    # 获得当前机场ID
                    response = HttpResponseRedirect('/component/')
                    currentAirport = airport_baseData.objects.all().first()
                    # 将username写入浏览器cookie,失效时间为3600
                    response.set_cookie('currentAirportId', currentAirport.id)

                    auth.login(request, user)
                    # 进入主页
                    return response
                else:
                    context = {
                        'message': '账号密码错误或该账号已被冻结。'
                    }
                    return render(request, 'login.html', context)
            else:
                context = {
                    'message': '验证码不正确。'
                }
                return render(request, 'login.html',context)
        except Exception as e:
            ret['message'] = str(e)
        ret_str = json.dumps(ret)
        return HttpResponse(ret_str)
    else:
        # context = {
        #     'message': ''
        # }
        return render(request, 'login.html')  # render里context将自带crsf数据

def logout(request):
    auth.logout(request)
    response = HttpResponseRedirect('/account/login/')
    response.delete_cookie('currentAirportId')
    return response

def modifyPwd(request):
    context={

    }
    return render(request, 'modify_pwd_dialog.html', context)  # render里context将自带crsf数据

def modifyPsdSubmit(request):
    ret = {'status': False, 'message': '', 'data': None}
    if request.method == 'POST':
        try:
            post_data = request.POST.get('post_data', None)
            post_data_dict = json.loads(post_data)

            zcEmail = post_data_dict['zcEmail']
            # OranPsd = post_data_dict['OranPsd']
            NewPsd = post_data_dict['NewPsd']
            email = request.user.email
            if email != zcEmail:
                ret['message'] = '未注册邮箱，请检查。'
            else:
                user = request.user
                user.set_password(NewPsd)
                user.save()
                auth.logout(request)
                ret['message'] = '修改密码成功。请重新登录。'
                ret['status'] = True
        except Exception as e:
            ret['message'] = str(e)
        ret_str = json.dumps(ret)
        return HttpResponse(ret_str)
    return render(request, 'modify_pwd_dialog.html')  # render里context将自带crsf数据