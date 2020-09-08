"""
Vistas
"""
import json
import datetime

from django.shortcuts import render
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt

from .models import *
# Create your views here.
from .utils import cart_data, guest_order


GENDER_SELECT = ''
SELECTED_SIZES = SizesGeneral.objects.values('size')
SELECTED_COLORS = Color.objects.values('color').order_by('color')

MIN_PRICE = 0
MAX_PRICE = 0

def inicio(request):
    data = cart_data(request)
    cart_items = data['cartItems']
    order = data['order']
    items = data['items']

    set_global_values()

    context = {'items':items, 'order':order, 'cartItems':cart_items}
    return render(request, 'tienda/inicio.html', context)

def tienda(request, gender):

    global GENDER_SELECT, MIN_PRICE, MAX_PRICE
    data = cart_data(request)
    cart_items = data['cartItems']

    GENDER_SELECT = gender
    asign_gender = ''
    if gender == 'man':
        asign_gender = 'm'
    else:
        asign_gender = 'f'

    productos = Product.objects.all().filter(gender=asign_gender,size__size__in=get_selected(SELECTED_SIZES,'size'),
    color__in=get_selected(SELECTED_COLORS,'color'), price__range=(MIN_PRICE, MAX_PRICE)).order_by('name').distinct()

    paginator = Paginator(productos, 6)

    pagina = request.GET.get("page") or 1
    post = paginator.get_page(pagina)
    pagina_actual = int(pagina)
    paginas = range(1, post.paginator.num_pages + 1)

    diff = range(0, (6 - post.object_list.count()))

    context = {'productos':post, 'cartItems':cart_items, 'paginas':paginas,
     'pagina_actual':pagina_actual,'sizes':SELECTED_SIZES,'gender':GENDER_SELECT,
     'colors':SELECTED_COLORS,'min_price':MIN_PRICE, 'max_price':MAX_PRICE,'ghosts':diff}

    return render(request, 'tienda/tienda.html', context)

def cart(request):

    data = cart_data(request)
    cart_items = data['cartItems']
    order = data['order']
    items = data['items']

    global GENDER_SELECT

    ctr = False

    if not GENDER_SELECT:
        ctr = True

    context = {'items':items, 'order':order, 'cartItems':cart_items,'gender':GENDER_SELECT,'ctr':ctr}
    return render(request, 'tienda/carro.html', context)

def checkout(request):

    data = cart_data(request)
    cart_items = data['cartItems']
    order = data['order']
    items = data['items']

    global GENDER_SELECT

    context = {'items':items, 'order':order, 'cartItems':cart_items,'gender':GENDER_SELECT}
    return render(request, 'tienda/checkout.html', context)

def update_item(request):
    data = json.loads(request.body)
    product_id = data['productId']
    action = data['action']

    customer = request.user.customer
    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        order_item.quantity = (order_item.quantity + 1)
    elif action == 'remove':
        order_item.quantity = (order_item.quantity - 1)

    order_item.save()

    quantity = order_item.quantity

    if order_item.quantity <= 0:
        order_item.delete()
        quantity = 0

    data_inf = {
        'quantity':quantity,
    }

    return JsonResponse(data_inf)

def process_order(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guest_order(request ,data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('Pago completo', safe=False)

@csrf_exempt
def get_item(request):
    data = json.loads(request.body)
    product_id = data['productId']

    product = Product.objects.get(id=product_id)

    data_item = {
        'name': product.name,
        'price': product.price,
        'url': product.image_url,
    }

    return JsonResponse(data_item)

@csrf_exempt
def set_opt(request):
    data = json.loads(request.body)
    type_req = data['type']

    if type_req == 'price':
        min_price = data['min_price']
        max_price = data['max_price']

        global MIN_PRICE, MAX_PRICE
        MIN_PRICE = min_price
        MAX_PRICE = max_price

    if type_req == 'size':
        action = data['action']
        index = data['index']
        global SELECTED_SIZES
        for obj_size in SELECTED_SIZES:
            if obj_size['size'] == index:
                obj_size['checked'] = action

    if type_req == 'color':
        action = data['action']
        index = data['index']

        global SELECTED_COLORS
        for obj_color in SELECTED_COLORS:
            if obj_color['color'] == index:
                obj_color['checked'] = action

    return JsonResponse({})

def set_global_values():

    global MIN_PRICE, MAX_PRICE, SELECTED_COLORS, SELECTED_SIZES

    MIN_PRICE = 20.00
    MAX_PRICE = 80.00

    for obj in SELECTED_COLORS:
        obj['checked'] = True

    for obj in SELECTED_SIZES:
        obj['checked'] = True

    return True

def get_selected(list_items, target):

    values=[]

    for obj in list_items:
        if obj['checked']:
            values.append(obj[target])

    return values


set_global_values()
