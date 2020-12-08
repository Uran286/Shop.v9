from django.contrib import admin

from user.models import User


# Adding app User to Admin site

admin.site.register(User)
