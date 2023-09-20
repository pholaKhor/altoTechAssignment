from django.test import TestCase
from rest_framework import status
from users.models import CustomUser, User, UserPermission, UserType
from django.contrib.auth import authenticate 
from rest_framework_simplejwt.tokens import RefreshToken 
from users.permission import get_permission_list_string
from django.core.management import call_command
from .mock_utils import create_work_order, get_db, update_work_order, get_work_order
from unittest import mock

def initialTest():
    # create assign user    
    user = User.objects.create_user(username="assignUser",password="password")
    user.save()
    CustomUser.objects.create(user=user, user_type = 2).save() 


def authenUser(username, password, user_type):
    user = User.objects.create_user(username=username,password=password)
    user.save()
    customUser = CustomUser.objects.create(user=user, user_type=user_type)
    customUser.save()
    user = authenticate(username=username, password=password) 
    permissionList = UserPermission.objects.filter(user_type=customUser.user_type)
    permission_list_string = get_permission_list_string(permissionList)
    refresh = RefreshToken.for_user(user)
    refresh.payload["permissions"] = permission_list_string
    return str(refresh.access_token)

# Create your tests here.

@mock.patch('work_order.views.create_work_order', side_effect=create_work_order)
@mock.patch('work_order.views.get_db', side_effect=get_db)
@mock.patch('work_order.views.update_work_order', side_effect=update_work_order)
@mock.patch('work_order.views.get_work_order', side_effect=get_work_order)
class WorkOrderTestCase(TestCase):    
    fixtures = ['user_permission_1.json']          

    # create work order test case
    def test_create_cleaning_type_success(self, *mock_save):        
        initialTest()
        access_token = authenUser("MaidSupervisor", "password", int(UserType.MAID_SUPERVISOR))
        header = {"HTTP_AUTHORIZATION": "Bearer " + access_token}
        data = {
            "room": 999,
            "type": "CLEANING"
        }
        response  = self.client.post('/work-orders/',data, **header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    
    def test_create_cleaning_type_by_supervisor_fail(self, *mock_save):
        initialTest()
        access_token = authenUser("MaidSupervisor", "password", int(UserType.SUPERVISOR))
        header = {"HTTP_AUTHORIZATION": "Bearer " + access_token}
        data = {
            "room": 999,
            "type": "CLEANING"
        }
        response  = self.client.post('/work-orders/',data, **header)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    
    def test_create_cleaning_type_by_guest_fail(self, *mock_save):
        initialTest()
        access_token = authenUser("MaidSupervisor", "password", int(UserType.GUEST))
        header = {"HTTP_AUTHORIZATION": "Bearer " + access_token}
        data = {
            "room": 999,
            "type": "CLEANING"
        }
        response  = self.client.post('/work-orders/',data, **header)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
 

    def test_create_maid_request_type_success(self, *mock_save):
        initialTest() 
        access_token = authenUser("MaidSupervisor", "password", int(UserType.MAID_SUPERVISOR))
        header = {"HTTP_AUTHORIZATION": "Bearer " + access_token}
        data = {
            "room": 999,
            "type": "MAID_REQUEST",
            "Description": "Optional description field."
        }
        response  = self.client.post('/work-orders/',data, **header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    
    def test_create_maid_request_type_by_supervisor_fail(self, *mock_save):
        initialTest() 
        access_token = authenUser("MaidSupervisor", "password", int(UserType.SUPERVISOR))
        header = {"HTTP_AUTHORIZATION": "Bearer " + access_token}
        data = {
            "room": 999,
            "type": "MAID_REQUEST",
            "Description": "Optional description field."
        }
        response  = self.client.post('/work-orders/',data, **header)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    
    def test_create_maid_request_type_by_guest_fail(self, *mock_save):
        initialTest() 
        access_token = authenUser("MaidSupervisor", "password", int(UserType.GUEST))
        header = {"HTTP_AUTHORIZATION": "Bearer " + access_token}
        data = {
            "room": 999,
            "type": "MAID_REQUEST",
            "Description": "Optional description field."
        }
        response  = self.client.post('/work-orders/',data, **header)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


     
    def test_create_technician_request_by_guest_type_success(self, *mock_save):
        initialTest()
        access_token = authenUser("Guest", "password", int(UserType.GUEST))
        header = {"HTTP_AUTHORIZATION": "Bearer " + access_token}
        data = {
            "room": 999,
            "type": "TECHNICIAN_REQUEST",
            "defects": "ELECTRICITY,AIR_CON"
        }
        response  = self.client.post('/work-orders/',data, **header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
 

    def test_create_technician_request_by_supervisor_type_success(self, *mock_save):
        initialTest()
        access_token = authenUser("Guest", "password", int(UserType.SUPERVISOR))
        header = {"HTTP_AUTHORIZATION": "Bearer " + access_token}
        data = {
            "room": 999,
            "type": "TECHNICIAN_REQUEST",
            "defects": "ELECTRICITY,AIR_CON"
        }
        response  = self.client.post('/work-orders/',data, **header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_technician_request_by_maid_supervisor_type_fail(self, *mock_save):
        initialTest()
        access_token = authenUser("Guest", "password", int(UserType.MAID_SUPERVISOR))
        header = {"HTTP_AUTHORIZATION": "Bearer " + access_token}
        data = {
            "room": 999,
            "type": "TECHNICIAN_REQUEST",
            "defects": "ELECTRICITY,AIR_CON"
        }
        response  = self.client.post('/work-orders/',data, **header)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

     
    def test_create_amenity_request_by_guest_success(self, *mock_save):
        initialTest()
        access_token = authenUser("Guest", "password", int(UserType.GUEST))
        header = {"HTTP_AUTHORIZATION": "Bearer " + access_token}
        data = {
            "room": 999,
            "type": "AMENITY_REQUEST",
            "amenityType,": "paper",
            "quantity,": 1
        }
        response  = self.client.post('/work-orders/',data, **header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    
    def test_create_amenity_request_by_maid_supervisor_fail(self, *mock_save):
        initialTest()
        access_token = authenUser("Guest", "password", int(UserType.MAID_SUPERVISOR))
        header = {"HTTP_AUTHORIZATION": "Bearer " + access_token}
        data = {
            "room": 999,
            "type": "AMENITY_REQUEST",
            "amenityType,": "paper",
            "quantity,": 1
        }
        response  = self.client.post('/work-orders/',data, **header)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        

    def test_create_amenity_request_by_supervisor_fail(self, *mock_save):
        initialTest()
        access_token = authenUser("Guest", "password", int(UserType.SUPERVISOR))
        header = {"HTTP_AUTHORIZATION": "Bearer " + access_token}
        data = {
            "room": 999,
            "type": "AMENITY_REQUEST",
            "amenityType,": "paper",
            "quantity,": 1
        }
        response  = self.client.post('/work-orders/',data, **header)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    
    # update work order test case    
    def test_update_cleaning_type_success(self, *mock_save):
        initialTest()
        access_token = authenUser("MaidSupervisor", "password", int(UserType.MAID_SUPERVISOR))
        header = {"HTTP_AUTHORIZATION": "Bearer " + access_token}
        data = {
            "status": "ASSIGNED",
            "assignedTo": "assignUser"
        }
        response  = self.client.patch('/work-orders/cleaningCreate1/',data ,content_type='application/json' , **header)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
 

    def test_update_cleaning_type_fail_no_assign_user(self, *mock_save):
        initialTest()
        access_token = authenUser("MaidSupervisor", "password", int(UserType.MAID_SUPERVISOR))
        header = {"HTTP_AUTHORIZATION": "Bearer " + access_token}
        data = {
            "status": "ASSIGNED"
        }
        response  = self.client.patch('/work-orders/cleaningCreate1/',data ,content_type='application/json' , **header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_update_assigned_type_success(self, *mock_save):
        initialTest()
        access_token = authenUser("MaidSupervisor", "password", int(UserType.MAID_SUPERVISOR))
        header = {"HTTP_AUTHORIZATION": "Bearer " + access_token}
        data = {
            "status": "IN_PROGRESS"
        }
        response  = self.client.patch('/work-orders/cleaningAssigned1/',data ,content_type='application/json' , **header)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT) 

    def test_update_inprogress_type_success(self, *mock_save):
        initialTest()
        access_token = authenUser("MaidSupervisor", "password", int(UserType.MAID_SUPERVISOR))
        header = {"HTTP_AUTHORIZATION": "Bearer " + access_token}
        data = {
            "status": "DONE"
        }
        response  = self.client.patch('/work-orders/cleaningInprogress1/',data ,content_type='application/json' , **header)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_to_cancel_type_success(self, *mock_save):
        initialTest()
        access_token = authenUser("MaidSupervisor", "password", int(UserType.MAID_SUPERVISOR))
        header = {"HTTP_AUTHORIZATION": "Bearer " + access_token}
        data = {
            "status": "CANCEL"
        }
        response  = self.client.patch('/work-orders/cleaningInprogress1/',data ,content_type='application/json' , **header)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    