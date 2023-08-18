from django.shortcuts import get_object_or_404, render, HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse

from .models import Blog, Comments


def index(request):
    latest_blog_posts = Blog.objects.order_by('-posted')[:3]
    context = {'latest_blog_posts': latest_blog_posts}
    return render(request, 'blog/index.html', context)

def archive(request):
    all_blog_posts = Blog.objects.order_by('-posted')
    context = {'all_blog_posts': all_blog_posts}
    return render(request, 'blog/archive.html', context)
   
def detail(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    if request.POST:

        try:
            form = request.POST
        except (KeyError, Comments.DoesNotExist):
            return render(request, '', {'blog': blog})
        else:
            blog.comments_set.create(commenter=form['username'], email=form['email'], content=form['comment'], posted=timezone.now())
            return HttpResponseRedirect(reverse('blog:detail', args=(blog.id,)))
 
    return render(request, 'blog/detail.html', {'blog': blog})

def about(request):
    return render(request, 'blog/about.html')

def techtipsWithoutCss(request):
    return render(request, 'blog/techtips-css.html')

def techtipsWithCss(request):
    return render(request, 'blog/techtips+css.html')

def plan(request):
    return render(request, 'blog/plan.html')


