from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Post, Category
from .serializers import PostSerializer, CategorySerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):   # 只读 ViewSet
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class PostViewSet(viewsets.ModelViewSet):                # 完整 CRUD ViewSet
    queryset = Post.objects.filter(status='published').select_related('category')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = ['status', 'category']  # ?status=published
    search_fields = ['title', 'content']  # ?search=Python
    ordering_fields = ['created_at', 'title']  # ?ordering=-created_at
    ordering = ['-created_at']
    authentication_classes = [SessionAuthentication,BasicAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    # 读公开，写需登录

    def get_queryset(self):
        """支持按分类筛选"""
        queryset = Post.objects.filter(status='published').select_related('category')
        category_id = self.request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset

    def perform_create(self, serializer):
        """创建文章时自动关联当前用户（如果模型有 author 字段）"""
        serializer.save()

    @action(detail=True, methods=['post'])
    def toggle_status(self, request, pk=None):
        """自定义动作：切换文章状态"""
        post = self.get_object()
        if post.status == 'published':
            post.status = 'draft'
        else:
            post.status = 'published'
        post.save()
        return Response({'id': post.id, 'status': post.status})