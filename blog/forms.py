from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'content', 'category', 'status','cover']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 10,
                'placeholder': '开始写你的文章...'
            }),
            'status': forms.Select,
        }
        labels = {
            'title': '文章标题',
            'slug': 'URL 别名',
            'content': '文章内容',
            'category': '所属分类',
            'status': '发布状态',
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 3:
            raise forms.ValidationError('标题至少需要 3 个字符！')
        return title