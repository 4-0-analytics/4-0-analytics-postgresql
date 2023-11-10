import datetime

from django.db import models
from pygments import highlight  # new
from pygments.formatters.html import HtmlFormatter  # new
from pygments.lexers import get_all_lexers, get_lexer_by_name  # new
from pygments.styles import get_all_styles
# from django.contrib.auth import get_user_model

# User = get_user_model()

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])

GENDER_CHOICES = (('M', 'Male'),
                  ('F', 'Female'),)


class AuditLog(models.Model):
    auditLogId = models.AutoField(primary_key=True, editable=False)
    actionId = models.IntegerField(blank=False)
    dateTime = models.DateTimeField(auto_now_add=True)
    tableName = models.CharField(max_length=100, default='')
    user = models.CharField(max_length=100, default='')
    createdBy = models.CharField(max_length=50, blank=False)
    createdDt = models.DateTimeField(auto_now_add=True)
    updatedBy = models.CharField(max_length=50, blank=False)
    updatedDt = models.DateTimeField(default='')

    def __str__(self):
        return self.tableName


class AuditValues(models.Model):
    auditValuesId = models.AutoField(primary_key=True, editable=False)
    auditLog = models.ForeignKey(AuditLog, on_delete=models.CASCADE, blank=False)
    fieldName = models.CharField(max_length=100, default='')
    previousValue = models.CharField(max_length=1000, default='')
    newValue = models.CharField(max_length=1000, default='')
    createdBy = models.CharField(max_length=50, blank=False)
    createdDt = models.DateTimeField(auto_now_add=True)
    updatedBy = models.CharField(max_length=50, blank=False)
    updatedDt = models.DateTimeField(default='')

    def __str__(self):
        return f"{self.auditLog} {self.fieldName}"


class DTC(models.Model):
    dtcId = models.AutoField(primary_key=True, editable=False)
    dtcDesc = models.CharField(max_length=100, default='')
    createdBy = models.CharField(max_length=50, blank=False)
    createdDt = models.DateTimeField(auto_now_add=True)
    updatedBy = models.CharField(max_length=50, blank=False)
    updatedDt = models.DateTimeField(default='')

    class Meta:
        ordering = ['dtcId']

    def __str__(self):
        return self.dtcDesc


class Vehicle(models.Model):
    vehicleId = models.CharField(primary_key=True, unique=True, max_length=20, blank=False, default='')
    vin = models.CharField(max_length=17, blank=False)
    licPlateNbr = models.CharField(max_length=10, blank=False)
    odoMeter = models.IntegerField(blank=False)
    emsExpDt = models.DateTimeField(blank=False)
    activityDt = models.DateTimeField(blank=False)
    latestActDt = models.DateTimeField(blank=False)
    createdBy = models.CharField(max_length=50, blank=False, default='')
    createdDt = models.DateTimeField(auto_now_add=True)
    updatedBy = models.CharField(max_length=50, blank=False)
    updatedDt = models.DateTimeField(default='')

    class Meta:
        ordering = ['vehicleId']

    def __str__(self):
        return self.vin


class Client(models.Model):
    clientId = models.AutoField(primary_key=True, editable=False)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, blank=False)
    clientNm = models.CharField(max_length=100, blank=False)
    clientType = models.CharField(max_length=10, default='')
    industry = models.CharField(max_length=25, default='')
    createdBy = models.CharField(max_length=50, blank=False)
    createdDt = models.DateTimeField(auto_now_add=True)
    updatedBy = models.CharField(max_length=50, blank=False)
    updatedDt = models.DateTimeField(default='')
    class Meta:
        ordering = ['clientId']

    def __str__(self):
        return self.clientNm


