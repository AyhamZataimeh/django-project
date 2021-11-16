from django import forms
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate,get_user_model,login,logout
from django.contrib import messages
from .forms import UserLogin,UserSignup,ProfileImage,UserUpdate, UserPosts, Booked
from .models import Products
from django.db.models import Q
from django.views.generic import TemplateView,DetailView, ListView
from django.views import View
from django.contrib.auth.decorators import login_required


User=get_user_model()

class HomePageView(TemplateView):
    template_name='app/home_page.html'
    def get_context_data(self, **kwargs):
        context =super().get_context_data(**kwargs)
        get_user=self.request.user.username
        # print('username is ',get_user)
        find_user=User.objects.get(username=get_user)
        user=Products.objects.filter(~Q(user=find_user))
        context['users']=user   
        return context

def booked_item_view(request,id):
    product=Products.objects.get(pk=id)
    context={
            'product':product
        }
    return render(request,'app/item-details.html',context)    


class BookItemView(View):

    def post(self,request):
        product_id=request.POST['product_id']
        product=get_object_or_404(Products,pk=product_id)
        product.is_booked=True
        product.save()
        return redirect('/user/item/'+product_id)


class UnBookedItemView(View):

    def post(self,request):
        product_id=request.POST['product_id']
        product=get_object_or_404(Products,pk=product_id)
        print(product.product)
        product.is_booked=False
        product.save()
        return redirect('profile')  
        

  


def home_page_view(request):
    get_username=request.user.username
    fetch_user=User.objects.get(username=get_username)
    users=Products.objects.filter(~Q(user=fetch_user))

  
    if request.method== 'POST':
        request.session['booked']=True

        return redirect('home')
    context={
        'users':users,
    }

    return render(request,'app/home_page.html',context)

def login_view(request):
    next=request.GET.get('next')
    if request.method == 'POST':
        form=UserLogin(request.POST)
        if form.is_valid():
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            user=authenticate(username=email,password=password)
            if not user.check_password(password):
                print('wrong')
                raise forms.ValidationError(' Wrong password')
            login(request,user)
            if next:
                return redirect(next)
            return redirect('home')
        context={
            'form':form
        }
        return render(request,'app/login_page.html',context)        
    else:
        form=UserLogin()
        context={
            'form':form
        }
        return render(request,'app/login_page.html',context)        

def logout_view(request):
    logout(request)
    return render(request,'app/logout_page.html')


def signin_view(request):
    next=request.GET.get('next')
    if request.method == 'POST':
        form=UserSignup(request.POST)
        img_form=ProfileImage(request.POST,request.FILES)

        if form.is_valid() and img_form.is_valid():
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            username=form.cleaned_data['username']
            user=form.save(commit=False)
            user.set_password(password)
            user.save()
            user_img=img_form.save(commit=False)
            get_user=get_object_or_404(User,username=username)
            user_img.user=get_user
            user_img.save()
            user_auth=authenticate(username=email,password=password)
            login(request,user_auth)
            if next:
                return redirect(next)
            messages.success(request,f'{username} you have successfully signed up')
            return redirect('login')
        context={
            'form':form,
            'image_form':img_form
        }        
        return render(request,'app/user_signup.html',context)
    else:
        form=UserSignup()
        img_form=ProfileImage()
        context={
            'form':form,
            'image_form':img_form
        }        
        return render(request,'app/user_signup.html',context)

@login_required
def profile(request):
    find_user=get_object_or_404(User,username=request.user.username)
  
    if request.method == 'POST':
        posts=Products.objects.filter(user=find_user)
        update_user=UserUpdate(request.POST,instance=request.user)
        update_image=ProfileImage(request.POST,request.FILES,instance=request.user.profileimage)
        user_post=UserPosts(request.POST,request.FILES)


        
        if update_user.is_valid() and update_image.is_valid():
            update_user.save()
           

            update_image.save()
            messages.success(request,' Profile has been updated ')
            return redirect('profile')

        if user_post.is_valid():
            post=user_post.save(commit=False)
            post.user=find_user
            post.save()
            messages.success(request,' You have posted ')
            return redirect('profile')

        context={
            'update_user':update_user,
            'update_image':update_image,
            'post':user_post,
            'posts':posts
        }

        return render(request,'app/user_profile.html',context)
    else:
        posts=Products.objects.filter(user=find_user)
        update_user=UserUpdate(instance=request.user)
        update_image=ProfileImage(instance=request.user.profileimage)
        user_post=UserPosts()
        context={
            'update_user':update_user,
            'update_image':update_image,
            'post':user_post,
            'posts':posts
        }
        return render(request,'app/user_profile.html',context)



class AcceptedPosts(View):
    def get(self,request):
        pass

    def post(self,request):
        product_id=request.POST['product_id']
        user_product=get_object_or_404(Products,pk=product_id)
        user_product.is_accepted=True
        user_product.is_pending=False        
        user_product.save()
        return redirect('admin-list')


class RejectedPosts(View):
    counter=0
    def get(self,request):
        pass
    
    def post(self,request):
        self.counter=self.counter+1
        product_id=request.POST['product_id']
        user_prodcut=get_object_or_404(Products,pk=product_id)
        user_prodcut.is_rejected=True
        user_prodcut.is_pending=False
        user_prodcut.user.rejected_post=self.counter
        if user_prodcut.user.rejected_post==3:
            user_prodcut.user.is_blocked=True
        user_prodcut.save()
        return redirect('admin-list')
        

class AdminListView(ListView):
    model=Products
    template_name='app/admin_list.html'
    context_object_name='users'
    
    





# Create your views here.
