from django import forms
from .models import Vendor, Category, FoodItem
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
    class Meta:
        model= FoodItem
        fields=['category', 'food_title', 'description', 'price', 'image']

