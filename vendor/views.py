from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse
from .forms import VendorRegisterationForm, CategoryForm, FoodItemForm
from accounts.forms import UserProfileForm
from django.shortcuts import get_object_or_404
from accounts.models import UserProfile
from .models import Vendor,Category, FoodItem
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_vendor
from django.template.defaultfilters import slugify

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vprofile(request):
    profile= get_object_or_404(UserProfile, user= request.user)
    vendor=get_object_or_404(Vendor, user= request.user)
    
    if request.method=='POST':
        profile_form= UserProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form= VendorRegisterationForm(request.POST, request.FILES, instance= vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, 'Settings updated.')
            return redirect('vprofile')

        else:
            messages.error(request, str(profile_form.errors))
            messages.error(request, str(vendor_form.errors))
    else:
        profile_form= UserProfileForm(instance= profile)
        vendor_form= VendorRegisterationForm(instance=vendor)
    context={
        'profile_form':profile_form,
        'vendor_form':vendor_form,
        'profile': profile,
        'vendor': vendor,
    }
    return render(request, 'vendor/vprofile.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def menu_builder(request):
    vendor= Vendor.objects.get(user= request.user)
    categories= Category.objects.filter(vendor= vendor).order_by('created_at')
    context={
        'categories': categories,
    }
    return render(request, 'vendor/menu_builder.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def foodItem_by_category(request, pk=None):
    vendor= Vendor.objects.get(user= request.user)
    category= get_object_or_404(Category, pk=pk)
    foodItems= FoodItem.objects.filter(vendor= vendor, category= category)

    return render(request, 'vendor/foodItem_by_category.html', {'foodItems': foodItems, 'category': category})

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_category(request):
    if request.method== 'POST':
        form= CategoryForm(request.POST)
        vendor= Vendor.objects.get(user= request.user)
        if form.is_valid():
            cat_name= form.cleaned_data['category_name']
            category= form.save(commit=False)
            category.vendor= vendor
            category.save()
            category.slug= slugify(cat_name)+'-'+ str(category.id)
            category.save()
            form.save()
            messages.success(request, "Category has been added!")
            return redirect('menu_builder')
    else:
        form= CategoryForm()

    context={'form': form}
    return render(request,  'vendor/add_category.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_category(request, pk=None):
    category= get_object_or_404(Category, id= pk)
    if request.method== 'POST':
        form= CategoryForm(request.POST, instance=category)
        if form.is_valid():
            cat_name= form.cleaned_data['category_name']
            category= form.save(commit=False)
            category.slug= slugify(cat_name)
            form.save()
            messages.success(request, "Category has been updated!")
            return redirect('menu_builder')
    else:
        form= CategoryForm(instance= category)

    context={
        'form': form,
        'category': category
    }
    return render(request, 'vendor/edit_category.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_category(request, pk=None):
    category= get_object_or_404(Category, id=pk)
    category.delete()
    messages.success(request, "Category has been successfully deleted!")
    return redirect('menu_builder')

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_foodItem(request):
    vendor= get_object_or_404(Vendor, user= request.user)
    if request.method== 'POST':
        form= FoodItemForm(request.POST, request.FILES)
        if form.is_valid():
            food_name= form.cleaned_data['food_title']
            foodItem= form.save(commit=False)
            foodItem.vendor= vendor
            foodItem.slug= slugify(food_name)
            form.save()
            messages.success(request, "Food Item has been created successfully!")

            return HttpResponseRedirect(reverse('foodItem_by_category', args=(foodItem.category.id,)))
    else:
        form= FoodItemForm()
        form.fields['category'].queryset= Category.objects.filter(vendor= vendor)

    context={
        'form': form,
    }
    return render(request, 'vendor/add_foodItem.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_foodItem(request, pk):
    foodItem= get_object_or_404(FoodItem, id= pk)
    vendor= get_object_or_404(Vendor, user= request.user)
    if request.method== 'POST':
        form= FoodItemForm(request.POST,request.FILES, instance=foodItem)
        if form.is_valid():
            food_name= form.cleaned_data['food_title']
            cat= form.cleaned_data['category']
            category= get_object_or_404(Category, category_name= cat)
            foodItem= form.save(commit=False)
            foodItem.slug= slugify(food_name)
            form.save()
            messages.success(request, "Food Item has been updated!")

            return HttpResponseRedirect(reverse('foodItem_by_category', args=(category.id,)))
    else:
        form= FoodItemForm(instance= foodItem)
        form.fields['category'].queryset= Category.objects.filter(vendor= vendor)

    context={
        'form': form,
        'foodItem': foodItem
    }
    return render(request, 'vendor/edit_foodItem.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_foodItem(request, pk=None):
    foodItem= get_object_or_404(FoodItem, id=pk)
    category= foodItem.category
    foodItem.delete()
    messages.success(request, "Food Item has been successfully deleted!")
    return HttpResponseRedirect(reverse('foodItem_by_category', args=(category.id,)))

def orders(request):
    pass
def earnings(request):
    pass
def statement(request):
    pass
def changepassword(request):
    pass
