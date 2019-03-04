from django.db import models
from django.utils.html import format_html

# 创建产品分类表
class Type(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='序号')
    type_name = models.CharField(max_length=20, verbose_name='产品类型')

    # 设置返回值
    def __str__(self):
        return self.type_name


# 创建产品信息表
class Product(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='序号')
    name = models.CharField(max_length=50, verbose_name='名称')
    weight = models.CharField(max_length=20, verbose_name='重量')
    size = models.CharField(max_length=20, verbose_name='尺寸')
    type = models.ForeignKey(Type, on_delete=models.CASCADE, verbose_name='产品类型')

    # 设置返回值
    def __str__(self):
        return self.name

    class Meta:
        # 如只设置verbose_name，在Admin会显示为“产品信息s”
        verbose_name = '产品信息'
        verbose_name_plural = '产品信息'

    # 自定义函数，设置字体颜色
    def colored_type(self):
        if '手机' in self.type.type_name:
            color_code = 'red'
        elif '平板电脑' in self.type.type_name:
            color_code = 'blue'
        elif '智能穿戴' in self.type.type_name:
            color_code = 'green'
        else:
            color_code = 'yellow'
        return format_html(
                '<span style="color: {};">{}</span>',
                color_code,
                self.type
        )
    # 设置Admin的标题
    colored_type.short_description = '带颜色的产品类型'



# class Performer(models.Model):
#     id = models.IntegerField(primary_key=True)
#     name = models.CharField(max_length=20)
#     nationality = models.CharField(max_length=20)
#
#
# class Program(models.Model):
#     id = models.IntegerField(primary_key=True)
#     performer = models.ManyToManyField(Performer)
#     name = models.CharField(max_length=20)
