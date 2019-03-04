from django.contrib import admin
from index import models
# 修改title和header
admin.site.site_title = 'MyDjango后台管理'
admin.site.site_header = 'MyDjango'

# 方法一
# 将模型直接注册到admin后台
# admin.site.register(models.Product)

# 方法二
# 自定义ProductAdmin类并继承ModelAdmin
# 注册方法一
# 使用Python装饰器将ProductAdmin和模型Product绑定并注册到后台
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    # 设置显示的字段，用于Admin后台数据的表头设置
    list_display = ['id', 'name', 'weight', 'size', 'type']
    # 设置可搜索的字段并在Admin后台数据生成搜索框
    # 如有外键，应使用双下划线连接两个模型的字段
    search_fields = ['id', 'name', 'type__type_name']
    # 设置过滤器
    # 在后再数据的右侧生成导航栏
    # 如有外键，应使用双下划线连接两个模型的字段
    list_filter = ['name', 'type__type_name']
    # 设置排序方式
    # ['id']为升序，['-id']为降序
    ordering = ['id']
    # 设置时间选择器
    # 如字段中有时间格式才可以使用
    # date_hierarchy = models.Field
    # 在添加新数据时，设置可添加数据的字段
    fields = ['name', 'weight', 'size', 'type']
    # 设置可读字段，在修改或新增数据时使其无法设置
    readonly_fields = ['name']

# 注册方法二
# admin.site.register(models.Product, ProductAdmin)
    list_display.append('colored_type')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'type':
            if not request.user.is_superuser:
                kwargs['queryset'] = models.Type.objects.filter(id__lt=4)
        return super(admin.ModelAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super(ProductAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(if__lt=6)

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            self.readonly_fields = []
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        if change:
            # 获取当前用户名
            user = request.user
            # 使用模型获取数据，pl代表具有主键属性的字段
            name = self.model.objects.get(pk=obj.pk).name
            # 使用表单获取数据
            weight = form.cleaned_data['weight']
            # 写入日志文件
            f = open('d://我的文档//MyDjango_log.txt', 'a')
            f.write('产品:' + str(name) + ',被用户:' + str(user) + '修改' + '\r\n')
            f.close()
        else:
            pass
        # 使用super可使自定义save_model既保留父类已有的功能又能添加自定义功能
        super(ProductAdmin, self).save_model(request, obj, form, change)
