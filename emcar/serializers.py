from rest_framework import serializers
from django.contrib.auth.models import User, Group
from emcar.models import *


class AuditValuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditValues
        # fields = '__all__'
        fields = ['auditValuesId', 'fieldName', 'previousValue', 'newValue']


class AuditLogSerializer(serializers.ModelSerializer):
    auditValues = AuditValuesSerializer(many=True, read_only=True)

    class Meta:
        model = AuditLog
        fields = ['auditLogId', 'actionId', 'dateTime', 'tableName', 'user']


class ClientUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientUser
        fields = ['clientUserId', 'department', 'adminUser', 'fName', 'lName', 'empNbr', 'jobTitle', 'employmentStat']


class ClientSerializer(serializers.ModelSerializer):
    clientUser = ClientUserSerializer(many=True, read_only=True)

    class Meta:
        model = AuditValues
        fields = '__all__'


class VehicleSerializer(serializers.ModelSerializer):
    clients = ClientSerializer(many=True, read_only=True)

    def get_client(self, obj):
        return ClientSerializer(obj.client_set.all(), many=True).data

    class Meta:
        model = Vehicle
        fields = ['vehicleId', 'vin', 'licPlateNbr', 'odoMeter', 'emsExpDt', 'activityDt', 'latestActDt']


class DTCSerializer(serializers.ModelSerializer):
    class Meta:
        model = DTC
        fields = ('dtcId', 'dtcDesc')


class DepartmentSerializer(serializers.ModelSerializer):
    clientUser = ClientUserSerializer(required=True)

    class Meta:
        model = Department
        fields = ('deptId', 'deptNm', 'clientUser')


class PermissionSerializer(serializers.ModelSerializer):
    # Role_list = RoleSerializer(many=True, read_only=True)

    class Meta:
        model = Department
        fields = ('permissionId', 'permissionDesc')


class GrantedPermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrantedPermissions

        fields = 'permission_id'


class RoleDisplaySerializer(serializers.ModelSerializer):
    '''To display Role with related permissions '''

    permissions = serializers.SerializerMethodField()

    class Meta:
        model = Role

        fields = ('roleId', 'roleDesc', 'permissions')

    def get_materials(self, role_instance):
        query_datas = GrantedPermissions.objects.filter(role=role_instance)

        return [GrantedPermissionsSerializer(permission).data for permission in query_datas]


class RoleSerializer(serializers.ModelSerializer):
    permission_id = serializers.PrimaryKeyRelatedField(queryset=Permission.objects.all(), many=True)

    class Meta:
        model = Department
        fields = ('roleId', 'roleDesc', 'permission_id')


class RoleCreateSerializer(serializers.ModelSerializer):
    '''To create a role with existed permission  '''

    permissions = GrantedPermissionsSerializer(many=True)

    class Meta:
        model = Role

        fields = ('roleId', 'roleDesc', 'permissions')

    def create(self, validated_data):
        permissions_data = validated_data.pop('permissions')

        role = Role.objects.create(**validated_data)

        for permission_data in permissions_data:
            GrantedPermissions.objects.create(
                role=role,
                permission=permission_data.get('permission')
            )

        return role


# class GrantedPermissionsSerializer(serializers.ModelSerializer):
#     permission = PermissionSerializer()
#
#     roles = RoleSerializer(source='permission_set', many=True)
#
#     class Meta:
#         model = GrantedPermissions
#         fields = ('permission', 'roles')
#         depth = 1

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


# class TutorialSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Tutorial
#         fields = ('id',
#                   'title',
#                   'description',
#                   'published')
#
#
# class EmployeeSerializer(serializers.ModelSerializer):
#     # PrimaryKeyRelatedField
#     tasks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
#
#     # tasks = serializers.StringRelatedField(many=True)
#     class Meta:
#         model = Employee
#         fields = (
#             'pk',
#             'emp_id',
#             'name',
#             'gender',
#             'designation',
#             'tasks')
#
#
# class EmployeeTaskSerializer(serializers.ModelSerializer):
#     # PrimaryKeyRelatedField
#     employee = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all(),
#                                                   many=False)
#
#     # # SlugRelatedField
#     # employee = serializers.SlugRelatedField(
#     #     queryset=Employee.objects.all(),
#     #     slug_field='name')
#
#     class Meta:
#         model = EmployeeTask
#         fields = (
#             'pk',
#             'task_name',
#             'employee',
#             'task_desc',
#             'created_date',
#             'deadline')
#         # fields = '__all__'
#
#
class YourSerializer(serializers.Serializer):
    """Your data serializer, define your fields here."""
    comments = serializers.IntegerField()
    likes = serializers.IntegerField()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    trips = serializers.HyperlinkedRelatedField(
        many=True, view_name="trip-detail", read_only=True
    )

    class Meta:
        model = User
        fields = ("url", "id", "username", "trips")
