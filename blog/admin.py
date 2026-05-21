from django.contrib import admin
from .models import Category,Post
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'post_count', 'created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}

    @admin.display(description='文章数')
    def post_count(self, obj):
        return obj.posts.count()


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # 列表页配置
    list_display = ['title', 'category', 'status', 'word_count', 'created_at']
    list_filter = ['status', 'category', 'created_at']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    list_editable = ['status']
    list_per_page = 20

    # 编辑页分组
    fieldsets = (
        ('基本信息', {
            'fields': ('title', 'slug', 'content')
        }),
        ('分类与状态', {
            'fields': ('category', 'status'),
            'classes': ('collapse',)  # 默认折叠，点开才能看到
        }),
    )

    # 自定义批量动作
    actions = ['make_published', 'make_draft']

    @admin.display(description='字数')
    def word_count(self, obj):
        return len(obj.content)

    @admin.action(description='✅ 批量设为已发布')
    def make_published(self, request, queryset):
        updated = queryset.update(status='published')
        self.message_user(request, f'成功发布 {updated} 篇文章')

    @admin.action(description='📝 批量设为草稿')
    def make_draft(self, request, queryset):
        updated = queryset.update(status='draft')
        self.message_user(request, f'{updated} 篇文章已改为草稿')
