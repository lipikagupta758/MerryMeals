from django import forms
from .models import Vendor, Category, FoodItem, OpeningHours
from accounts.validators import allow_only_images_validator

class VendorRegisterationForm(forms.ModelForm):
    vendor_license= forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[allow_only_images_validator], required=False)
    class Meta:
        model= Vendor
        fields=['vendor_name', 'vendor_license']

class CategoryForm(forms.ModelForm):
    class Meta:
        model=  Category
        fields=['category_name', 'description']

class FoodItemForm(forms.ModelForm):
    image= forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[allow_only_images_validator], required=False)

    class Meta:
        model= FoodItem
        fields=['category', 'food_title', 'description', 'price', 'image', 'is_available']

class OpeningHoursForm(forms.ModelForm):
    class Meta:
        model= OpeningHours
        fields= ['day', 'from_hour', 'to_hour', 'is_closed']
