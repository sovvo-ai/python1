from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Category, Post
from .forms import PostForm


class CategoryModelTest(TestCase):
    """分类模型测试"""
    def test_create_category(self):
        cat = Category.objects.create(name='Python', slug='python')
        self.assertEqual(str(cat), 'Python')
        self.assertIsNotNone(cat.created_at)

    def test_slug_unique(self):
        """重复 slug 应该报错"""
        Category.objects.create(name='Python', slug='python')
        with self.assertRaises(Exception):
            Category.objects.create(name='Python2', slug='python')


class PostModelTest(TestCase):
    """文章模型测试"""
    def setUp(self):
        self.cat = Category.objects.create(name='Django', slug='django')

    def test_create_published_post(self):
        post = Post.objects.create(
            title='发布文章', slug='pub-post', content='正文',
            category=self.cat, status='published'
        )
        self.assertEqual(post.status, 'published')
        self.assertEqual(str(post), '发布文章')

    def test_default_status_is_draft(self):
        """不指定状态时默认应为草稿"""
        post = Post.objects.create(
            title='草稿', slug='draft-post', content='...',
            category=self.cat
        )
        self.assertEqual(post.status, 'draft')

    def test_ordering(self):
        """最新的文章应该排在前面"""
        old = Post.objects.create(
            title='旧的', slug='old', content='...', category=self.cat
        )
        new = Post.objects.create(
            title='新的', slug='new', content='...', category=self.cat
        )
        posts = list(Post.objects.all())
        self.assertEqual(posts[0], new)


class PostViewTest(TestCase):
    """视图测试"""
    def setUp(self):
        self.cat = Category.objects.create(name='Django', slug='django')
        self.post = Post.objects.create(
            title='测试文章', slug='test-post',
            content='测试内容正文', category=self.cat, status='published'
        )
        # 创建一个用户用于测试登录
        self.user = User.objects.create_user(username='testuser', password='test123')

    def test_post_list_view(self):
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '测试文章')

    def test_post_detail_view(self):
        response = self.client.get(f'/blog/post/{self.post.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '测试内容正文')

    def test_post_detail_404(self):
        response = self.client.get('/blog/post/99999/')
        self.assertEqual(response.status_code, 404)

    def test_create_post_requires_login(self):
        """未登录访问创建页应重定向到登录页"""
        response = self.client.get('/blog/post/create/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_create_post_after_login(self):
        """登录后可以访问创建页"""
        self.client.login(username='testuser', password='test123')
        response = self.client.get('/blog/post/create/')
        self.assertEqual(response.status_code, 200)


class PostFormTest(TestCase):
    """表单测试"""
    def setUp(self):
        self.cat = Category.objects.create(name='Python', slug='python')

    def test_valid_form(self):
        data = {
            'title': '测试标题', 'slug': 'test-slug',
            'content': '正文内容', 'category': self.cat.id,
            'status': 'published'
        }
        form = PostForm(data=data)
        self.assertTrue(form.is_valid(), msg=form.errors)

    def test_title_too_short(self):
        """标题太短应该验证失败"""
        data = {
            'title': 'Ab', 'slug': 'test',
            'content': '正文', 'category': self.cat.id,
        }
        form = PostForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)