from typing import Any
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpRequest
from django.shortcuts import render,HttpResponse,get_object_or_404,redirect
from django.urls import reverse,reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User as mainUser
from django.views.generic import *
from blog.models import *
from blog.forms import *
# Create your views here.

user_model=get_user_model()


class index(ListView):
    model=post
    template_name="blog/index.html"
    def get_queryset(self) -> QuerySet[Any]:
        return post.objects.filter(published=True).order_by('published_date').all()

class detail_post(DeleteView):
    model=post
    template_name="blog/detail.html"

class create_post(CreateView):
    model = post
    template_name="blog/create.html"
    form_class = create_form
    success_url= reverse_lazy('home:profile')

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form2=form.save(commit=False)
        form2.user=get_object_or_404(mainUser,pk=self.request.user.id)
        cat=self.request.POST.get('cat')
        form2.category=cat
        form2.save()
        return super().form_valid(form)

class update_post(UpdateView):
    model = post
    form_class = create_form
    template_name="blog/update.html"
    success_url=reverse_lazy('home:profile')
    
    def get_queryset(self) -> QuerySet[Any]:
        QuerySet=post.objects.filter(pk=self.kwargs['pk']).all()
        return QuerySet
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form2=form.save(commit=False)
        cat=self.request.POST.get('cat')
        form2.category=cat
        form2.save()
        return super().form_valid(form)

class delete_post(DeleteView):
    model = post
    template_name="blog/delete.html"
    success_url=reverse_lazy("blog:home")

def publish(request,pk):
    req_post=post.objects.get(pk=pk)
    if req_post.user==request.user:
        if req_post.published:
            req_post.unpublish()
            return redirect(reverse_lazy('home:profile'))
        req_post.publish()
        return redirect(reverse_lazy('home:profile'))
    else:
        return redirect(reverse_lazy('home:home'))
        