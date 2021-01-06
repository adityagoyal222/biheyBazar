from customers.models import Customer
from vendors.models import Vendor

def customer_vendor(request):
    return {
        "customer_context": Customer.objects.filter(user = request.user).first(),
        "vendor_context": Vendor.objects.filter(user = request.user).first(),
    }