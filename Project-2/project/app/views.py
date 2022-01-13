from django.http import request
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate,get_user_model,login,logout
from django.contrib import messages
from django.views.generic.base import TemplateView
from .forms import UserLogin,UserSignup,ProfileImage,UserUpdate, UserPosts
from .models import Products, BlockUsers, RequestedBook
from .models import ProfileImage as UserProfile 
from django.db.models import Q
from django.views.generic import DetailView, ListView
from django.views import View
from django.contrib.auth.decorators import login_required


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
    user=request.user
    product=Products.objects.get(pk=id)
    get_user=get_object_or_404(User,pk=user.id)
    check_users=RequestedBook.objects.filter(product_owner__id=product.id)
    print(check_users)
    has_requsted=False
    is_accepted=False
    is_rejected=False
    for check_user in check_users:
        if user.id == check_user.requestd_user.id:
            has_requsted=True
        
        if check_user.is_accepted and user.id == check_user.requestd_user.id :
            is_accepted=True
            has_requsted=False    
        
        if check_user.is_rejected and user.id == check_user.requestd_user.id :
            is_rejected=True   
            has_requsted=False     
        pass
    
        
    # print(check_product)
    context={
            'product':product,
            'has_requsted':has_requsted,
            'is_accepted':is_accepted,
            'is_rejected':is_rejected
            
          
        }
    return render(request,'app/item-details.html',context)    


class UsersDetails(ListView):
    model=User
    template_name='app/users_details.html'
    context_object_name='users'
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)       
        users=User.objects.filter(is_admin=False)
        context['users']=users
        return context

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
        path=self.request.path
        if path=='/unbook/item':
            return redirect('booked_item')
        elif path=='/user/unbook/item':    
            return redirect('profile')  
        

  




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
    return redirect('login')


def signup_view(request):
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

def profile_edit(request,id):
    user=get_object_or_404(User,pk=id)
    user_update=UserUpdate(instance=request.user)
    profileimage_update=ProfileImage(request.FILES,instance=request.user.profileimage)

    if request.method=='POST':
        user_update=UserUpdate(request.POST,instance=request.user)
        profileimage_update=ProfileImage(request.POST,request.FILES,instance=request.user.profileimage)
      

        if user_update.is_valid() and profileimage_update.is_valid():
            user_update.save()
            profileimage_update.save()
            messages.success(request,'you have successfully update your profile')
            path=request.path
            return redirect(path)
  

        context={
            'user_update':user_update,
            'profileimage_update':profileimage_update,
            'user':user
        }
 

        return render(request,'app/edit_profile.html',context)
    
    context={
        'user_update':user_update,
        'profileimage_update':profileimage_update,
        'user':user
    }
    return render(request,'app/edit_profile.html',context)
 
    
    


