import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Profile, Product, Order
from django.db.models import Q, Count, F


def get_profiles(search_string=None):
    if search_string is None:
        return ''
    profiles = (Profile.objects.annotate(num_orders=Count('profile_orders'))
                .filter(Q(full_name__icontains=search_string)
                        | Q(email__icontains=search_string)
                        | Q(phone_number__icontains=search_string)).order_by('full_name'))

    if not profiles:
        return ''

    result = []

    [result.append(f"Profile: {p.full_name}, email: {p.email}, "
                   f"phone number: {p.phone_number}, "
                   f"orders: {p.num_orders}") for p in profiles]

    return '\n'.join(result)


def get_loyal_profiles():
    profiles = Profile.objects.get_regular_customers()

    if not profiles:
        return ''

    result = []
    [result.append(f"Profile: {p.full_name}, orders: {p.num_orders}") for p in profiles]
    return '\n'.join(result)


def get_last_sold_products():
    try:
        products = Order.objects.prefetch_related('products').latest('creation_date')
        products = products.products.all().order_by('name')
        if not products:
            return ''

        product_name = ', '.join(p.name for p in products)
        return f"Last sold products: {product_name}"
    except Order.DoesNotExist:
        return ''


def get_top_products():
    products = (Product.objects.prefetch_related('product_order')
                .annotate(num_orders=Count('product_order'))
                .filter(num_orders__gt=0)
                .order_by('-num_orders', 'name'))[:5]

    if not products:
        return ''
    if products:
        result = []
        [result.append(f"{p.name}, sold {p.num_orders} times") for p in products]
        result = '\n'.join(result)

        return f"Top products:\n{result}"
    return ''


# print(get_top_products())

def apply_discounts():
    orders = (Order.objects.annotate(num_products=Count('products'))
              .filter(num_products__gt=2, is_completed=False).update(total_price=F('total_price') * 0.9))

    return f"Discount applied to {orders} orders."


# print(apply_discounts())


def complete_order():
    order = (Order.objects.prefetch_related('products')
             .filter(is_completed=False)
             .order_by('creation_date')
             .first())

    if order is None:
        return ''

    order.is_completed = True
    order.save()

    for product in order.products.all():
        product.in_stock -= 1

        if product.in_stock == 0:
            product.is_available = False

        product.save()

    return "Order has been completed!"