class AdminUser(models.Model):
    adminUserId = models.AutoField(primary_key=True, editable=False)
    fName = models.CharField(max_length=30, blank=False)
    lName = models.CharField(max_length=30, blank=False)
    jobTitle = models.CharField(max_length=50, blank=False)
    employmentStat = models.CharField(max_length=8, default='')
    createdBy = models.CharField(max_length=50, blank=False)
    createdDt = models.DateTimeField(auto_now_add=True)
    updatedBy = models.CharField(max_length=50, blank=False)
    updatedDt = models.DateTimeField(default='')

    def __str__(self):
        return f"{self.fName} {self.lName}"


class Department(models.Model):
    deptId = models.AutoField(primary_key=True, editable=False)
    # clientUser = models.OneToOneField(ClientUser,
    #                                   on_delete=models.CASCADE,
    #                                   blank=False
    #                                   )
    deptNm = models.CharField(max_length=50, blank=False)
    createdBy = models.CharField(max_length=50, blank=False)
    createdDt = models.DateTimeField(auto_now_add=True)
    updatedBy = models.CharField(max_length=50, blank=False)
    updatedDt = models.DateTimeField(default='')

    def __str__(self):
        return self.deptNm


class ClientUser(models.Model):
    clientUserId = models.AutoField(primary_key=True, editable=False)
    client = models.ForeignKey(Client, related_name='clientUsers', on_delete=models.CASCADE, blank=False)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    adminUser = models.ForeignKey(AdminUser, on_delete=models.CASCADE)
    fName = models.CharField(max_length=30, blank=False)
    lName = models.CharField(max_length=30, blank=False)
    empNbr = models.IntegerField(blank=False)
    jobTitle = models.CharField(max_length=50, blank=False)
    employmentStat = models.CharField(max_length=8, default='')
    createdBy = models.CharField(max_length=50, blank=False)
    createdDt = models.DateTimeField(auto_now_add=True)
    updatedBy = models.CharField(max_length=50, blank=False)
    updatedDt = models.DateTimeField(default='')
    def __str__(self):
        return f"{self.fName} {self.lName}"


class Role(models.Model):
    roleId = models.AutoField(primary_key=True, editable=False)
    # grantedpermid = models.CharField(max_length=50, blank=False)
    roleDesc = models.CharField(max_length=50, blank=False)
    permissions = models.ManyToManyField("Permission", through='GrantedPermissions')
    createdBy = models.CharField(max_length=50, blank=False)
    createdDt = models.DateTimeField(auto_now_add=True)
    updatedBy = models.CharField(max_length=50, blank=False)
    updatedDt = models.DateTimeField(default='')

    def __str__(self):
        return self.roleDesc


class Permission(models.Model):
    permissionId = models.AutoField(primary_key=True, editable=False)
    # grantedpermid = models.CharField(max_length=50, blank=False)
    permissionDesc = models.CharField(max_length=50, blank=False)
    createdBy = models.CharField(max_length=50, blank=False)
    createdDt = models.DateTimeField(auto_now_add=True)
    updatedBy = models.CharField(max_length=50, blank=False)
    updatedDt = models.DateTimeField(default='')

    def __str__(self):
        return self.permissionDesc


