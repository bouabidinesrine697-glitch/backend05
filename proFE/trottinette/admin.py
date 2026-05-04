from django.contrib import admin
from .models import Trottinette, Maintenance, TrottinetteBooking  

admin.site.register(Trottinette)
admin.site.register(Maintenance)
admin.site.register(TrottinetteBooking)

