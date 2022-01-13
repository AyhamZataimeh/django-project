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

            if not user.check_password(password):
                    raise forms.ValidationError('Wrong password')            
        return super(UserLogin,self).clean(*args,**kwargs)

class UserSignup(forms.ModelForm):
    username=forms.CharField(label='Name',max_length=80)
    email=forms.EmailField(label='Email',max_length=80)
    password=forms.CharField(label='Password',widget=forms.PasswordInput)
    password2=forms.CharField(label=' Confrim Password',widget=forms.PasswordInput)
    phone_number=forms.CharField(label='Phone Number')
    address=forms.CharField(label='Address')
    st_name=forms.CharField(label='Street')
   
    
    username.widget.attrs['class']='form-control'
    email.widget.attrs['class']='form-control'
    password.widget.attrs['class']='form-control'
    password2.widget.attrs['class']='form-control'
    phone_number.widget.attrs['class']='form-control'
    address.widget.attrs['class']='form-control'
    st_name.widget.attrs['class']='form-control'
  
    
    class Meta:
        model=User
        fields=['username','email','password','password2'
        ,'gender','phone_number','city','address','st_name']
        widgets={
            'gender':forms.widgets.RadioSelect,

            
            

        }
        
    def clean(self,*args,**kwargs):

        username=self.cleaned_data['username']
        email=self.cleaned_data['email']
        password=self.cleaned_data['password']
        password2=self.cleaned_data['password2']
        phone_number=self.cleaned_data['phone_number']
        print(len(password),'1232312')



        if password != password2:
            raise forms.ValidationError(' Password must match ')

        if len(password) <8 or len(password2)<8:
            raise forms.ValidationError('Password must be at least 8 character')    

        check_email=User.objects.filter(email=email)
        check_user=User.objects.filter(username=username)
        check_phone_number=User.objects.filter(phone_number=phone_number)


        if check_user.exists():
            raise forms.ValidationError(f'{username} already exsit ') 


        if check_email.exists():
            raise forms.ValidationError(f'{email} already exsit')

      
        if check_phone_number.exists():
            raise forms.ValidationError('phone number already exsit')


        return super(UserSignup,self).clean(*args,**kwargs)


class UserUpdate(forms.ModelForm):
    username=forms.CharField(max_length=80,label='new name', required=False)
    email=forms.EmailField(max_length=80,label='new email',required=False)
    phone_number=forms.CharField(max_length=80,label='new phone number',required=False)

    def __init__(self, *args, **kwargs):
        super(UserUpdate, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'



    class Meta:
        model=User
        fields=['username','email','phone_number','city','address','st_name']
        labels={
            'username':'New name',
            'email':'New email',
            'phone_number':'New phone number',
            'city':'new address',
            'address':'new address',
            'st_name':'new street'
        }

        

class ProfileImage(forms.ModelForm):
    image=forms.ImageField(required=False)
    
    class Meta:
        model=ProfileImage
        fields=['image']


class UserPosts(forms.ModelForm):
  

    class Meta:
        model=Products
        fields=['product','product_image','category']
        labels={
            'product':'Product description',
            'product_image':'Prodcut Image',
            'category':'product_category'
        }




        