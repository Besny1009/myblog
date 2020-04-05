from django.contrib import admin
from .models import Banner, Category, Tag, Tui, Artical, Link

#导入需要管理的数据库
@admin.register(Artical)
class ArticalAdmin(admin.ModelAdmin):
    # 文章列表里显示想要显示的字段
    list_display = ('id', 'category', 'title', 'tui', 'user', 'views', 'create_time', 'img')
    # 每页显示数量
    list_per_page = 50
    # 后台数据列表排列方式
    ordering = ('-create_time', )
    # 设置哪些字段可以点击编辑界面
    list_display_links = ('id', 'title')


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('id', 'text_info', 'img', 'link_url')
    # 设置哪些字段可以点击编辑界面
    list_display_links = ('text_info', )

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Tui)
class TuiAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'linkurl')


