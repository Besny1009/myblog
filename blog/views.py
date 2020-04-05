from django.http import JsonResponse
from django.shortcuts import render
from .models import *
from django.forms.models import model_to_dict
from django.db.models import Count
import json
import math
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

#首页
pageNumber = 5
def index(request):

    #分类(导航部分)
    allCategory = Category.objects.all().values('id', 'name')
    category = [category for category in allCategory]

    #轮播图
    allBanner = Banner.objects.filter(is_active=True)[:4].values('text_info', 'img', 'link_url')
    banner = [banner for banner in allBanner]

    #推荐文章
    recommendArtical = Artical.objects.order_by('id').filter(tui__name='首页推荐')[:3].values('id', 'title', 'excerpt')
    recommend = [recommend for recommend in recommendArtical]


    #最新文章
    new = []
    newsArtical = Artical.objects.order_by('id', '-create_time')[:10].values('id', 'title', 'excerpt', 'create_time', 'category__id','category__name', 'img')

    for artical in newsArtical:
        artical['create_time'] = artical['create_time'].strftime('%Y-%m-%d')
        new.append(artical)

    #友情链接
    allLinks = Link.objects.all().values('name', 'linkurl')
    links = [link for link in allLinks]

    # 所有标签
    allTags = Tag.objects.all().values('name')
    tags = [tag for tag in allTags]

    #热门推荐
    hotRecommend = Artical.objects.order_by('id').filter(tui__name='热门推荐')[:6].values('id', 'img', 'title')
    hots = [hot for hot in hotRecommend]

    #热门文章
    hotArticals = Artical.objects.order_by('-views')[:10].values('id', 'title')
    hotArtical = [hot for hot in hotArticals]
    context = {
        'category': category,
        'banner': banner,
        'recommendArtical': recommend,
        'newsArtical': new,
        'links': links,
        'tags': tags,
        'hotRecommend': hots,
        'hotArticals': hotArtical
    }
    return render(request, 'index .html', context)

#列表页
def list(request,lid):
    # 获取当前页
    page = request.GET.get('page')
    #获取所有分类
    category = Category.objects.all()
    # 获取分类名称
    cname = Category.objects.get(id=lid)
    # 热门推荐
    recommend = Artical.objects.filter(tui__id=2)[:6]
    # 所有标签
    tag = Tag.objects.all()
    # 根据分类id获取列表内容
    list = Artical.objects.filter(category_id=lid)
    # 查询数据超过指定的条数分页
    paginator = Paginator(list, pageNumber)
    try:
        list = paginator.page(page)
    except PageNotAnInteger:
        list = paginator.page(1)
    except EmptyPage:
        list = paginator.page(paginator.num_pages)
    return render(request, 'list.html', locals())
# 详情页
def show(request, aid):
    # 导航分类
    category = Category.objects.all()
    # 获取文章内容
    artical = Artical.objects.get(id=aid)
    # 热门推荐
    recommend = Artical.objects.filter(tui_id=2)[:6]
    # 标签
    tag = Tag.objects.all()
    # 可能感兴趣
    interest = Artical.objects.all().order_by('?')[:10]

    # 上一篇
    pre_blog = Artical.objects.filter(create_time__gt=artical.create_time, category_id=artical.category.id).first()
    # 下一篇
    next_blog = Artical.objects.filter(create_time__lt=artical.create_time, category=artical.category_id).last()

    artical.views = artical.views + 1
    artical.save()
    return render(request, 'show.html', locals())
# 标签搜索
def tags(request,tname):
    # 导航标签
    category = Category.objects.all()
    # 热门推荐
    recommend = Artical.objects.filter(tui_id=2)[:6]
    # 所有标签
    tag = Tag.objects.all()
    # 获取标签内容
    list = Artical.objects.filter(tag__name=tname)
    #获取当前页
    page = request.GET.get('page')
    paginator = Paginator(list, pageNumber)
    try:
        list = paginator.page(page)
    except PageNotAnInteger:
        list = paginator.page(1)
    except EmptyPage:
        list = paginator.page(paginator.num_pages)
    return render(request, 'tags.html', locals())
