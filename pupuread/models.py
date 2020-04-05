from django.db import models

# Create your models here.
# 导航表
class Nav(models.Model):
    name = models.CharField('导航名称', max_length=16)
    sort = models.IntegerField('排序', default=0)
    class Meta:
        verbose_name = '导航'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

# 分类归属
class Attribution(models.Model):
    name = models.CharField("归属名称", max_length=16)
    class Meta:
        verbose_name = "分类归属"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

# 小说分类表
class Category(models.Model):
    name = models.CharField("分类名称", max_length=32)
    pid = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, verbose_name='父级ID')
    attribution = models.ForeignKey(Attribution, on_delete=models.CASCADE, blank=True, null=True, verbose_name='分类归属')
    sort = models.IntegerField('排序', default=0)

    class Meta:
        verbose_name = "小说分类"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name



# 推荐
class Recommend(models.Model):
    name = models.CharField("推进名称", max_length=32)
    class Meta:
        verbose_name = '推荐'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

# 小说标签表
class Label(models.Model):
    name = models.CharField("标签名称", max_length=32)
    attribution = models.ForeignKey(Attribution, verbose_name='归属', on_delete=models.CASCADE, blank=True, null=True)
    recommend = models.ForeignKey(Recommend, verbose_name='推荐', on_delete=models.CASCADE, blank=True, null=True)
    sort = models.IntegerField('排序', default=0)

    class Meta:
        verbose_name = '小说标签'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

# 小说作者
class Author(models.Model):
    name = models.CharField("作者名称", max_length=16)
    introduction = models.TextField("作者简介", default="这是一位来自星星的作者", blank=True, null=True)
    img = models.ImageField(upload_to='pupuread/author_img/%Y%m%d', verbose_name='作者头像', blank=True, null=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    modified_time = models.DateTimeField('修改时间', auto_now=True)
    class Meta:
        verbose_name = '小说作者'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name