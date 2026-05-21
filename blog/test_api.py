from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Category, Post


class PostAPITest(APITestCase):
    def setUp(self):
        self.cat = Category.objects.create(name='Python', slug='python')
        self.post = Post.objects.create(
            title='API文章', slug='api-post', content='API测试内容',
            category=self.cat, status='published'
        )
        self.user = User.objects.create_user(username='apiuser', password='api123')

    def test_get_post_list(self):
        response = self.client.get('/blog/api/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_get_post_detail(self):
        response = self.client.get(f'/blog/api/posts/{self.post.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'API文章')

    def test_create_without_auth_fails(self):
        """未认证创建应返回 401"""
        data = {'title': '新文章', 'slug': 'new', 'content': '...',
                'category': self.cat.id, 'status': 'draft'}
        response = self.client.post('/blog/api/posts/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_with_auth_succeeds(self):
        """登录后创建应返回 201"""
        self.client.login(username='apiuser', password='api123')
        data = {'title': '认证创建', 'slug': 'auth-create',
                'content': '...', 'category': self.cat.id, 'status': 'draft'}
        response = self.client.post('/blog/api/posts/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_search(self):
        response = self.client.get('/blog/api/posts/?search=API')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_filter_by_category(self):
        cat2 = Category.objects.create(name='JavaScript', slug='js')
        Post.objects.create(
            title='JS文章', slug='js-post', content='...',
            category=cat2, status='published'
        )
        response = self.client.get(f'/blog/api/posts/?category={cat2.id}')
        self.assertEqual(len(response.data['results']), 1)
