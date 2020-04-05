from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    # 显示字段
    list_display = ['name', 'introduction', 'img']
    # 排序规则
    ordering = ['-create_time']
    # 每页显示数量
    list_per_page = 25
    # 点击可编辑
    list_display_links = ['name']

@admin.register(Nav)
class NavAdmin(admin.ModelAdmin):
    # 显示字段
    list_display = ['name', 'sort']
    # 排序规则
    ordering = ['sort']
    # 每页显示数量
    list_per_page = 25
    # 点击可编辑
    list_display_links = ['name']

@admin.register(Recommend)
class RecommendAdmin(admin.ModelAdmin):
    # 显示字段
    list_display = ['name']
    # 每页显示数量
    list_per_page = 25
    # 点击可编辑
    list_display_links = ['name']

@admin.register(Attribution)
class AttributionAdmin(admin.ModelAdmin):
    # 显示字段
    list_display = ['name']
    # 每页显示数量
    list_per_page = 25
    # 点击可编辑
    list_display_links = ['name']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # fields = (('name', 'attribution'), 'pid')
    # 显示字段
    list_display = ['id', 'name', 'pid', 'attribution', 'sort']
    # 排序规则
    ordering = ['attribution', 'pid', 'sort']
    # 每页显示数量
    list_per_page = 25
    # 点击可编辑
    # list_display_links = ['name']
    # 筛选条件
    list_filter = ['attribution']
    # 列表页点击可编辑
    #list_editable = ['pid', 'sort']

    # 空值展示样式
    empty_value_display = ''

    list_max_show_all = 200
    search_fields = ('name', 'attribution__name')

@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    # 显示字段
    list_display = ['name', 'recommend', 'attribution', 'sort']
    # 排序规则
    ordering = ['sort']
    # 每页显示数量
    list_per_page = 25
    # 点击可编辑
    list_display_links = ['name']