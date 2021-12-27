from django import forms
from django.http import request
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate,get_user_model,login,logout
from django.contrib import messages
from .forms import UserLogin,UserSignup,ProfileImage,UserUpdate, UserPosts, Booked
from .models import Products, BlockUsers
from .models import ProfileImage as UserProfile 
from django.db.models import Q
from django.views.generic import TemplateView,DetailView, ListView
from django.views import View
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test


User=get_user_model()

class HomePageView(ListView):
    template_name='app/home_page.html'
    model=Products
    context_object_name='products'

    try:
        def get_context_data(self, **kwargs):
                request=self.request
                if request.user.is_authenticated:
                    context =super().get_context_data(**kwargs)
                    get_username=self.request.user.username
                    user=User.objects.get(username=get_username)
                    user_products=Products.objects.filter(~Q(user=user)).order_by('-post_date')
                    context['products']=user_products   
                    return context
    except:
        pass            
        

def sort_item(request,category):
    get_items=Products.objects.filter(category=category)
    context={
        'products':get_items
    }
    return render(request,'app/home_page.html',context)



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
        product_owner_id=product.user.id
        owner=get_object_or_404(User,pk=product_owner_id)
        product.is_booked=True
        product.save()
        path=self.request.path
        if path=='/users/user':
            return redirect(f'{path}/{owner.id}')         
        elif path=='/user/item':
            return redirect(f'{path}/{product_id}')

        # print()


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
    user=request.user
    if request.method == 'POST':
        form=UserLogin(request.POST)
        if form.is_valid():
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            user=authenticate(username=email,password=password)  
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
            'posts':posts,
            'user':find_user
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
            'posts':posts,
            # 'user_1':find_user
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

class AcceptAllPosts(View):

    def post(self,request):
        pending_posts=Products.objects.filter(is_pending=True)
        for pending_post in pending_posts:
            pending_post.is_accepted=True
            pending_post.is_pending=False
            pending_post.save()


        return redirect('admin-list')

class Users(ListView):
    model=User
    template_name='app/users.html'
    context_object_name='users'

    def get_context_data(self, **kwargs):
        is_admin=self.request.user.is_superuser
        context=super().get_context_data(**kwargs)
        users=User.objects.filter(is_admin=False)
        context['users']=users
        context['is_admin']=is_admin
        return context

class BlockUserView(View):
    def post(self,request):
        user_id=request.POST['user_id']
        user=get_object_or_404(User,pk=user_id)
        user.is_blocked=True
        block_user=BlockUsers()
        block_user.username=user.username
        block_user.email=user.email
        block_user.phone_number=user.phone_number
        profile_image=get_object_or_404(UserProfile,user=user)
        block_user.profile_image=profile_image
        user.save()
        block_user.save()
        return redirect('users')


class UserDetail(DetailView):
    model=User
    template_name='app/user_profile.html'
    context_object_name='user'
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        loaded_user=self.object
        get_loaded_user=get_object_or_404(User,pk=loaded_user.id)
        user_products=Products.objects.filter(user=get_loaded_user)
        request=self.request
        user=request.user
        visitor=loaded_user.id != user.id
        context['is_visitor']=visitor
        context['posts']=user_products
        return context
   
      



class RejectedPosts(View):
    def get(self,request):
        pass
    
    def post(self,request):
        product_id=request.POST['product_id']
        user_prodcut=get_object_or_404(Products,pk=product_id)
        user=get_object_or_404(User,pk=user_prodcut.user.id)
        user_prodcut.is_rejected=True
        user_prodcut.is_pending=False
        user.rejected_post+=1
        if user.rejected_post==3:
            profile_image=get_object_or_404(UserProfile,user=user)
            delete_products=Products.objects.filter(user=user).delete()
            block_users=BlockUsers.objects.create(id=user.id,username=user.username,
                                        email=user.email,phone_number=user.phone_number,
                                        profile_image=profile_image)
            user.is_blocked=True
            block_users.save()
            user.save()
            messages.error(request,f'{user.username} have been blocked!')
            return redirect('admin-list')


        user.save()    
        user_prodcut.save()
        return redirect('admin-list')
        
class UnblockUser(View):

    def post(self,request):
        get_user_name=request.POST['user_id']
        get_user=get_object_or_404(User,username=get_user_name)
        unblock_user=get_object_or_404(BlockUsers,username=get_user).delete()
        get_user.is_blocked=False
        get_user.rejected_post=0
        get_user.save()
        # unblock_user.save()
        messages.success(request,f'{get_user.username} has been remove from the block list ')
        return redirect('block-users')



class UserLikes(View):

    def post(self,request):
        get_user_id=request.POST['user_id']
        user=get_object_or_404(User,pk=get_user_id)

        # user.total_liked


class BlockListView(ListView):
    model=BlockUsers
    template_name='app/block_list.html'
    context_object_name='users'

   


class AdminListView(ListView):
    model=Products
    template_name='app/admin_list.html'
    context_object_name='users'

    
    





# Create your views here.
