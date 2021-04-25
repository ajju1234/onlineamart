import string
import random

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from django.shortcuts import render, redirect
from django.views.generic import View

from shopping.models import Product, Cart, Item, Review
from shopping.form import ReviewForm, LoginForm

# Create your views here.
def index(request):
    user = request.user
    items = ''
    if user.is_anonymous:
        user = ''
    else:
        items = Item.objects.filter(cart__user=user, cart__checked_out=False)
        items = items.count() if items else 0
    products = Product.objects.filter(total_items__gt=0)

    return render(request, 'index.html', {'products':products, 'user':user, 'items':items, 'page':'home'})


def add_to_cart(request, product_id):
    user = request.user
    if not user.is_authenticated:
        return redirect('user_login')    
    product_id = product_id
    print('product is hai ye',product_id)
    cart = Cart.objects.filter(checked_out=False, user=user)
    cart = cart[0] if cart else ''
    if not cart:
        cart = Cart.objects.create(user=user)
    Item.objects.create(cart=cart, product_id=product_id, quantity=1)
    messages.info(request, "Item added to cart")
    return redirect('index')

def calculate_sum(cart_items):
    items_sum = 0
    for item in cart_items:
        items_sum = items_sum + (item.quantity * item.product.unit_price)
    return items_sum

def cart(request):
    user = request.user
    items= ''
    cart_items = []
    if not user.is_authenticated:
    	return redirect('user_login')
    else:
        cart_items = Item.objects.filter(cart__user=user, cart__checked_out=False)
        items = cart_items.count() if cart_items else 0
    items_sum = calculate_sum(cart_items)
    return render(request, 'cart.html', {'user':user, 'items':items, 'page':'cart', 'cart_items': cart_items, 'sum':items_sum})

def update_item_quantity(request):
    item_id = request.GET.get('item_id')
    quantity = request.GET.get('quantity')
    item = Item.objects.get(id=item_id)
    if item.product.total_items > int(quantity):
        item.quantity = quantity
        item.save()
    return redirect('cart')

def thank_you(request):
    user = request.user
    items = ''
    cart_items = []
    if not user.is_authenticated:
    	return redirect('user_login')
    else:
        cart_items = Item.objects.filter(cart__user=user, cart__checked_out=False)
        items = cart_items.count() if cart_items else 0
    items_sum = calculate_sum(cart_items)
    return render(request, 'thankyou.html', {'user':user, 'items':items, 'page':'cart', 'cart_items':cart_items, 'sum':items_sum})

def remove_item(request):
    item_id = request.GET.get('item_id')
    Item.objects.get(id=item_id).delete()
    return redirect('cart')

def confirm_order(request):
    user = request.user
    cart_items = Item.objects.filter(cart__user=user, cart__checked_out=False)
    items_sum = calculate_sum(cart_items)
    cart = Cart.objects.get(user=user, checked_out=False)
    cart.checked_out = True
    cart.save()
    User.objects.filter(username=user.username).delete()
    return render(request, 'thankyou.html', {'user':user, 'items':0, 'page':'cart', 'cart_items':cart_items, 'sum':items_sum, 'shopping':'Continue Shopping'})

def credit_card_page(request):
    return render(request, 'credit_card.html',{})


########
###Review
#######
def product_details(request, product_id):
	user = request.user
	if user.is_anonymous:
		user = ''
	product = [Product.objects.get(id=product_id)]
	print('product for review',str(product))
	reviews = Review.objects.filter(product_id=product_id)
	# for rev in reviews:
	# 	print(rev.user)
	return render(request, 'details.html', {'product':product, 'reviews':reviews})

def add_review(request, product_id):
	if request.method=="POST":
		form =  ReviewForm(request.POST)
		if form.is_valid():
			rating = form.cleaned_data.get("rating")
			review_text= form.cleaned_data.get("review_text")

			post = Review(user=request.user, product_id=product_id, rating =  rating, review_text=review_text)
			post.save()
			return redirect('product_details', product_id=post.product_id)

	user = request.user
	if user.is_anonymous:
		chars = string.ascii_uppercase + string.digits
		user_name = ''.join(random.choice(chars) for _ in range(9))
		password = '1234567a'
		user = User.objects.create(username=user_name, first_name='guest', last_name='guest', email='guest@gmail.com', is_active=True, is_staff=True)
		user.set_password(password)
		user.save()
		user = authenticate(username=user_name, password=password)
		if user:
			login(request, user)

	product_id = product_id
	form = ReviewForm()
	return render(request, 'add_review.html',{'form':form, "product_id":product_id})


####################
######## User Authentication###############
def user_login(request):
	if request.method == "POST":
		form = LoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get("username")
			password = form.cleaned_data.get("password")
			user = authenticate(request, username=username, password=password)
			if user is not None:
				login(request, user)
				return redirect('index')
			else:
				messages.info(request, "Invalid Credentials!")
				return redirect('user_login')
	else:
		form = LoginForm()
		return render(request, 'login.html', {"form":form})

def user_registration(request):
	# if request.user.is_authenticated:
	# 	return redirect('index')
	if request.method=="POST":
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, "Congratulations! You are signed up")
			return redirect('index')
			# return redirect('user_login')
		else:
			messages.error(request, "Enter valid information")
			return redirect(user_registration)
	else:
		form = UserCreationForm()
		return render(request, "register.html", {"form":form})

def user_logout(request):
	logout(request)
	return redirect('index')