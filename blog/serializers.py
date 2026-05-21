from rest_framework import serializers
from .models import Category, Post


class CategorySerializer(serializers.ModelSerializer):
    post_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'post_count']


class PostSerializer(serializers.ModelSerializer):
    # 显示分类名称（只读）
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'content', 'category',
                  'category_name', 'status', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def validate_title(self, value):
        if len(value) < 3:
            raise serializers.ValidationError('标题至少需要 3 个字符')
        return value

class PostDetailSerializer(serializers.ModelSerializer):
    """带完整分类信息的文章序列化器（用于详情）"""
    category = CategorySerializer(read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'content', 'category',
                  'category_name', 'status', 'created_at', 'updated_at']