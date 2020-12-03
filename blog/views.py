from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import FormView, TemplateView

from blog.forms import CreateBlogForm
from blog.models import Blog


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
            return super().form_valid(form)

        blog_info = json['response']['blog']

        new_blog = {
            field.name: blog_info[field.name]
            for field in Blog._meta.get_fields()
        }

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


class BlogDetail(TemplateView):
    template_name = 'blog/detail.html'

    @property
    def blog(self):
        return Blog.objects.get(name=self.kwargs['name'])

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            blog=self.blog,
            **kwargs
        )
