from users.token import get_permission, is_authenticate
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status
from users.models import CustomUser
from django.contrib.auth.models import User
from .db_utils import create_work_order, get_db, get_work_order, update_work_order
from .response_utils import get_missing_require_param_response, get_invalid_param_response, \
      get_not_found_response, get_no_permission_response, get_internal_error_response
from .utils import WORK_ORDER_STATUS, WORK_ORDER_TYPE, get_work_order_type_enum, get_work_order_status_enum, \
get_work_order_status_string
from datetime import datetime

# Create your views here.
class WorkOrdersAPIView(APIView):
    def post(self, request):
        user , token = is_authenticate(request)
        if user is None:
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)     
        data = request.data
        work_order = {}
        work_order["status"] = get_work_order_status_string(WORK_ORDER_STATUS.CREATED)
        # check request parameter
        assignedTo = data.get("assignedTo", None)
        if assignedTo is not None:
            # check assigned to user
            try:
                customUser = CustomUser.objects.get(username=assignedTo)
            except CustomUser.DoesNotExist:
                return Response(
                    {"detail": "Invalid assignedTo user."},
                    status=status.HTTP_400_BAD_REQUEST)
            work_order["assignedTo"] = customUser.user.username
            work_order["status"] = get_work_order_status_string(WORK_ORDER_STATUS.ASSIGNED)
        room = data.get("room", None)
        if room is None:
            return get_missing_require_param_response("room")
        work_order["room"] = room     
        workType = data.get("type", None)
        if workType is None:
            return get_missing_require_param_response("type")
        if get_work_order_type_enum(workType) not in [WORK_ORDER_TYPE.CLEANING,
                            WORK_ORDER_TYPE.MAID_REQUEST,
                            WORK_ORDER_TYPE.TECHNICIAN_REQUEST,
                            WORK_ORDER_TYPE.AMENITY_REQUEST]:
            return get_invalid_param_response("type")
        work_order["type"] = workType          
        # check permission  
        permission_list = get_permission(token)
        match get_work_order_type_enum(workType):
            case WORK_ORDER_TYPE.CLEANING:
                if "create_work_order_cleaning" not in permission_list:
                    return get_no_permission_response()
            case WORK_ORDER_TYPE.MAID_REQUEST:
                if "create_work_order_maid_req" not in permission_list:
                    return get_no_permission_response()
                
                # optional for MAID_REQUEST work order type
                if "description" in data:
                    work_order["description"] = data["description"]

            case WORK_ORDER_TYPE.AMENITY_REQUEST:
                if "create_work_order_amenity_req" not in permission_list:
                    return get_no_permission_response()
                
                # optional for AMENITY_REQUEST work order type
                if "amenityType" in data:
                    work_order["amenityType"] = data["amenityType"]
                if "quantity" in data:
                    work_order["quantity"] = data["quantity"]

            case WORK_ORDER_TYPE.TECHNICIAN_REQUEST:
                if "create_work_order_technician_req" not in permission_list:
                    return get_no_permission_response()
                
                # optional for TECHNICIAN_REQUEST work order type
                if "defects" in data:
                    defects = data["defects"].split(',')
                    for defect in defects:
                        if defect not in ["ELECTRICITY", "AIR_CON", "PLUMBING", "INTERNET"]:
                            return get_invalid_param_response("defects")
                    work_order["defects"] = data["defects"]     
        work_order["createdBy"] = user.username       
        work_order_id = create_work_order(work_order)
        return Response({"work_order_id": work_order_id}, status=status.HTTP_200_OK)
    
    
class WorkOrderAPIView(APIView):
    def patch(self, request, work_order_id):
        data = request.data
        # check request parameter        
        # check work_order_id
        db = get_db()
        if db is None:
            return get_internal_error_response()
        updated_work_order = {}
        work_order = get_work_order(db, work_order_id)
        if work_order is None: 
           return get_not_found_response("work_order_id")
        update_status = data.get("status", None)
        # check room
        if "room" in data:
            updated_work_order["room"] = data["room"] 
 
        # check work order status
        if update_status is not None:             
            update_status_enum = get_work_order_status_enum(update_status)
            if update_status_enum not in [
                WORK_ORDER_STATUS.CREATED, 
                WORK_ORDER_STATUS.ASSIGNED,
                WORK_ORDER_STATUS.IN_PROGRESS,
                WORK_ORDER_STATUS.DONE,
                WORK_ORDER_STATUS.CANCEL,
                WORK_ORDER_STATUS.CANCELLED_BY_GUEST]:
                return get_invalid_param_response("status")
            
            # check optional status for CLEANING work order type
            if work_order["type"] != "CLEANING" and  update_status_enum == WORK_ORDER_STATUS.CANCELLED_BY_GUEST:
                return get_invalid_param_response("status")
            
            match update_status_enum:
                case WORK_ORDER_STATUS.ASSIGNED:
                    assignedTo = data.get("assignedTo", None)
                    if assignedTo is not None:
                        # check assigned to user
                        try:
                            customUser = User.objects.get(username=assignedTo)
                        except User.DoesNotExist:
                            return Response(
                                {"detail": "Invalid assignedTo user."},
                                status=status.HTTP_400_BAD_REQUEST)
                        updated_work_order["assignedTo"] = customUser.username
                    else:
                        # if status type == ASSIGNED must have "assignedTo" parameter
                        return get_missing_require_param_response("assignedTo")
                case WORK_ORDER_STATUS.IN_PROGRESS:
                    updated_work_order["startedAt"] = datetime.now()
                case WORK_ORDER_STATUS.DONE:
                    updated_work_order["finishedAt"] = datetime.now() 
            updated_work_order["status"] = get_work_order_status_string(update_status_enum)

        # optional field update by work order type 
        match get_work_order_type_enum(work_order["type"]):             
            case WORK_ORDER_TYPE.MAID_REQUEST:                 
                # optional for MAID_REQUEST work order type
                if "description" in data:
                    updated_work_order["description"] = data["description"]

            case WORK_ORDER_TYPE.AMENITY_REQUEST: 
                # optional for AMENITY_REQUEST work order type 
                if "amenityType" in data:
                    updated_work_order["amenityType"] = data["amenityType"]
                if "quantity" in data:
                    updated_work_order["quantity"] = data["quantity"] 

            case WORK_ORDER_TYPE.TECHNICIAN_REQUEST:
                # optional for TECHNICIAN_REQUEST work order type
                if "defects" in data:
                    defects = data["defects"].split(',')
                    for defect in defects:
                        if defect not in ["ELECTRICITY", "AIR_CON", "PLUMBING", "INTERNET"]:
                            return get_invalid_param_response("defects")
                    updated_work_order["defects"] = data["defects"]            
        
        # update work order
        if update_work_order(work_order_id, updated_work_order):
            return Response({},
                    status=status.HTTP_204_NO_CONTENT)
        else:
            return get_internal_error_response()
        