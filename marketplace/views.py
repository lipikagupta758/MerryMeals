from decimal import Decimal
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from .context_processors import get_cart_counter
from vendor.models import Vendor, Category, FoodItem
from django.db.models import Prefetch
from .models import Cart, Restaurant_Cart
from django.contrib.auth.decorators import login_required
# Create your views here.

def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
    vendors_count= vendors.count()
    context= {
        'vendors': vendors,
        'vendors_count': vendors_count
    }
    return render(request, 'marketplace/listings.html', context)

def vendor_detail(request, vendor_slug):
    vendor= get_object_or_404(Vendor, vendor_slug= vendor_slug) 
    categories= Category.objects.filter(vendor= vendor).prefetch_related(
        Prefetch(
            'foodItems',
            queryset=FoodItem.objects.filter(is_available=True)
        )
    )
    if request.user.is_authenticated:
        cart_items= Restaurant_Cart.objects.filter(user= request.user)
    else:
        cart_items= None
    context={
        'vendor': vendor,
        'categories': categories,
        'cart_items': cart_items,
    }

    return render(request, 'marketplace/vendor-detail.html', context)

def add_to_cart(request, food_id):
    if request.user.is_authenticated:
        # to check if the request is from ajax code
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                foodItem= FoodItem.objects.get(id= food_id)
                vendor= foodItem.vendor
                try:
                    chkCart= Restaurant_Cart.objects.get(user= request.user, foodItem= foodItem, vendor= vendor)
                    chkCart.quantity+=1
                    chkCart.save()
                    return JsonResponse({'status':'Success', 'message':'Increased cart quantity', 'cart_counter': get_cart_counter(request),  'quantity': chkCart.quantity})
                except:
                    chkCart= Restaurant_Cart.objects.create(user= request.user, foodItem= foodItem, quantity=1, vendor= vendor)
                    cart_exists= Cart.objects.filter(user= request.user, vendor= vendor).exists()
                    
                    if not cart_exists: 
                        cart= Cart.objects.create(user= request.user, vendor= vendor)
                    
                    return JsonResponse({'status':'Success', 'message':'Added item to cart', 'cart_counter': get_cart_counter(request),   'quantity': chkCart.quantity})

            except:
                return JsonResponse({'status':'Failed', 'message':'The food item does not exist'})
        else:
            foodItem= FoodItem.objects.get(id= food_id)
            vendor= foodItem.vendor
            try:
                chkCart= Restaurant_Cart.objects.get(user= request.user, foodItem= foodItem, vendor= vendor)
                chkCart.quantity+=1
                chkCart.save()
            except:
                chkCart= Restaurant_Cart.objects.create(user= request.user, foodItem= foodItem, quantity=1, vendor= vendor)
                cart_exists= Cart.objects.filter(user= request.user, vendor= vendor).exists() 
                if not cart_exists: 
                    cart= Cart.objects.create(user= request.user, vendor= vendor)
            return redirect('cart', vendor_slug= foodItem.vendor.vendor_slug)
    else:
        return JsonResponse({'status':'login_required', 'message': 'You must be logged in to add items to cart'})
   
def decrease_cart(request, food_id):
    if request.user.is_authenticated:
        # to check if the request is from ajax code
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                foodItem= FoodItem.objects.get(id= food_id)
                vendor= foodItem.vendor
                try:
                    chkCart= Restaurant_Cart.objects.get(user= request.user, foodItem= foodItem, vendor= vendor)
                    if chkCart.quantity>1:
                        chkCart.quantity-=1
                        chkCart.save()
                    else:
                        chkCart.delete()
                        count= Restaurant_Cart.objects.filter(user= request.user, vendor= vendor).count()
                        if count==0:
                            cart= Cart.objects.get(user= request.user, vendor= vendor).delete()
                    return JsonResponse({'status': 'Success', 'message':'Decreased cart quantity', 'cart_counter': get_cart_counter(request),  'quantity': chkCart.quantity})
                except:
                    return JsonResponse({'status': 'Failed', 'message':'Invalid operation', 'quantity': 0})

            except:
                return JsonResponse({'status': 'Failed', 'message':'The food item does not exist'})
        else:
            foodItem= FoodItem.objects.get(id= food_id)
            vendor= foodItem.vendor
            chkCart= Restaurant_Cart.objects.get(user= request.user, foodItem= foodItem, vendor= vendor)
            if chkCart.quantity>1:
                chkCart.quantity-=1
                chkCart.save()
            else:
                chkCart.delete()
                count= Restaurant_Cart.objects.filter(user= request.user, vendor= vendor).count()
                if count==0:
                    cart= Cart.objects.get(user= request.user, vendor= vendor).delete()
            return redirect('cart', vendor_slug= foodItem.vendor.vendor_slug )
    else:
        return JsonResponse({'status': 'login_required', 'message': 'You must be logged in to add items to cart'})

@login_required(login_url='login')
def cart(request, vendor_slug):
    vendor= Vendor.objects.get(vendor_slug= vendor_slug)
    cart_items= Restaurant_Cart.objects.filter(user=request.user, vendor= vendor).order_by('created_at')

    # subtotal and total amount
    subtotal=0
    for item in cart_items:
        subtotal+= (item.foodItem.price* item.quantity)
    tax=  subtotal* Decimal('0.18')
    total=  subtotal + tax

    context={
        'cart_items': cart_items,
        'vendor': vendor,
        'subtotal': subtotal,
        'tax': tax,
        'total': total,
    }
    # Check if the request is AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Return JSON response for AJAX requests
        return JsonResponse({
            'subtotal': float(subtotal),
            'tax': float(tax),
            'total': float(total),
    })
    
    return render(request, 'marketplace/cart.html', context)

@login_required(login_url='login')
def user_carts(request):
    restaurant_carts= Cart.objects.filter(user= request.user).order_by('created_at').order_by('created_at')
    context={
        'restaurant_carts': restaurant_carts
    }
    return render(request, 'marketplace/user_carts.html', context)

@login_required(login_url='login')
def delete_cart(request, cart_id):
    cart_item= Restaurant_Cart.objects.get(id= cart_id)
    cart_item.delete()
    return redirect('cart', vendor_slug= cart_item.vendor.vendor_slug)
