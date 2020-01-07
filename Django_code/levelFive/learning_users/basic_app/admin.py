from django.contrib import admin
from basic_app.models import UserProfileInfo
# Register your models here.
# register the model we created to the admin
# if we login as an admin we can wee the actual model
admin.site.register(UserProfileInfo)
