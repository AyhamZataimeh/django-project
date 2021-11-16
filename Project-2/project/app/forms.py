from django import forms
from django.contrib.auth import authenticate, get_user_model
from .models import ProfileImage, Products

User=get_user_model()

class UserLogin(forms.Form):
    email=forms.EmailField(label='Email',max_length=80)
    password=forms.CharField(label='Password',widget=forms.PasswordInput)
    email.widget.attrs['class']='form-control'
    password.widget.attrs['class']='form-control'

    def clean(self,*args,**kwargs):
        email=self.cleaned_data['email']
        password=self.cleaned_data['password']
        if email and password:
            user=authenticate(username=email,password=password)

            if not user:
                raise forms.ValidationError(' user dosent exsit ')
           
            if not user.is_active:
                raise forms.ValidationError('User doesnt exit ')        
        return super(UserLogin,self).clean(*args,**kwargs)

class UserSignup(forms.ModelForm):
    username=forms.CharField(label='Name',max_length=80)
    email=forms.EmailField(label='Email',max_length=80)
    password=forms.CharField(label='Password',widget=forms.PasswordInput)
    password2=forms.CharField(label=' Confrim Password',widget=forms.PasswordInput)
    phone_number=forms.CharField(label='Phone Number')
    # gender=forms.CharField(label='Gender')
    
    username.widget.attrs['class']='form-control'
    email.widget.attrs['class']='form-control'
    password.widget.attrs['class']='form-control'
    password2.widget.attrs['class']='form-control'
    phone_number.widget.attrs['class']='form-control'
    # gender.widget.attrs['class']='form-check-input'

    def __init__(self,*args,**kwargs):
        super(UserSignup,self).__init__(*args,**kwargs)
        
        # for field in self.visible_fields():
        #     field.field.widget.attrs['class']='form-control'


    
    class Meta:
        model=User
        fields=['username','email','password','password2','gender','phone_number']
        widgets={
            'gender':forms.widgets.RadioSelect
        }
    def clean(self,*args,**kwargs):
        username=self.cleaned_data['username']
        email=self.cleaned_data['email']
        password=self.cleaned_data['password']
        password2=self.cleaned_data['password2']
        phone_number=self.cleaned_data['phone_number']


        if password != password2:
            raise forms.ValidationError(' Password must match ')

        check_email=User.objects.filter(email=email)
        check_user=User.objects.filter(username=username)
        check_phone_number=User.objects.filter(phone_number=phone_number)

        if check_email.exists():
            raise forms.ValidationError(f'{email} already exsit')

        if check_user.exists():
            raise forms.ValidationError(f'{username} already exsit ') 

        if check_phone_number.exists():
            raise forms.ValidationError('phone number already exsit')


        return super(UserSignup,self).clean(*args,**kwargs)


class UserUpdate(forms.ModelForm):

    username=forms.CharField(max_length=80,label='new name')
    email=forms.EmailField(max_length=80,label='new email')
    phone_number=forms.CharField(max_length=80,label='new phone number')
    
    class Meta:
        model=User
        fields=['username','email','phone_number']
        labels={
            'username':'New name',
            'email':'New email',
            'phone_number':'New phone number'
        }
    def clean(self,*args,**kwargs):
        username=self.cleaned_data['username']
        email=self.cleaned_data['email']
        phone_number=self.cleaned_data['phone_number']

        check_username=User.objects.filter(username=username)
        check_email=User.objects.filter(email=email)
        check_phone_number=User.objects.filter(phone_number=phone_number)

        if check_username.exists():
            raise forms.ValidationError('user with that name already exsit try another one ')

        if check_email.exists():
            raise forms.ValidationError('user with that email already exsit try another one')    
        
        if check_phone_number.exists():
            raise forms.ValidationError('user with that phone number already exsit try another one')    


        return super(UserUpdate,self).clean(*args,**kwargs)    
        

class ProfileImage(forms.ModelForm):

    image=forms.ImageField()
    class Meta:
        model=ProfileImage
        fields=['image']


class UserPosts(forms.ModelForm):
  

    class Meta:
        model=Products
        fields=['product','product_image']
        labels={
            'product':'Product description',
            'product_image':'Prodcut Image'
        }

class Booked(forms.ModelForm):
    class Meta:
        model=Products
        fields=['is_booked']
