import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Profile, Product, Order
from django.db.models import Count, Q, F


def get_profiles(search_string=None):
    result = []
    if search_string is not None:
        profiles = Profile.objects.annotate(num_of_orders=Count('profile_orders')).filter(
            Q(full_name__icontains=search_string) |
            Q(email__icontains=search_string) |
            Q(phone_number__icontains=search_string)).order_by('full_name')

        [result.append(f"Profile: {p.full_name}, "
                       f"email: {p.email}, "
                       f"phone number: {p.phone_number}, "
                       f"orders: {p.num_of_orders}") for p in profiles]

    return '\n'.join(result) if result else ''


def get_loyal_profiles():
    profiles = Profile.objects.get_regular_customers()

    if not profiles:
        return ''

    result = []

    [result.append(f"Profile: {p.full_name}, orders: {p.num_orders}") for p in profiles]

    return '\n'.join(result)


def get_last_sold_products():
    try:
        latest_order = Order.objects.prefetch_related('products').latest('creation_date')
        order_products = latest_order.products.all().order_by('name')
        if not order_products:
            return ''
        all_products = ', '.join(p.name for p in order_products)

        return f"Last sold products: {all_products}"
    except Order.DoesNotExist:
        return ''


def get_top_products():
    top_products = (Product.objects.prefetch_related('product_orders').annotate(num_orders=Count('product_orders'))
                    .filter(num_orders__gt=0)
                    .order_by('-num_orders', 'name'))[:5]

    if top_products:
        # result = '\n'.join(f"{p.name}, sold {p.num_orders} times" for p in top_products)
        result = []
        [result.append(f"{p.name}, sold {p.num_orders} times") for p in top_products]
        result = '\n'.join(result)
        return f"Top products:\n{result}"
    return ''


def apply_discounts():
    orders = ((Order.objects.annotate(num_of_updated_orders=Count('products')))
              .filter(num_of_updated_orders__gt=2, is_completed=False)
              .update(total_price=F('total_price') * 0.9))

    return f"Discount applied to {orders} orders."


def complete_order():
    com_order = (Order.objects.prefetch_related('products')
                 .filter(is_completed=False)
                 .order_by('creation_date')
                 .first())

    if com_order is None:
        return ''

    com_order.is_completed = True
    com_order.save()

    for product in com_order.products.all():
        product.in_stock -= 1

        if product.in_stock == 0:
            product.is_available = False

        product.save()

    return 'Order has been completed!'
