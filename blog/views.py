from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from blog.models import Blog


class BlogCreateView(CreateView):
    model = Blog
    fields = ("name", "content", "preview")
    success_url = reverse_lazy('blog:blog_list')

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.save()

        return super().form_valid(form)


class BlogListView(ListView):
    model = Blog

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        # queryset = queryset.filter(is_published=True)
        return queryset


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_counter += 1
        self.object.save()
        return self.object


class BlogUpdateView(UpdateView):
    model = Blog
    fields = ("name", "content", "preview")

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            # new_blog.slug = slugify(new_blog.name)
            new_blog.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:blog_detail', args=[self.kwargs.get('pk')])


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:blog_list')


# def toggle_publish(request, pk):
#     blog_item = get_object_or_404(Blog, pk=pk)
#     if blog_item.is_published:
#         blog_item.is_published = False
#     else:
#         blog_item.is_published = True
#
#     blog_item.save()
#     return redirect(reverse('blog:blog_list'))
