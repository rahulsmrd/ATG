from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import *
from django.urls import reverse_lazy
from django.views.generic import *
from django.contrib.auth.decorators import login_required
from home.models import *
from blog.models import *
from home.forms import *
from django.contrib.auth import authenticate,login,get_user_model


user_model=get_user_model()

# Create your views here.

def index(request):
    return render(request, 'index.html')



def SignUp(request):
    if request.method == 'POST':
        is_doc=request.POST.get('check')
        if is_doc:
            doc_id=request.POST.get('doc_id')
        user_form=UserCreateForm(request.POST)
        profile=profile_form(request.POST,request.FILES)
        if user_form.is_valid() and profile.is_valid():
            user=user_form.save()
            pro=profile.save(commit=False)
            pro.user=user
            pro.is_doctor=bool(is_doc)
            if is_doc:
                pro.doc_id=doc_id
            pro.save()
            return redirect(reverse_lazy("home:home"))
    return render(request, 'signup.html',{'Userform':UserCreateForm,'profile_form':profile_form,})

@login_required
def dashboard(request):
    user=request.user
    profile_data=profile.objects.filter(user=user.id).all()
    return render(request, 'dashboard.html',{'user':user, 'profile':profile_data[0]})

def login_user(request,pk):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        if pk=='1':
            doc_id=request.POST.get('doc_id')
        user=authenticate(username=username, password=password)
        if user is not None:
            user_info=profile.objects.filter(user=user.id).all()
            if pk=='1':
                if user_info[0].doc_id==int(doc_id):
                    login(request,user)
                    return redirect(reverse_lazy('home:dashboard'))
            elif pk=='0':
                login(request,user)
                return redirect(reverse_lazy('home:dashboard'))
            else:
                return render(request,'login.html',{'error': "Invalid Doctor ID"})
        else:
            return render(request,'login.html',{"error": "Invalid Credentials"})
    return render(request, 'login.html',{"pk_user":pk})

def contact(request):
    if request.method == 'POST':
        cont=contact_form(request.POST)
        cont.save()
        return redirect(reverse_lazy('home:home'))
    return render(request,'contact.html',{'form':contact_form})

@login_required
def user_profile(request):
    user=request.user
    all_posts=post.objects.filter(user=user)
    pro=profile.objects.filter(user=user)[0]
    return render(request, 'profile.html', {
        'published': all_posts.filter(published=True).all(),
        'not_published': all_posts.filter(published=False).all(),
        'profile':pro
                                            })

class PasswordChangeView(PasswordChangeView,LoginRequiredMixin):
    form_class = PasswordChangeForm
    template_name='pasword_change.html'
    success_url=reverse_lazy("home:profile")

class update_profile_data(UpdateView):
    model=profile
    form_class=profile_form
    template_name="update_profile.html"
    success_url=reverse_lazy("home:profile")

    def form_valid(self, form):
        form2=form.save(commit=False)
        if not form2.is_doctor:
            form2.doc_id=None
        form2.save()
        return super().form_valid(form)