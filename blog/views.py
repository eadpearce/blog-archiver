from django.urls import reverse_lazy
from django.views.generic import FormView

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
        blog_info = form.get_blog_info()
        new_blog = {
            field.name: blog_info[field.name]
            for field in Blog._meta.get_fields()
        }

        if Blog.objects.filter(uuid=new_blog['uuid']).exists():
            return super().form_valid(form)

        Blog.objects.create(**new_blog)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            blogs=self.blogs,
            **kwargs
        )
