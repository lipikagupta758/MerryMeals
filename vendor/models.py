from django.db import models
from accounts.models import User, UserProfile
from accounts.utils import send_notification

# Create your models here.
class Vendor(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    user_profile= models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='user_profile')
    vendor_name= models.CharField(max_length=50)
    vendor_slug= models.SlugField(max_length=100, unique=True)
    vendor_license= models.ImageField(upload_to='vendor/license')
    is_approved= models.BooleanField(default=False)
    created_at= models.DateTimeField(auto_now_add=True)
    modified_at= models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vendor_name
    
    def save(self, *args, **kwargs):
        if self.pk is not None:
            original_status= Vendor.objects.get(pk=self.pk)
            if original_status.is_approved != self.is_approved:
                mail_template= 'accounts/emails/admin_approval_email.html'
                context= {
                    'user': self.user,
                    'is_approved': self.is_approved,
                }
                if self.is_approved== True:
                    mail_subject= "Congratulations! Your restaurant has been approved."
                    send_notification(mail_subject, mail_template, context)
                    # Send notification email
                    
                else:
                    # Send notification mail for unapproved vendor account
                    mail_subject= "We are sorry! Your restaurant is not eligible for pulishing your food menu on our marketplace."
                    send_notification(mail_subject, mail_template, context)
        return super(Vendor, self).save(*args, **kwargs)

class Category(models.Model):
    vendor= models.ForeignKey(Vendor, on_delete=models.CASCADE)
    category_name= models.CharField(max_length=50, unique= True)
    slug= models.SlugField(max_length=100, unique=True)
    description= models.TextField(max_length=250, blank=True)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name= 'category'
        verbose_name_plural= 'categories'
    
    def __str__(self):
        return self.category_name
    
    def clean(self):
        self.category_name= self.category_name.capitalize()
        
class FoodItem(models.Model):
    vendor= models.ForeignKey(Vendor, on_delete=models.CASCADE)
    category= models.ForeignKey(Category, on_delete=models.CASCADE, related_name='foodItems')
    food_title= models.CharField(max_length=50, unique= True)
    slug= models.SlugField(max_length=100, unique=True)
    description= models.TextField(max_length=250, blank=True)
    price= models.DecimalField(max_digits=10, decimal_places=2)
    image= models.ImageField(upload_to='foodImages')
    is_available= models.BooleanField(default=True)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.food_title
    
    def clean(self):
        self.food_title= self.food_title.capitalize()