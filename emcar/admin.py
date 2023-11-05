from django.contrib import admin
from django.db.models.base import ModelBase

from emcar import models
# from .models import AdminUser, AuditLog, AuditValues, Department, DataLogger, DTC, EmailValidationStatus
# from .models import EmailValidStatus, ClientUser, Client, Contact, Country, CityTown
# from .models import VehicleFuel, Vehicle, VehicleData, VehicleWarranty, VehicleMprs, VehicleReviews, VehicleDataLoggerHist
# from .models import VehicleDemInt, VehicleEngTrns, StatesProvence, GrantedPermissions, HashAlgo, Permission, Role
# from .models import StatesProvence, GrantedPermissions, UserRoles, UserLoginData, VehicleWarranty

for model_name in dir(models):
    model = getattr(models, model_name)
    if isinstance(model, ModelBase):
        # admin.site.unregister(Block)
        admin.site.register(model)

# @admin.register(Tutorial, Employee, EmployeeTask)
# class TutorialAdmin(admin.ModelAdmin):
#     readonly_fields = ("description",)


# @admin.register(Tutorial, Employee, EmployeeTask)
# class DefaultAdmin(admin.ModelAdmin):
#     pass
#
#
# # admin.site.register(Tutorial, TutorialAdmin)
#
# class AdminEmployee(admin.ModelAdmin):
#     # the list only tells Django what to list on the admin site
#     list_display = ["emp_id", "name", "gender"]


# admin.site.register(Home, HomeAdmin)
