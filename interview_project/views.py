# encoding: utf-8
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import json
import yaml
from interview_project import models
import shortuuid
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
import re
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required


def sign_up(request):
    return render(request, "sign-up.html")


def userlogin(request):
    if request.method == 'POST':

        # username = request.POST.get('username')
        username = 'zying'
        password = request.POST.get('password')
        next_url = request.POST.get('next')
        if not next_url:
            next_url = reverse('manage')
        user = authenticate(request,username=username,password=password)
        if user:
            login(request, user)
            msg = {"msg": '登录成功', 'url': next_url, "code": 0}
        else:
            msg = {"msg": '登录失败', 'code': 1}
        return HttpResponse(json.dumps(msg), content_type="application/json")
    else:
        next_url = request.GET.get('next')
        next_url = next_url if all([next_url]) else reverse('manage')
        if request.user:
            if request.user.is_authenticated:
                return HttpResponseRedirect(next_url)
        return render(request, "login.html", {'next': next_url})


def userlogout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


def index(request):
    return render(request, 'index.html')


def create_cluster(request):
    return render(request, 'create_cluster.html')


def connection_cluster(request):
    return render(request, 'connection_cluster.html')


@login_required
def manage(request):
    return render(request, 'manage.html')


@login_required
def template_mange(request):
    if request.method == 'GET':
        return render(request, "template_manage.html")
    else:
        data = []
        key = request.POST.get('key')
        if all([key]):
            msg = models.Yamls.objects.filter(name__contains=key)
        else:
            msg = models.Yamls.objects.all()
        for i in msg:
            template_info = models.Templates.objects.filter(id=i.template_id)
            if template_info:
                template_name = template_info.first().name
            else:
                template_name = '未知'
            message = dict()
            message['id'] = i.id
            message['name'] = i.name
            message['args'] = i.args
            message['template_name']= template_name
            data.append(message)
        count = len(data)
        response = {"code": 0, "msg": "success", "count": count, "data": data}
        return HttpResponse(json.dumps(response), content_type="application/json")


@login_required
def upload_file(request):
    if request.method == 'POST':
        my_file = request.FILES.get("file", None)
        if not my_file:
            return HttpResponse("no files for upload!")
        template_name = str(my_file.name).split('.')[0]
        content = str(my_file.read(), encoding='utf8')
        template_id = shortuuid.uuid()
        models.Templates.objects.create(id=template_id, name=template_name)
        number = 1
        for i in yaml.safe_load_all(content):
            yaml_id = shortuuid.uuid()
            yaml_name = '%s.%s' % (template_name, i['kind'])
            models.Yamls.objects.create(number=number, id=yaml_id, name=yaml_name, template_id=template_id,
                                        content=yaml.safe_dump(i), args=[])
            number += 1
    response = {"msg": "Upload file succeeded"}
    return HttpResponse(json.dumps(response), content_type="application/json")


@login_required
def detail_files(request):
    yaml_id = request.GET.get('yaml_id')
    data = models.Yamls.objects.filter(id=yaml_id)
    if data:
        yaml_info = data.first()
        msg = yaml_info.content
        return render(request, 'detail_file.html', {'yaml_info': yaml_info, 'msg': msg})
    else:
        return HttpResponse('data not found!')


@login_required
def del_file(request):
    yaml_id = request.POST.get('id')
    print(yaml_id)
    data = models.Yamls.objects.filter(id=yaml_id)
    data.delete()
    response = {"msg": "删除成功"}
    return HttpResponse(json.dumps(response), content_type="application/json")


@login_required
def edit_yaml(request):
    if request.method == 'GET':
        yaml_id = request.GET.get('yaml_id')
        data = models.Yamls.objects.filter(id=yaml_id).first()
        yaml_context = data.content
        return render(request, 'edit_yaml.html', {'yaml_context': yaml_context.replace('\n', '<br>'),
                                                  'yaml_id': data.id})
    else:

        yaml_content = request.POST.get('yaml_content')
        yaml_id = request.POST.get('yaml_id')
        result = [str(s).replace("{{", "").replace("}}", "")
                  for s in re.findall(r'\{{.*?}\}', yaml_content)]

        p = check_parameter(result)
        if type(p) == str:
            response = {'msg': p}
        else:
            old_content = models.Yamls.objects.filter(id=yaml_id).first().content
            old_args = [str(s).replace("{{", "").replace("}}", "")
                        for s in re.findall(r'\{{.*?}\}', old_content)]
            diff_args = list(set(result) - set(old_args))
            models.Yamls.objects.filter(id=yaml_id).update(content=yaml_content)
            response = {"msg": "更新成功"}
            if len(diff_args) > 0:
                template_id = models.Yamls.objects.filter(id=yaml_id).first().template_id
                models.ActionTemplates.objects.filter(template_id=template_id).update(status=1)
        return HttpResponse(json.dumps(response), content_type="application/json")