class GrantedPermissions(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    createdBy = models.CharField(max_length=50, blank=False)
    createdDt = models.DateTimeField(auto_now_add=True)
    updatedBy = models.CharField(max_length=50, blank=False)
    updatedDt = models.DateTimeField(default='')

    def __str__(self):
        return "{}_{}".format(self.role.__str__(), self.permission.__str__())


class UserRoles(models.Model):
    userRolesID = models.AutoField(primary_key=True, editable=False)
    clientUser = models.ForeignKey(ClientUser, related_name='roles', on_delete=models.CASCADE, blank=False)
    role = models.ForeignKey(Role, related_name='clientUsers', on_delete=models.CASCADE, blank=False)
    createdBy = models.CharField(max_length=50, blank=False)
    createdDt = models.DateTimeField(auto_now_add=True)
    updatedBy = models.CharField(max_length=50, blank=False)
    updatedDt = models.DateTimeField(default='')

    def __str__(self):
        return "{}_{}".format(self.role.__str__(), self.clientUser.__str__())


class UserLoginData(models.Model):
    userLoginDataId = models.AutoField(primary_key=True, editable=False)
    clientUser = models.OneToOneField(ClientUser,
                                      on_delete=models.CASCADE,
                                      blank=False
                                      )
    loginName = models.CharField(max_length=30, blank=False)
    emailName = models.CharField(max_length=50, default='')
    passwordHash = models.CharField(max_length=250, blank=False)
    passwordSalt = models.CharField(max_length=100, blank=False)
    tokenGenTime = models.DateTimeField(auto_now_add=True)
    confirmationToken = models.CharField(max_length=100, default='')
    paswordRecovToken = models.CharField(max_length=100, default='')
    RecoveryTokenTime = models.DateTimeField(auto_now_add=True)
    createdBy = models.CharField(max_length=50, blank=False)
    createdDt = models.DateTimeField(auto_now_add=True)
    updatedBy = models.CharField(max_length=50, blank=False)
    updatedDt = models.DateTimeField(default='')

    def __str__(self):
        return "{}_{}".format(self.clientUser.__str__(), self.loginName.__str__())


class HashAlgo(models.Model):
    hashAlgoID = models.AutoField(primary_key=True, editable=False)

    userLoginData = models.OneToOneField(UserLoginData,
                                         on_delete=models.CASCADE
                                         )
    algorithmName = models.CharField(max_length=10, blank=False)
    createdBy = models.CharField(max_length=50, blank=False)
    createdDt = models.DateTimeField(auto_now_add=True)
    updatedBy = models.CharField(max_length=50, blank=False)
    updatedDt = models.DateTimeField(default='')

    def __str__(self):
        return "{}_{}".format(self.userLoginData.__str__(), self.algorithmName.__str__())


class EmailValidStatus(models.Model):
    emailValidStatusId = models.AutoField(primary_key=True, editable=False)
    userLoginData = models.OneToOneField(UserLoginData,
                                         on_delete=models.CASCADE
                                         # primary_key=True
                                         )
    statusDescription = models.CharField(max_length=30, blank=False)
    createdBy = models.CharField(max_length=50, blank=False)
    createdDt = models.DateTimeField(auto_now_add=True)
    updatedBy = models.CharField(max_length=50, blank=False)
    updatedDt = models.DateTimeField(default='')

    def __str__(self):
        return "{}_{}".format(self.userLoginData.__str__(), self.statusDescription.__str__())


class ContactAddress(models.Model):
    contactAddressId = models.AutoField(primary_key=True, editable=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, blank=False)
    country = models.CharField(max_length=100, default='')
    stateProvince = models.CharField(max_length=100, default='')
    address1 = models.CharField(max_length=120, blank=False)
    address2 = models.CharField(max_length=120, default='')
    address3 = models.CharField(max_length=120, default='')
    emailAddr = models.CharField(max_length=100, blank=False)
    cityTownNm = models.CharField(max_length=100, blank=False)
    countyFips = models.IntegerField()
    countyNm = models.CharField(max_length=100, blank=False)
    lat = models.DecimalField(max_digits=6, decimal_places=4)
    lng = models.DecimalField(max_digits=7, decimal_places=4)
    population = models.IntegerField()
    density = models.DecimalField(max_digits=1000, decimal_places=1)
    source = models.CharField(max_length=10, blank=False)
    incorporated = models.CharField(max_length=5, blank=False)
    timeZone = models.CharField(max_length=25, blank=False)
    ranking = models.IntegerField()
    zipCd = models.IntegerField(blank=False)
    createdBy = models.CharField(max_length=50, blank=False)
    createdDt = models.DateTimeField(auto_now_add=True)
    updatedBy = models.CharField(max_length=50, blank=False)
    updatedDt = models.DateTimeField(default='')

    def __str__(self):
        return self.address1


# class Country(models.Model):
#     countryId = models.AutoField(primary_key=True, editable=False)
#     contact = models.OneToOneField(Contact, on_delete=models.CASCADE, blank=False)
#     name = models.CharField(max_length=100, blank=False)
#     createdBy = models.CharField(max_length=50, blank=False)
#     createdDt = models.DateTimeField(auto_now_add=True)
#     createdBy = models.CharField(max_length=50, blank=False)
#     createdDt = models.DateTimeField(default='')
#
#     def __str__(self):
#         return self.name


# class StatesProvence(models.Model):
#     stateProvId = models.AutoField(primary_key=True, editable=False)
#     country = models.OneToOneField(Country, on_delete=models.CASCADE, blank=False)
#     stateName = models.CharField(max_length=100, blank=False)
#     createdBy = models.CharField(max_length=50, blank=False)
#     createdDt = models.DateTimeField(auto_now_add=True)
#     createdBy = models.CharField(max_length=50, blank=False)
#     createdDt = models.DateTimeField(default='')
#
#     def __str__(self):
#         return self.stateName


# class CityTown(models.Model):
#     cityTownId = models.AutoField(primary_key=True, editable=False)
#     statesProvence = models.OneToOneField(StatesProvence, on_delete=models.CASCADE, blank=False)
#     cityTownNm = models.CharField(max_length=100, blank=False)
#     countyFips = models.IntegerField()
#     countyNm = models.CharField(max_length=100, blank=False)
#     lat = models.DecimalField(max_digits=6, decimal_places=4)
#     lng = models.DecimalField(max_digits=7, decimal_places=4)
#     population = models.IntegerField()
#     density = models.DecimalField(max_digits=1000, decimal_places=1)
#     source = models.CharField(max_length=10, blank=False)
#     incorporated = models.CharField(max_length=5, blank=False)
#     timeZone = models.CharField(max_length=25, blank=False)
#     ranking = models.IntegerField()
#     zipCd = models.IntegerField(blank=False)
#     createdBy = models.CharField(max_length=50, blank=False)
#     createdDt = models.DateTimeField(auto_now_add=True)
#     createdBy = models.CharField(max_length=50, blank=False)
#     createdDt = models.DateTimeField(default='')
#
#     def __str__(self):
#         return self.cityTownNm


class DataLogger(models.Model):
    dataLoggerId = models.AutoField(primary_key=True, editable=False)
    dataLoggerNbr = models.IntegerField(blank=False)
    productCode = models.CharField(max_length=20, default='')
    imei = models.IntegerField()
    macId = models.IntegerField()
    simNumber = models.IntegerField(blank=False)
    firmwareVersion = models.IntegerField(blank=False)
    configVersion = models.CharField(max_length=16, default='')
    status = models.CharField(max_length=8, default='')
    createdBy = models.CharField(max_length=50, blank=False)
    createdDt = models.DateTimeField(auto_now_add=True)
    updatedBy = models.CharField(max_length=50, blank=False)
    updatedDt = models.DateTimeField(default='')

    def __str__(self):
        return self.dataLoggerNbr


class VehicleDataLoggerHist(models.Model):
    datalogger = models.ForeignKey(DataLogger,
                                   on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle,
                                on_delete=models.CASCADE)
    status = models.CharField(max_length=3, blank=False)
    dataLogStartDt = models.DateTimeField(blank=False)
    dataLogEndDt = models.DateTimeField(blank=False)
    odomStart = models.IntegerField(blank=False)
    odomEnd = models.IntegerField(blank=False)
    createdBy = models.CharField(max_length=50, blank=False)
    createdDt = models.DateTimeField(auto_now_add=True)
    updatedBy = models.CharField(max_length=50, blank=False)
    updatedDt = models.DateTimeField(default='')


class VehicleData(models.Model):
    vehicleDataId = models.AutoField(primary_key=True, editable=False)
    vehicle = models.ForeignKey(Vehicle,
                                on_delete=models.CASCADE)
    vehicleNbr = models.IntegerField(blank=False)
    make = models.CharField(max_length=30, blank=False)
    model = models.CharField(max_length=10, default='')
    year = models.IntegerField(blank=False)
    trim = models.CharField(max_length=30, blank=False)
    trimDesc = models.CharField(max_length=100, default='')
    createdBy = models.CharField(max_length=50, blank=False)
    createdDt = models.DateTimeField(auto_now_add=True)
    updatedBy = models.CharField(max_length=50, blank=False)
    updatedDt = models.DateTimeField(default='')

    def __str__(self):
        return self.vehiclenbr


class VehicleMprs(models.Model):
    vehicleMprsId = models.AutoField(primary_key=True, editable=False)
    vehicleData = models.OneToOneField(VehicleData, on_delete=models.CASCADE, blank=False)
    mprs = models.DecimalField(max_digits=10, decimal_places=2)
    colorExt = models.CharField(max_length=30, default='')
    colorInt = models.IntegerField(blank=False)
    createdBy = models.CharField(max_length=50, blank=False)
    createdDt = models.DateTimeField(auto_now_add=True)
    updatedBy = models.CharField(max_length=50, blank=False)
    updatedDt = models.DateTimeField(default='')

    def __str__(self):
        return self.mprs


class VehicleReviews(models.Model):
    vehicleReviewId = models.AutoField(primary_key=True, editable=False)
    vehicleData = models.OneToOneField(VehicleData, on_delete=models.CASCADE, blank=False)
    source = models.CharField(max_length=100, default='')
    sourceUrl = models.CharField(max_length=100, default='')
    imageUrl = models.CharField(max_length=100, default='')
    nhtsaoOverAllRating = models.CharField(max_length=100, default='')
    pros = models.CharField(max_length=500, default='')
    cons = models.CharField(max_length=500, default='')
    createdBy = models.CharField(max_length=50, blank=False)
    createdDt = models.DateTimeField(auto_now_add=True)
    updatedBy = models.CharField(max_length=50, blank=False)
    updatedDt = models.DateTimeField(default='')

    def __str__(self):
        return self.source


class VehicleFuel(models.Model):
    vehicleFuelId = models.AutoField(primary_key=True, editable=False)
    vehicleData = models.OneToOneField(VehicleData, on_delete=models.CASCADE, blank=False)
    engineType = models.CharField(max_length=30, blank=False)
    fuelType = models.CharField(max_length=30, blank=False)
    fuelTankCapac = models.DecimalField(max_digits=2, decimal_places=1, blank=False)
    combineDmpg = models.CharField(max_length=15, blank=False)
    cityHigwayMpg = models.CharField(max_length=15)
    cityHigwayRng = models.CharField(max_length=15)
    epaCombineDmpg = models.CharField(max_length=15)
    cityMpg = models.CharField(max_length=15)
    highwayMpg = models.CharField(max_length=15)
    kwh100Mi = models.DecimalField(max_digits=4, decimal_places=2)
    timeToChrgBatt = models.DecimalField(max_digits=4, decimal_places=2)
    electricIrng = models.DecimalField(max_digits=4, decimal_places=2)
    createdBy = models.CharField(max_length=50, blank=False)
    createdDt = models.DateTimeField(auto_now_add=True)
    updatedBy = models.CharField(max_length=50, blank=False)
    updatedDt = models.DateTimeField(default='')

    def __str__(self):
        return f"{self.engineType} {self.fueType}"


class VehicleDemInt(models.Model):
    vehicleDemIntId = models.AutoField(primary_key=True, editable=False)
    vehicleData = models.OneToOneField(VehicleData, on_delete=models.CASCADE, blank=False)
    frontHeadRoom = models.DecimalField(max_digits=5, decimal_places=2)
    frontHipRoom = models.DecimalField(max_digits=5, decimal_places=2)
    frontLegRoom = models.DecimalField(max_digits=5, decimal_places=2)
    frontShoulderRm = models.DecimalField(max_digits=5, decimal_places=2)
    trimDesc = models.CharField(max_length=100, default='')
    rearHeadRoom = models.DecimalField(max_digits=5, decimal_places=2)
    rearHipRoom = models.DecimalField(max_digits=5, decimal_places=2)
    rearLegRoom = models.DecimalField(max_digits=5, decimal_places=2)
    rearShoulderRm = models.DecimalField(max_digits=5, decimal_places=2)
    createdBy = models.CharField(max_length=50, blank=False)
    createdDt = models.DateTimeField(auto_now_add=True)
    updatedBy = models.CharField(max_length=50, blank=False)
    updatedDt = models.DateTimeField(default='')

    def __str__(self):
        return f"{self.vehicleDemIntId} {self.frontHeadRoom}"


class VehicleWarranty(models.Model):
    vehicleWarrId = models.AutoField(primary_key=True, editable=False)
    vehicleData = models.OneToOneField(VehicleData, on_delete=models.CASCADE, blank=False)
    manufacture = models.IntegerField()
    basic = models.IntegerField()
    driveTrain = models.IntegerField()
    roadSide = models.IntegerField()
    rust = models.IntegerField()
    hybriDcompnt = models.IntegerField()
    evBatt = models.IntegerField()
    createdBy = models.CharField(max_length=50, blank=False)
    createdDt = models.DateTimeField(auto_now_add=True)
    updatedBy = models.CharField(max_length=50, blank=False)
    updatedDt = models.DateTimeField(default='')

    def __str__(self):
        return f"{self.vehicleWarrId} {self.manufacture}"


class VehicleEngTrns(models.Model):
    vehicleEngRrnsId = models.AutoField(primary_key=True, editable=False)
    vehicleData = models.OneToOneField(VehicleData, on_delete=models.CASCADE, blank=False)
    torQue = models.IntegerField()
    valves = models.IntegerField()
    valveTiming = models.CharField(max_length=30, blank=False)
    camType = models.CharField(max_length=30, blank=False)
    driveType = models.CharField(max_length=50, default='')
    trans = models.CharField(max_length=50, default='')
    createdBy = models.CharField(max_length=50, blank=False)
    createdDt = models.DateTimeField(auto_now_add=True)
    updatedBy = models.CharField(max_length=50, blank=False)
    updatedDt = models.DateTimeField(default='')

    def __str__(self):
        return f"{self.vehicleEngRrnsId} {self.torQue} {self.valves}"


class VehicleDimExt(models.Model):
    vehicleDimExtId = models.AutoField(primary_key=True, editable=False)
    vehicleData = models.OneToOneField(VehicleData, on_delete=models.CASCADE, blank=False)
    bodyType = models.CharField(max_length=30, blank=False)
    doors = models.IntegerField(blank=False)
    seats = models.IntegerField()
    length = models.DecimalField(max_digits=4, decimal_places=2, blank=False)
    height = models.DecimalField(max_digits=5, decimal_places=1, blank=False)
    wheelbase = models.DecimalField(max_digits=4, decimal_places=2)
    frontTrack = models.DecimalField(max_digits=4, decimal_places=2)
    rearTrack = models.DecimalField(max_digits=4, decimal_places=2, blank=False)
    groundClernc = models.DecimalField(max_digits=4, decimal_places=2, blank=False)
    angleOfApproach = models.DecimalField(max_digits=4, decimal_places=2)
    width = models.DecimalField(max_digits=4, decimal_places=2)
    angleOfDeparture = models.DecimalField(max_digits=4, decimal_places=2)
    turningCircle = models.DecimalField(max_digits=4, decimal_places=2)
    dragCoeff = models.DecimalField(max_digits=4, decimal_places=2)
    epaInteriorVolume = models.DecimalField(max_digits=4, decimal_places=2)
    cargoCapacity = models.DecimalField(max_digits=4, decimal_places=2)
    maxcargoCapac = models.DecimalField(max_digits=4, decimal_places=2)
    curbWeight = models.DecimalField(max_digits=6, decimal_places=2)
    grossWeight = models.IntegerField()
    maxPayld = models.IntegerField()
    maxTowcapac = models.IntegerField()
    createdBy = models.CharField(max_length=50, blank=False)
    createdDt = models.DateTimeField(auto_now_add=True)
    updatedBy = models.CharField(max_length=50, blank=False)
    updatedDt = models.DateTimeField(default='')

    def __str__(self):
        return f"{self.vehicleDimExtId} {self.bodyType}"


class EmailValidationStatus(models.Model):
    emailValidationId = models.AutoField(primary_key=True, editable=False)
    userLoginData = models.OneToOneField(UserLoginData, on_delete=models.CASCADE, blank=False)
    statusDescription = models.CharField(max_length=30, default='')
    createdBy = models.CharField(max_length=50, blank=False)
    createdDt = models.DateTimeField(auto_now_add=True)
    updatedBy = models.CharField(max_length=50, blank=False)
    updatedDt = models.DateTimeField(default='')

    def __str__(self):
        return f"{self.emailValidationId} {self.statusDescription}"


# class HashAlgo(models.Model):
#     hashAlgoId = models.AutoField(primary_key=True, editable=False)
#     userLoginData = models.OneToOneField(UserLoginData, on_delete=models.CASCADE, blank=False)
#     algorithmName = models.CharField(max_length=10, default='')
#     createdBy = models.CharField(max_length=50, blank=False)
#     createdDt = models.DateTimeField(auto_now_add=True)
#     createdBy = models.CharField(max_length=50, blank=False)
#     createdDt = models.DateTimeField(default='')
#
#     def __str__(self):
#         return f"{self.hashAlgoId} {self.algorithmName}"

# class Tutorial(models.Model):
#     title = models.CharField(max_length=70, blank=False, default='')
#     description = models.CharField(max_length=200, blank=False, default='')
#     published = models.BooleanField(default=False)
#
#     class Meta:
#         managed = False
#
#     # def save(self, *args, **kwargs):  # new
#     #     """
#     #         Use the `pygments` library to create a highlighted HTML
#     #         representation of the code snippet.
#     #         """
#     #     lexer = get_lexer_by_name(self.language)
#     #     linenos = "table" if self.linenos else False
#     #     options = {"title": self.title} if self.title else {}
#     #     formatter = HtmlFormatter(
#     #         style=self.style, linenos=linenos, full=True, **options
#     #     )
#     #     self.highlighted = highlight(self.code, lexer, formatter)
#     #     super(Tutorial, self).save(*args, **kwargs)
#
#     def save(self, *args, **kwargs):
#         # do something with Invoice here
#         return super().save(*args, **kwargs)
#
#     def __str__(self):
#         return self.title
#
#
# class Employee(models.Model):
#     emp_id = models.IntegerField()
#     name = models.CharField(max_length=150)
#     gender = models.CharField(max_length=1,
#                               choices=GENDER_CHOICES,
#                               default='M')
#     designation = models.CharField(max_length=150)
#
#     class Meta:
#         ordering = ['emp_id']
#
#     def __str__(self):
#         return self.name
#
#
# class EmployeeTask(models.Model):
#     task_name = models.CharField(max_length=150)
#     employee = models.ForeignKey(Employee,
#                                  related_name='tasks',
#                                  on_delete=models.CASCADE)
#     task_desc = models.CharField(max_length=350)
#     created_date = models.DateTimeField(auto_now_add=True)
#     deadline = models.DateTimeField()
#
#     class Meta:
#         ordering = ['task_name']
#
#     def __str__(self):
#         return self.task_name
