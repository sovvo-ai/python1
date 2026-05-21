from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length = 100, unique = True, verbose_name = '分类名称')
    slug = models.SlugField(max_length = 100, unique = True, verbose_name = 'URL别名')
    created_at = models.DateTimeField(auto_now_add = True, verbose_name = '创建时间')

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = '分类'
        ordering=['id']
    def __str__(self):
        return self.name

class Post(models.Model):
    STATUS_CHOICES = [
        ('draft', '草稿'),
        ('published', '发布'),
    ]

    title = models.CharField(max_length = 200, verbose_name = '标题')
    slug = models.SlugField(max_length = 200, unique_for_date = 'created_at', verbose_name = 'URL别名')
    content = models.TextField(verbose_name = '内容')
    category = models.ForeignKey(
        Category,
        on_delete = models.CASCADE,
        related_name='posts',
        verbose_name = '分类'
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name = '状态'
    )
    cover = models.ImageField(
        upload_to='covers/%Y/%m/',
        blank=True,
        verbose_name='封面图'
    )
    created_at = models.DateTimeField(auto_now_add = True, verbose_name = '创建时间')
    updated_at = models.DateTimeField(auto_now = True, verbose_name = '更新时间')

    class Meta:
        ordering = ['-created_at']
        verbose_name = '文章'
        verbose_name_plural = '文章'
    def __str__(self):
        return self.title