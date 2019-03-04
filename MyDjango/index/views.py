import csv

from django.shortcuts import render, redirect
from django.http import HttpResponse
from index import models
from index import form

# def index(request):
#     type_list = models.Product.objects.values('type').distinct()
#     name_list = models.Product.objects.values('name', 'type')
#     context = {'title': "首页", 'type_list': type_list, 'name_list': name_list}
#     return render(request, 'index.html', context=context, status=200)
#
#
# views.py的mydate函数
def mydate(request, year):
    return render(request, 'myyear.html')


def myyear_dict(request, year, month):
    return render(request, 'myyear_dict.html', {'month': month})


def download(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;  filename="somefilename.csv"'
    writer = csv.writer(response)
    writer.writerow(['First row', 'A', 'B', 'C'])
    return response


def login(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        # 绝对路径，完整的地址信息
        # return redirect('http://127.0.0.1:8000/')
        # 相对路径，代表首页地址
        return redirect('/')
    else:
        if request.GET.get('name'):
            name = request.GET.get('name')
        else:
            name = 'Everyone'
        return HttpResponse('username is ' + name)


# views.py 代码。 将表单ProductForm实例化并将其传递到模板中生成网页内容
# def index(request):
#     product = form.ProductForm()
#     return render(request, 'data_form.html', locals())
def index(request):
    # GET请求
    if request.method == "GET":
        product = form.ProductForm()
        return render(request, 'data_form.html', locals())
    # POST请求
    else:
        product = form.ProductForm(request.POST)
        if product.is_valid():
            # 获取网页控件name的数据
            # 方法1：
            name = product['name']
            # 输出<input type="text" name="name" value="1" maxlength="20" id="id_name" class="c1" required />
            # 方法2：
            # cleaned_data将控件name的数据进行清洗，转换成Python数据类型
            cname = product.cleaned_data['name']
            print(name)
            print(cname)
            return HttpResponse('提交成功')
        else:
            # 将错误信息输出，error_msg是错误信息以json格式输出
            error_msg = product.errors.as_json()
            print(error_msg)
            return render(request, 'data_form.html', locals())


def models_index(request, id):
    if request.method == "GET":
        instance = models.Product.objects.filter(id=id)
        # 判断数据是否存在
        if instance:
            product = form.ProductModelForm(instance=instance[0])
        else:
            product = form.ProductModelForm()
        return render(request, 'data_form.html', locals())
    else:
        product = form.ProductModelForm(request.POST)
        if product.is_valid():
            # 获取weight的数据，并通过clean_weight进行清洗，转换成屁哟通红数据类型
            weight = product.cleaned_data['weight']
            # 数据保存方法一
            # 直接将数据保存到数据库
            # product.save()
            # 数据保存方法二
            # save方法设置commit = False，将生成数据库对象product_db，然后对该对象的属性值修改并保存
            product_db = product.save(commit=False)
            product_db.name = '我的iPhone'
            product_db.save()
            # 数据保存方法三
            # save_m2m() 方法用用于保存ManyToMany的数据类型
            # product.save_m2m()
            return HttpResponse('提交成功！weight清洗后的数据为：' + weight)
        else:
            # 将错误信息输出，error_msg是将错误信息以json格式输出
            error_msg = product.errors.as_json()
            print(error_msg)
            return render(request, 'data_form.html', locals())
