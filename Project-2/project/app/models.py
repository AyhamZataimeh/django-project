from django.core.exceptions import MiddlewareNotUsed
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.timezone import now
from PIL import Image
from django.utils.translation import gettext_lazy as _

class UserAccountManager(BaseUserManager):
    def create_user(self, username,email,password):
        if not username:
            raise ValueError(' User must have a name')
        if not email:
            raise ValueError('User must have Email')    

        user=self.model(username=username,email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self,username,email,password):
        user=self.create_user(username=username,email=self.normalize_email(email),password=password)
        user.is_admin=True
        user.is_staff=True 
        user.is_superuser=True
        user.save(using=self._db)
        return user   

male='male'
female='female'
gender=(
    (male,'male'),
    (female,'female')
)

class UserAccount(AbstractBaseUser):
    class Gender(models.TextChoices):
        male='male',_('male')
        female='female',_('female')
    username=models.CharField(max_length=80,unique=True)
    email=models.EmailField(max_length=80,unique=True,verbose_name='Email')
    phone_number=models.CharField(max_length=10,verbose_name='Phone Number',unique=True)
    password=models.CharField(max_length=80,verbose_name='Password')
    gender=models.CharField(max_length=10,choices=Gender.choices,null=True)
    login_date=models.DateField(verbose_name='Login date',auto_now_add=True)
    last_login=models.DateField(verbose_name='Last Login',auto_now=True)
    rejected_post=models.IntegerField(default=0)
    blocked=models.BooleanField(default=False)
    is_admin=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    
    objects=UserAccountManager()   
   
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username']

    def __str__(self) -> str:
        return self.username

    def has_perm(self,perm,obj=None,):
        return self.is_admin

    def has_module_perms(self,app_label):
        return True    

class ProfileImage(models.Model):
    image=models.ImageField(upload_to='images',blank=True,null=True)
    user=models.OneToOneField(UserAccount,on_delete=models.CASCADE,null=True)

    def __str__(self) -> str:
        return f'{self.user.username} profile image'
          

    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        img=Image.open(self.image.path)
        if img.height>300 or img.width>300:
            reszie=(300,300)
            img.thumbnail(reszie)
            img.save(self.image.path)



    


class Products(models.Model):
    product=models.CharField(max_length=80)
    post_date=models.DateField(default=now)
    product_image=models.ImageField(upload_to='products')
    is_booked=models.BooleanField(default=False)
    is_pending=models.BooleanField(default=True)
    is_rejected=models.BooleanField(default=False)
    is_accepted=models.BooleanField(default=False)
    user=models.ForeignKey(UserAccount,on_delete=models.CASCADE,null=True)

    
    def __str__(self):
        return f'{self.user.username} prodcut'

    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        img=Image.open(self.product_image.path)
        if img.height>300 or img.width>300:
            reszie=(300,300)
            img.thumbnail(reszie)
            img.save(self.product_image.path)

# Create your models here.