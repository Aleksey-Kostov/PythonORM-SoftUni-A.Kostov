import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Profile, Product, Order
from django.db.models import Count, Q


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
    latest_order = Order.objects.prefetch_related('products').latest('creation_date')
    order_products = latest_order.products.all().order_by('name')

    if not latest_order or not order_products:
        return ''

    all_products = ', '.join(p.name for p in order_products)

    return f"Last sold products: {all_products}"
