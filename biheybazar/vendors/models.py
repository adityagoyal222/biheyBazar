from django.db import models
from django.db.models.fields import related
from django.urls import reverse
from users.models import User
from django.db.models.deletion import CASCADE
from ckeditor.fields import RichTextField


# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    category_pic = models.ImageField(upload_to="category_pic", blank=True)

    def __str__(self):
        return self.category_name

    def get_absolute_url(self):
        return reverse('home')

class Vendor(models.Model):
   

    user = models.OneToOneField(User, on_delete=CASCADE, primary_key=True)
    vendor_name = models.CharField(max_length=200, blank=False)
    logo = models.ImageField(upload_to='logo')
    cover_image = models.ImageField(upload_to='cover_image')
    slug = models.SlugField(default='')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    about = RichTextField(blank=True,default='',null=True)
    review_int = models.IntegerField(default=0)
    address = models.CharField(max_length=200, blank=True, null=True)
    contact = models.CharField(max_length=15, blank=True, null=True)

    # String representation of vendor model
    def __str__(self):
        return self.vendor_name

    # def total_ratings(self):
    #     from reviews.models import Review
    #     # ratings = Review.objects.filter(vendor=self).only("ratings")
    #     rt = Review.objects.filter(vendor=self).values_list("ratings")
    #     # print(len(rt))
    #     # print(rt)
    #     self.review_int = 1

    def avg_ratings(self):
        from reviews.models import Review
        rt = Review.objects.filter(vendor=self).values_list("ratings")
        # vendor=Vendor.objects.get(vendor_name=self)
        sum = 0
        
        for i in rt:
            for j in i:
                print(j)
                sum+=j

        if len(rt)>0:
            average=sum//len(rt)
            self.review_int = average
            self.save()

    def order_vendor(self):
        vendor = Vendor.objects.all().order_by('-review_int')
        print(vendor)
           
        

            

class VendorImage(models.Model):
    # Model for uploading images to a vendor account
    vendor = models.ForeignKey(Vendor, on_delete=CASCADE, related_name='images')
    image = models.ImageField(upload_to='vendor_images')

class VendorPricing(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=CASCADE, related_name='pricing')
    description = models.CharField(max_length=150, blank=False)
    price = models.CharField(max_length=50, blank=False)

class Tag(models.Model):
    CHOICES = (
        ('Location', 'Location'),
        ('Culture', 'Culture'),
    )
    tag_name = models.CharField(max_length=150)
    tag_type = models.CharField(max_length=10, choices=CHOICES, default=CHOICES[1][1])
    vendors = models.ManyToManyField(Vendor, through="VendorTag", related_name="vendor_tag")

    def __str__(self):
        return self.tag_name
    
    def get_absolute_url(self):
        return reverse('home')

    class Meta:
        ordering = ['tag_name']

class VendorTag(models.Model):
    vendor = models.ForeignKey(Vendor, related_name="vendor_tags", on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, related_name="vendor", on_delete=models.CASCADE)

    def __str__(self):
        return self.vendor.vendor_name

    class Meta:
        unique_together = ('vendor', 'tag')
