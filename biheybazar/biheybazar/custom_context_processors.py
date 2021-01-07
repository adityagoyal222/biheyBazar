from customers.models import Customer
from vendors.models import Vendor

def customer_vendor(request):
    customer = ''
    vendor = ''
    if request.user.is_authenticated:
        if request.user.is_customer:
            customer = Customer.objects.filter(user = request.user).first()
        elif request.user.is_authenticated:
            vendor = Vendor.objects.filter(user = request.user).first()
    return {
        "customer_context": customer,
        "vendor_context": vendor,
    }