from django import forms
from blog import api_client


class CreateBlogForm(forms.Form):
    blog_name = forms.CharField(label='Blog name')

    def get_blog_info(self):
        blog_name = self.cleaned_data['blog_name']
        return api_client.get_blog_info(blog_name=blog_name)
