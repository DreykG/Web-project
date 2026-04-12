from django.contrib import admin

from .models import Gang, GangJoinRequest, GangMember, GangMessage, GangVaultRental

# Register your models here.
admin.site.register(Gang)
admin.site.register(GangJoinRequest)
admin.site.register(GangMember)
admin.site.register(GangMessage)
admin.site.register(GangVaultRental)

