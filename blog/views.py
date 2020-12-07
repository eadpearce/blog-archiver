from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.views.generic import FormView

from blog.forms import CreateBlogForm, GetPostsForm
from blog.models import Blog
from post.models import Post, Block, Reblog


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

        if Blog.objects.filter(uuid=blog_info['uuid']).exists():
            return super().form_valid(form)

        Blog.objects.create(
            avatar=blog_info['avatar'],
            description=blog_info['description'],
            name=blog_info['name'],
            title=blog_info['title'],
            total_posts=blog_info['total_posts'],
            url=blog_info['url'],
        )

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
            # new_post = get_necessary_fields(post, Post, exclude='blog')

            if Post.objects.filter(id=post['id']).exists():
                continue

            new_post = Post.objects.create(
                blog=self.blog,
                id=post['id'],
                type=post['type'],
                post_url=post['post_url'],
                tags=post.get('tags', ''),
                summary=post['summary'],
                source_url=post.get('source_url', ''),
                content=post.get('content', ''),
                layout=post.get('layout', ''),
            )

            for reblog in post['trail']:
                new_reblog = Reblog.objects.create(post=new_post)

                for block in reblog['content']:

                    url = ''

                    if block.get('media'):
                        url = block.get('media')[0]['url']

                    new_block = Block.objects.create(
                        reblog=new_reblog,
                        text=block.get('text'),
                        url=url,
                    )
                    new_block.save()

        return super().form_valid(form)
