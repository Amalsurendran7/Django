
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from django.urls import reverse

from django.utils.crypto import get_random_string




# Create your models here.


class MyAccountManager(BaseUserManager):
    def create_user(self, fname, lname, username, email,referral,password=None,address=None,):
        if not email:
            raise ValueError('User must have an email address')

        if not username:
            raise ValueError('User must have an username')

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            fname = fname,
            lname = lname,
            address=address,
            
            referral=referral
        )

        user.set_password(password)
        user.save(using=self._db)
        
        return user

    def create_superuser(self, fname, lname, email, username,password,referral=get_random_string(length=32) ):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            fname = fname,
            lname = lname,
            referral=referral,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user






class customer(AbstractBaseUser):
    fname=models.CharField(max_length=15)
    lname=models.CharField(max_length=150)
    username=models.CharField(max_length=150,unique=True)
    email=models.CharField(max_length=150)
    phone=models.CharField(max_length=150)
    address=models.CharField(max_length=150,null=True)
    password=models.CharField(max_length=150)
    referral=models.CharField(max_length=250,default="None")
   
    status=models.CharField(max_length=150,default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin  = models.BooleanField(default=False)
    is_staff   = models.BooleanField(default=False)
    is_active   = models.BooleanField(default=True)
    is_superadmin   = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['fname','lname','email']

    objects = MyAccountManager()

    def full_name(self):
        return f'{self.fname} {self.lname}'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True


    
  

    
    
    def get_absolute_url(self):
        return reverse("adm", args=[ self.slug])



class category(models.Model):
    category_name=models.CharField(max_length=15)
    slug = models.SlugField(max_length=100, unique=True,null=True)

    def __str__(self):
        return self.category_name

    def get_url(self):
            return reverse('products_by_category', args=[self.slug])    
    
    

class produc(models.Model):
    name=models.CharField(max_length=15)
    price=models.IntegerField()
    description=models.TextField()
    img=models.ImageField(blank=True, null=True, upload_to='static')
    slug = models.SlugField(max_length=100, unique=True,null=True)
    p_offer=models.BooleanField(default=False)
    c_offer=models.BooleanField(default=False)
    o_percentage=models.IntegerField(null=True,default=False)
    


    img2=models.ImageField(upload_to='static',default=True)
    img3=models.ImageField(upload_to='static',default=True)
    img4=models.ImageField(upload_to='static',default=True)
    status=models.CharField(default='False',max_length=10)
    cate_id=models.ForeignKey(category,on_delete=models.CASCADE,default=True)
    stock=models.IntegerField(null=True)
    offer=models.CharField(max_length=30,default="None")

    def __str__(self):
        return self.name

    def get_url(self):
            return reverse('products_by_price', args=[self.slug])       
    

class banner(models.Model):
    desc=models.TextField()
    image=models.ImageField(upload_to='static')
    title=models.CharField(max_length=20,default=True)


class wish(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

class sales_report(models.Model):
    date = models.DateField(null=True)
    product_name = models.CharField(null=True,max_length=100)
    quantity = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)


class monthly_sales_report(models.Model):
    date = models.DateField(null=True)
    product_name = models.CharField(null=True, max_length=100)
    quantity = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)        


class wishItem(models.Model):
    user = models.ForeignKey(customer, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(produc, on_delete=models.CASCADE)
    
    cart    = models.ForeignKey(wish, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quantity

    def __unicode__(self):
        return self.product


class Address(models.Model):
    useradd = models.ForeignKey(customer, on_delete=models.CASCADE, null=True,related_name='hello')
    addresssave=models.CharField(max_length=100)


class Wallet(models.Model):
    user_e= models.CharField(max_length=100,default=True)
    w_amount=models.IntegerField(null=True)    



     
     

