from django import forms
from blog import api_client


class CreateBlogForm(forms.Form):
    blog_name = forms.CharField(label='Blog name')

    def get_blog_info(self):
        blog_name = self.cleaned_data['blog_name']
        return api_client.get_blog_info(blog_name=blog_name)


class GetPostsForm(forms.Form):
    limit = forms.IntegerField()
    offset = forms.IntegerField()

    def get_posts(self, blog_name):
        return api_client.get_posts(blog_name=blog_name)