def check_parameter(parameter_list):
    print(parameter_list)
    for parameter in parameter_list:
        print(parameter)
        # 判断非空
        if not all([parameter]):
            return '参数名不得为空'
        if ' ' in parameter:
            return '修改失败，参数:"%s" 不能包含空格' % parameter
        # 判断异常字符
        if str(parameter).replace('_', '').isalnum():
            if parameter[0] in '0123456789':
                return '修改失败，参数:%s 格式异常，不能以数字开头~！' % parameter
            if any('\u4e00' <= char <= '\u9fff' for char in parameter):
                return '修改失败，参数:%s 格式异常，不能包含汉字~！' % parameter
        else:
            return '修改失败，参数:%s 存在异常字符' % parameter
    return True


@login_required
def template_list(request):
    if request.method == "GET":
        return render(request, 'template_list.html')
    else:
        data = []
        key = request.POST.get('key')
        if all([key]):
            msg = models.ActionTemplates.objects.filter(name__contains=key)
        else:
            msg = models.ActionTemplates.objects.all()
        for i in msg:
            message = dict()
            message['id'] = i.id
            message['name'] = i.name
            message['status'] = i.status
            data.append(message)
        count = len(data)
        response = {"code": 0, "msg": "success", "count": count, "data": data}
        return HttpResponse(json.dumps(response), content_type="application/json")


@login_required
def template_create(request):
    if request.method == "GET":
        template_info = models.Templates.objects.all()
        return render(request, 'create_template.html', {'template_info': template_info})
    else:
        args_data = json.loads(request.POST.get('args_info'))
        template_name = request.POST.get('template_name')
        template_id = request.POST.get('template_id')

        models.ActionTemplates.objects.create(id=shortuuid.uuid(), name=template_name, template_id=template_id,
                                              template_value=args_data)
        respone = {"code": 0, "msg": "创建成功"}
        return HttpResponse(json.dumps(respone), content_type="application/json")


@login_required
def template_edit(request):
    if request.method == "GET":
        action_template_id = request.GET.get('template_id')
        action_template_info = models.ActionTemplates.objects.filter(id=action_template_id).first()
        template_info = models.Templates.objects.all()
        return render(request, 'edit_template.html', {'template_info': template_info,
                                                      'action_template_info': action_template_info})
    else:
        action_template_id = request.POST.get('action_template_id')
        args_data = json.loads(request.POST.get('args_info'))
        template_name = request.POST.get('template_name')

        models.ActionTemplates.objects.filter(id=action_template_id).update(name=template_name,
                                                                            template_value=args_data,status=0)
        respone = {"code": 0, "msg": "更新成功"}
        return HttpResponse(json.dumps(respone), content_type="application/json")


@login_required
def get_template_args(request):
    if request.method == "POST":
        template_id = request.POST.get('template_id')
        data = []
        code = 0
        msg = 'success'
        template_info = models.Templates.objects.filter(id=template_id)
        if template_info:
            yaml_info = models.Yamls.objects.filter(template_id=template_id)
            for y in yaml_info:
                tmp = {'name': y.name, 'id': y.id}
                args = [str(s).replace("{{", "").replace("}}", "")
                        for s in re.findall(r'\{{.*?}\}', y.content)]
                if len(args) > 0:
                    tmp['args'] = args
                    data.append(tmp)
        else:
            code = -1
            msg = 'data not found'
        respone = {"code": code, "msg": msg, "data": data}
        return HttpResponse(json.dumps(respone), content_type="application/json")


def replace_template(args_info, yaml_obj):
    # 还有变量的内容
    yaml_content = str(yaml_obj.content)
    print(args_info)
    args_info = eval(args_info)
    args = [str(s).replace("{{", "").replace("}}", "")
            for s in re.findall(r'\{{.*?}\}', yaml_content)]
    format_dict = {}
    for arg in args:
        # arg 用户自定义的变量 例如 {{ name }}
        for a in args_info:
            # 用户前端填写的变量 例如 {'yaml_id': 'haUT6EbxLykNUjpH8Vn326', 'arg_name': 'name', 'value': '2'}
            if a['yaml_id'] == yaml_obj.id and arg == a['arg_name']:
                format_dict[arg] = a['value']
    return yaml_content.format().format(**format_dict)


@login_required
def template_detail(request):
    if request.method == "GET":
        template_id = request.GET.get('template_id')
        action_template_info = models.ActionTemplates.objects.filter(id=template_id).first()
        yaml_info = models.Yamls.objects.filter(template_id=action_template_info.template_id)
        result = []
        for y in yaml_info:
            yaml_content = replace_template(action_template_info.template_value, y)
            result.append(yaml_content)
        return render(request, 'detail_template.html', {'message': "---\n".join(result)})


@login_required
def del_template(request):
    template_id = request.POST.get('id')
    data = models.ActionTemplates.objects.filter(id=template_id)
    data.delete()
    response = {"msg": "删除成功"}
    return HttpResponse(json.dumps(response), content_type="application/json")