# 搜索文章
def search(request):
    keywords = request.GET.get('search')
    list = Artical.objects.order_by('-id').filter(title__contains=keywords)
    recommend = Artical.objects.order_by('-id').filter(tui_id=2)[:6]
    tag = Tag.objects.all()
    category = Category.objects.all()
    page = request.GET.get('page')
    paginator = Paginator(list, pageNumber)
    try:
        list = paginator.page(page)
    except PageNotAnInteger:
        list = paginator.page(1)
    except EmptyPage:
        list = paginator.page(paginator.num_pages)

    return render(request, 'search.html', locals())


# 获取分类文章列表的内容
def getArticalList(request):

    category_id = request.GET.get('category_id')
    page = request.GET.get('page')

    if page is None:
        page = 1

    limit = (page - 1) * pageNumber
    total_pages = 0
    articals = []

    query = Artical.objects.filter(category=category_id).order_by("-create_time")
    # count
    total = query.count()
    # total pages
    total_pages = math.ceil(total / pageNumber)

    AllArticals = query[limit:(limit + pageNumber)].values('id', 'title', 'excerpt', 'create_time', 'img',
                                                           'category__name')
    for artical in AllArticals:
        artical['create_time'] = artical['create_time'].strftime('%Y-%m-%d')
        articals.append(artical)
    code = 200
    msg = '返回内容'
    context = {
        'artical': articals,
        'total_pages': total_pages
    }

    return render(request, 'list.html', locals())

# 获取文章的详情
def articalDetail(request):
    artical_id = request.GET.get('artical_id')
    detail = {}
    try:
        artical = Artical.objects.get(id=artical_id)
        artical.create_time = artical.create_time.strftime('%Y-%m-%d')
        category_name = artical.category.name
        username = artical.user.username
        artical = model_to_dict(artical)
        artical['category_name'] = category_name
        artical['username'] = username
        artical.pop('img')
        artical.pop('user')
        artical.pop('category')
        artical.pop('tui')
        artical.pop('excerpt')

        artical['tag'] = [str(tag) for tag in artical['tag']]

        print(artical)
        detail.update(artical)
        code = 200
        msg = "获取信息成功"
    except Artical.DoesNotExist:
        code = 500
        msg = "根据传送的ID获取不到文章"
    except Artical.MultipleObjectsReturned:
        code = 500
        msg = "获取文章的个数有多个"
    context = {
        'code': code,
        'msg': msg,
        'data': {
            'detail': detail
        }
    }

    return JsonResponse(context)

# 根据标签搜索
def getTagSearch(request):
    tagName = request.GET.get('tagName')
    page = request.GET.get('page')

    if page is None:
        page = 1
    else:
        page = int(page)
    limit = (page - 1) * pageNumber
    searchArtical = []
    total_page = 0
    query = Artical.objects.order_by('-create_time').filter(tag__name__icontains=tagName)
    total = query.count()
    getSearchInfo = query[limit:limit + pageNumber].values('id', 'title', 'excerpt', 'img', 'create_time',
                                                           'category__name')

    total_page = math.ceil(total / pageNumber)
    for search in getSearchInfo:
        search['create_time'] = search['create_time'].strftime('%Y-%m-%d')
        searchArtical.append(search)

    code = 200
    msg = '返回查询数据'

    context = {
        code: code,
        msg: msg,
        'data': {
            'searchInfo': searchArtical,
            'total_page': total_page
        }
    }
    return JsonResponse(context, safe=False)

# 搜索结果
def getSearch(request):
    search = request.GET.get('keywords')
    page = request.GET.get('page')

    if page is None:
        page = 1
    page = int(page)

    searchArticals = []
    pageNumber = 6

    offset = (page - 1) * pageNumber

    total_page = 0

    query = Artical.objects.filter(title__contains=search)
    # 符合条件的总数
    total = query.count()
    # 总页数
    total_page = math.ceil(total / pageNumber)

    getResult = query[offset: offset + pageNumber].values('id', 'title', 'excerpt', 'img', 'category__name',
                                                          'create_time')

    for artical in getResult:
        artical['create_time'] = artical['create_time'].strftime('%Y-%m-%d')
        searchArticals.append(artical)

    code = 200
    msg = '返回数据'

    context = {
        'code': code,
        'msg': msg,
        'data': {
            'searchArticals': searchArticals,
            'total_page': total_page
        }
    }

    return JsonResponse(context, safe=False)