@login_required
def profile(request):
    find_user=get_object_or_404(User,username=request.user.username)
  
    if request.method == 'POST':
        posts=Products.objects.filter(user=find_user)
        user_post=UserPosts(request.POST,request.FILES)


     
        if user_post.is_valid():
            post=user_post.save(commit=False)
            post.user=find_user
            find_user.total_posts+=1
            find_user.save()
            post.save()
            messages.success(request,' You have posted ')
            return redirect('profile')

        context={
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
  
    def post(self,request):
        product_id=request.POST['product_id']
        user_product=get_object_or_404(Products,pk=product_id)
        user=get_object_or_404(User,pk=user_product.user.id)
        user.accepted_posts+=1
        user_product.is_accepted=True
        user_product.is_pending=False        
        user_product.save()
        user.save()
        return redirect('admin-list')

class AcceptAllPosts(View):

    def post(self,request):
        posts=Products.objects.filter(is_pending=True)
        for post in posts:
            user=get_object_or_404(User,pk=post.user.id)
            post.is_accepted=True
            post.is_pending=False
            user.accepted_posts+=1
            user.save()
            post.save()



        return redirect('admin-list')

class RejectAllPost(View):
    
    def post(self,request):
        posts=Products.objects.filter(is_pending=True)
        for post in posts:
            user=get_object_or_404(User,pk=post.user.id)
            post.is_pending=False
            post.is_rejected=True
            user.rejected_post+=1
            user.save()
            post.save()

     

        return redirect('admin-list')   


class Users(ListView):
    model=User
    template_name='app/users.html'
    context_object_name='users'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        is_admin=self.request.user.is_superuser
        users=User.objects.filter(is_admin=False)
        context['users']=users
        context['is_admin']=is_admin
        return context

class BlockUserView(View):

    def post(self,request):
        user_id=request.POST['user_id']
        user=get_object_or_404(User,pk=user_id)
        user.is_blocked=True
        delete_products=Products.objects.filter(user=user).delete()
        block_user=BlockUsers()
        block_user.username=user.username
        block_user.email=user.email
        block_user.phone_number=user.phone_number
        profile_image=get_object_or_404(UserProfile,user=user)
        block_user.profile_image=profile_image
        user.save()
        block_user.save()
        path=self.request.path
        print(path)
        if path =='/block/user/':
            return redirect('users')
        elif path == '/block/users/':
            return redirect('users-details')    




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
        path=self.request.path
        messages.success(request,f'{get_user.username} has been remove from the block list ')
        if path =='/unblock-users/':
            return redirect('block-users')
        elif path =='/unblock-user/':
            return redirect('users-details')        
        # return redirect('user-details')



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



class RequestBook(View):

    def post(self,request):
        get_user=request.user
        product_id=request.POST['product_id']
        user=get_object_or_404(User,pk=get_user.id)
        get_owner=get_object_or_404(Products,pk=product_id)
        requested_book=RequestedBook()
        requested_book.product_owner=get_owner
        requested_book.requestd_user=user
        user.booked_requests+=1
        requested_book.save()
        user.save()
        messages.success(request,'Request has been sent to the owner')

        path=self.request.path
        if path=='/users/user':
            return redirect(f'{path}/{requested_book.product_owner.user.id}')         
        elif path=='/user/item':
            return redirect(f'{path}/{product_id}')
      

        # return redirect(f'/user/item/{product_id}')
        
class BookView(ListView):
    template_name='app/requested_book.html'
    model=RequestedBook
    context_object_name='users'
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        user=self.request.user
        # print(user.id)
        user=get_object_or_404(User,pk=user.id)
        prodcut_owner=Products.objects.filter(user=user).first()
        # print(prodcut_owner)    
        owner=RequestedBook.objects.filter(product_owner__user__id=user.id)
        context['users']=owner
        return context
   


class BookedUserAccept(View):
    def post(self,request):
        user_id=request.POST['user_id']
        product=get_object_or_404(RequestedBook,pk=user_id)
        get_product=get_object_or_404(Products,pk=product.product_owner.id)
        print(get_product.product)
        other_products=RequestedBook.objects.filter(product_owner__product=get_product.product)
     
        for other_product in other_products :
            other_product.is_rejected=True
            other_product.is_pending=False
            other_product.save()
        product.is_pending=False
        product.is_rejected=False
        product.is_accepted=True
        get_product.is_booked=True
        get_product.save()  
        product.save() 
       
        return redirect('requested-book')


class BookedUserReject(View):

    def post(self,request):
        user_id=request.POST['user_id']
        # user=get_object_or_404(User,pk=user_id)
        product=get_object_or_404(RequestedBook,pk=user_id)
        product.is_pending=False
        product.is_rejected=True
        product.save()
        return redirect('requested-book')


class UserBookedItem(ListView):
    model=RequestedBook
    template_name='app/booked_item.html'
    context_object_name='booked_items'
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        get_user=self.request.user
        user=get_object_or_404(User,pk=get_user.id)
        booked_items=RequestedBook.objects.filter(requestd_user=user)
        context['booked_items']=booked_items
        return context
    

