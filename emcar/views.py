from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, Group, auth  # new
from django.http.response import HttpResponse, JsonResponse
# from rest_framework.parsers import JSONParser
from rest_framework import status, views, generics, permissions, renderers

from emcar.models import Permission, GrantedPermissions, Role, Vehicle, Client
from emcar.serializers import RoleSerializer, PermissionSerializer, RoleDisplaySerializer, GrantedPermissionsSerializer, \
    UserSerializer, YourSerializer, GroupSerializer, VehicleSerializer, ClientSerializer
# from emcar.models import Tutorial, Employee, EmployeeTask
# from emcar.serializers import TutorialSerializer, YourSerializer, UserSerializer, EmployeeSerializer, \
#     EmployeeTaskSerializer  # new
from rest_framework.decorators import api_view

from django.views.decorators.csrf import csrf_exempt

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view  # new
from rest_framework.response import Response  # new
from rest_framework.reverse import reverse  # new


@api_view(['GET', 'POST', 'DELETE'])
def group_list(request):
    if request.method == 'GET':
        groups = Group.objects.all()

        name = request.GET.get('name', None)
        if name is not None:
            groups = groups.filter(name__contains=name)

        groupss_serializer = GroupSerializer(groups, many=True)
        return JsonResponse(groupss_serializer.data, safe=False)
        # 'safe=False' for objects serialization

    elif request.method == 'POST':
        group_data = JSONParser().parse(request)
        group_serializer = GroupSerializer(data=group_data)
        if group_serializer.is_valid():
            group_serializer.save()
            return JsonResponse(group_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(group_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET', 'PUT', 'DELETE'])
# def tutorial_detail(request, pk):
#     # find tutorial by pk (id)
#     try:
#         tutorial = Tutorial.objects.get(pk=pk)
#         if request.method == 'GET':
#             tutorial_serializer = TutorialSerializer(tutorial)
#             return JsonResponse(tutorial_serializer.data)
#         elif request.method == 'PUT':
#             tutorial_data = JSONParser().parse(request)
#             tutorial_serializer = TutorialSerializer(tutorial, data=tutorial_data)
#             if tutorial_serializer.is_valid():
#                 tutorial_serializer.save()
#                 return JsonResponse(tutorial_serializer.data)
#             return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         elif request.method == 'DELETE':
#             tutorial.delete()
#             return JsonResponse({'message': 'Tutorial was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
#     except Tutorial.DoesNotExist:
#         return JsonResponse({'message': 'The tutorial does not exist'}, status=status.HTTP_404_NOT_FOUND)
#
#         # GET / PUT / DELETE tutorial

@api_view(['GET', 'PUT', 'DELETE'])
def group_detail(request, pk):
    # find tutorial by pk (id)
    try:
        group = Group.objects.get(id=pk)
        if request.method == 'GET':
            group_serializer = GroupSerializer(group)
            return JsonResponse(group_serializer.data)
        elif request.method == 'PUT':
            group_data = JSONParser().parse(request)
            group_serialize = GroupSerializer(group, data=group_data)
            if group_serialize.is_valid():
                group_serialize.save()
                return JsonResponse(group_serialize.data)
            return JsonResponse(group_serialize.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            group.delete()
            return JsonResponse({'message': 'Group was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    except Group.DoesNotExist:
        return JsonResponse({'message': 'The group does not exist'}, status=status.HTTP_404_NOT_FOUND)

        # GET / PUT / DELETE group

# @api_view(['GET'])
# def tutorial_list_published(request):
#     tutorials = Tutorial.objects.filter(published=True)
#
#     if request.method == 'GET':
#         tutorials_serializer = TutorialSerializer(tutorials, many=True)
#         return JsonResponse(tutorials_serializer.data, safe=False)

@api_view(['GET'])
def group_list_published(request):
    groups = Group.objects.filter(published=True)

    if request.method == 'GET':
        groups_serializer = GroupSerializer(groups, many=True)
        return JsonResponse(groups_serializer.data, safe=False)


@api_view(["GET"])  # new
def api_root(request, format=None):
    return Response(
        {
            "users": reverse("user-list", request=request, format=format),
            "employees": reverse("employee-list", request=request, format=format),
        }
    )


@csrf_exempt
def vehicle_list(request):
    if request.method == 'GET':
        veh = Vehicle.objects.all()
        veh_serializer = VehicleSerializer(veh, many=True)
        return JsonResponse(veh_serializer.data, safe=False)

    elif request.method == 'POST':
        veh_data = JSONParser().parse(request)
        veh_serializer = VehicleSerializer(data=veh_data)

        if veh_serializer.is_valid():
            veh_serializer.save()
            return JsonResponse(veh_serializer.data,
                                status=201)
        return JsonResponse(veh_serializer.errors,
                            status=400)


@csrf_exempt
def vehicle_detail(request, pk):
    try:
        veh = Vehicle.objects.get(vehicleId=pk)
    except Vehicle.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        veh_serializer = VehicleSerializer(veh)
        return JsonResponse(veh_serializer.data)
    elif request.method == 'DELETE':
        veh.delete()
        return HttpResponse(status=204)


@csrf_exempt
def client_list(request):
    if request.method == 'GET':
        client = Client.objects.all()
        client_serializer = ClientSerializer(client, many=True)
        return JsonResponse(client_serializer.data, safe=False)
    elif request.method == 'POST':
        client_data = JSONParser().parse(request)
        client_serializer = ClientSerializer(data=client_data)
        if client_serializer.is_valid():
            client_serializer.save()
            return JsonResponse(client_serializer.data,
                                status=201)
        return JsonResponse(client_serializer.errors,
                            status=400)


@csrf_exempt
def client_detail(request, pk):
    try:
        client = Client.objects.get(clientId=pk)
    except Client.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        client_serializer = ClientSerializer(client)
        return JsonResponse(client_serializer.data)

    elif request.method == 'DELETE':
        client.delete()
        return HttpResponse(status=204)


@api_view(["GET"])
def get_Vehicles(request):
    vehicles = Vehicle.objects.all()
    context = {
        'vehicles': vehicles
    }
    return render(request, 'index.html', context)


# @csrf_exempt
# def employee_list(request):
#     if request.method == 'GET':
#         emp = Employee.objects.all()
#         emp_serializer = EmployeeSerializer(emp, many=True)
#         return JsonResponse(emp_serializer.data, safe=False)
#
#     elif request.method == 'POST':
#         emp_data = JSONParser().parse(request)
#         emp_serializer = EmployeeSerializer(data=emp_data)
#
#         if emp_serializer.is_valid():
#             emp_serializer.save()
#             return JsonResponse(emp_serializer.data,
#                                 status=201)
#         return JsonResponse(emp_serializer.errors,
#                             status=400)
#
#
# @csrf_exempt
# def employee_detail(request, pk):
#     try:
#         emp = Employee.objects.get(pk=pk)
#     except Employee.DoesNotExist:
#         return HttpResponse(status=404)
#
#     if request.method == 'GET':
#         emp_serializer = EmployeeSerializer(emp)
#         return JsonResponse(emp_serializer.data)
#     elif request.method == 'DELETE':
#         emp.delete()
#         return HttpResponse(status=204)
#
#
# @csrf_exempt
# def employeetask_list(request):
#     if request.method == 'GET':
#         emptask = EmployeeTask.objects.all()
#         emptask_serializer = EmployeeTaskSerializer(emptask, many=True)
#         return JsonResponse(emptask_serializer.data, safe=False)
#     elif request.method == 'POST':
#         emptask_data = JSONParser().parse(request)
#         emptask_serializer = EmployeeTaskSerializer(data=emptask_data)
#         if emptask_serializer.is_valid():
#             emptask_serializer.save()
#             return JsonResponse(emptask_serializer.data,
#                                 status=201)
#         return JsonResponse(emptask_serializer.errors,
#                             status=400)
#
#
# @csrf_exempt
# def employeetask_detail(request, pk):
#     try:
#         emptask = EmployeeTask.objects.get(pk=pk)
#     except EmployeeTask.DoesNotExist:
#         return HttpResponse(status=404)
#
#     if request.method == 'GET':
#         emptask_serializer = EmployeeTaskSerializer(emptask)
#         return JsonResponse(emptask_serializer.data)
#
#     elif request.method == 'DELETE':
#         emptask.delete()
#         return HttpResponse(status=204)
#
#
# @api_view(["GET"])
# def get_Employees(request):
#     employees = Employee.objects.all()
#     context = {
#         'employees': employees
#     }
#     return render(request, 'index.html', context)


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username is already taken')
                return redirect(register)
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email is already taken')
                return redirect(register)
            else:
                user = User.objects.create_user(username=username, password=password,
                                                email=email, first_name=first_name, last_name=last_name)
                user.save()

                return redirect('login_user')
        else:
            messages.info(request, 'Both passwords are not matching')
            return redirect(register)
    else:
        return render(request, 'registration/registration.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Invalid Username or Password')
            return redirect('login_user')
    else:
        return render(request, 'login.html')


def home(request):
    return render(request, 'home.html')


def logout_user(request):
    auth.logout(request)
    return redirect('home')


class YourView(views.APIView):

    def get(self, request):
        yourdata = [{"likes": 10, "comments": 0}, {"likes": 4, "comments": 23}]
        results = YourSerializer(yourdata, many=True).data
        return JsonResponse(results, safe=False)
        # return Response(results)


class UserList(generics.ListAPIView):  # new
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):  # new
    queryset = User.objects.all()
    serializer_class = UserSerializer
