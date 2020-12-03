from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.views.generic import FormView

from blog.forms import CreateBlogForm, GetPostsForm
from blog.models import Blog
from post.models import Post


def get_necessary_fields(data, model_class, exclude=None):
    return {
        field.name: data[field.name]
        for field in model_class._meta.get_fields()
        if field.name != exclude and data.get(field.name)
    }


class Index(FormView):
    template_name = "blog/index.html"
    form_class = CreateBlogForm
    success_url = reverse_lazy('index')

    @property
    def blogs(self):
        return Blog.objects.all()

    def form_valid(self, form):
        json, status_code = form.get_blog_info()

        if status_code != 200:
            messages.error(self.request, f'Got {status_code} from Tumblr API')

        blog_info = json['response']['blog']

        new_blog = get_necessary_fields(blog_info, Blog, exclude='posts')

        if Blog.objects.filter(uuid=new_blog['uuid']).exists():
            return super().form_valid(form)

        Blog.objects.create(**new_blog)

        messages.success(self.request, f"Blog {blog_info['name']} added!")

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            blogs=self.blogs,
            **kwargs
        )


class BlogDetail(FormView):
    template_name = 'blog/detail.html'
    form_class = GetPostsForm

    @property
    def blog(self):
        return get_object_or_404(Blog, name=self.kwargs['name'])

    def get_success_url(self):
        return reverse_lazy('blog-detail', kwargs=self.kwargs)

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            blog=self.blog,
            **kwargs
        )

    def form_valid(self, form):
        json, status_code = form.get_posts(self.kwargs['name'], **form.cleaned_data)

        if status_code != 200:
            messages.error(self.request, f'Got {status_code} from Tumblr API')

        posts = json['response']['posts']

        for post in posts:
            new_post = get_necessary_fields(post, Post, exclude='blog')

            if Post.objects.filter(id=new_post['id']).exists():
                continue

            Post.objects.create(
                blog=self.blog,
                **new_post
            )

        return super().form_valid(form)
