import json
import re
import sys
from random import sample

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from apps.userper.models import Contact
from . import models


# 学习视图
class Learn(View):
    def get(self, request):
        p = request.GET.get('p', '')
        # 设置默认页面
        if not p:
            p = '1022910821149312'
        c = models.Course.objects.values('content', 'title', 'id').filter(p=p).first()

        nex = models.Course.objects.values('p').filter(id=(c.get('id') + 1)).first()
        previous = models.Course.objects.values('p').filter(id=c.get('id') - 1).first()
        if nex:
            ne = nex.get('p')
        else:
            ne = '1022910821149312'
        if previous:
            pr = previous.get('p')
        else:
            pr = '1022910821149312'

        content = '''<ul class="pager">
        <li class="previous"><a href="?p={}">&larr; 上一页</a></li>
        <li class="next"><a href="?p={}">下一页 &rarr;</a></li>
        </ul>'''.format(pr, ne)
        content = c.get('content') + content

        # 爬取所有文章存到数据库
        # import requests
        # from lxml import etree
        # from lxml.html import tostring
        # import time
        #
        # headers = {
        #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36",
        #     "Connection": "keep-alive",
        #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        #     "Accept-Language": "zh-CN,zh;q=0.9"
        # }
        #
        # url = 'https://www.liaoxuefeng.com/'
        #
        # a = requests.get('https://www.liaoxuefeng.com/wiki/1022910821149312', headers=headers)
        # s = etree.HTML(a.text)
        # n = s.xpath('//*[@id="x-offcanvas-left"]/div/div/ul[2]/li')
        # for i in n:
        #     path = i.xpath('a/@href')
        #     print(path)
        #     u = url + path[0]
        #     a = requests.get(u, headers=headers)
        #     code = a.apparent_encoding  # 获取编码格式
        #     s = etree.HTML(a.text)
        #     h = s.xpath('//*[@id="x-content"]/div[2]')[0]
        #     title = s.xpath('//*[@id="x-content"]/h4/text()')[0]
        #     con = tostring(h, encoding=code).decode(code)
        #
        #     nex = '0'
        #     print(re.sub(r'src = ".*?"', 'src = "/static/resource/picture/{}.jpg"'.format(nex), con))
        #     # print(title, path[0].split('/')[-1], tostring(h, encoding=code).decode(code))
        #
        #     # images = models.Course.objects.get_or_create(title=title, p=path[0].split('/')[-1],
        #     #                                              content=con)
        #     time.sleep(3)

        return render(request, 'index/learn.html', locals())


# js测试视图
def test(request):
    return render(request, 'index/test.html')


# 考试视图
@login_required  # 确认是否登录
@csrf_exempt
def exam(request):
    """
    1.判断学生是否登录,没有登录则重定向到登录
    2.渲染当前学生信息
    3.点击开始考试返回相应试题难度
    4.从数据库筛选10条对应难度试题返回给前端
    4.考试完成同步到用数据库保存成绩
    :param request:
    :return:
    """
    # 如果没有登录则重定向到登录
    if request.method == 'GET':
        p = int(request.GET.get('p', ''))
        if p == 0:
            contact = Contact.objects.all().filter(user_id=request.user.id)
            # 只返回html
            return render(request, 'index/exam.html', locals())
        # 随机筛选10道题
        con = models.Exam.objects.filter(is_delete=False, level=p).only('title').order_by('?')[:10]
        # 序列化
        lis = []
        for i in con:
            dic = {
                'title': i.title,
                'wor': i.wor,
                'level': i.level,
                'A': i.A,
                'B': i.B,
                'C': i.C,
                'D': i.D
            }
            lis.append(dic)
        return JsonResponse({'data': lis})
    # 更新成绩
    if request.method == 'POST':
        json_str = request.body
        if not json_str:
            return JsonResponse({'data': '空'})
        content = json.loads(json_str.decode('utf8'))
        contact = Contact.objects.only('id').filter(user_id=request.user.id)
        if content.get('level') == '1':
            contact.update(score_1=content.get('marks'))
        elif content.get('level') == '2':
            contact.update(score_2=content.get('marks'))
        elif content.get('level') == '3':
            contact.update(score_3=content.get('marks'))
        return JsonResponse({'data': 'ok'})
