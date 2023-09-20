from .models import PermissionType

def get_permission_list_string(permission_list):
    result_list = []
    for permission in permission_list:
        result_list.append(get_perission_string(permission))
    return result_list

def get_perission_string(permission):
    match permission.permission_type:
        case PermissionType.CREATE_WORK_ODER_CLEANING:
            return "create_work_order_cleaning"
        case PermissionType.CREATE_WORK_ODER_MAID_REQ:
            return "create_work_order_maid_req"
        case PermissionType.CREATE_WORK_ODER_AMENITY_REQ:
            return "create_work_order_amenity_req"
        case PermissionType.CREATE_WORK_ODER_TECHNICIAN_REQ:
            return "create_work_order_technician_req"
        
def check_permission(required_permission, permission_list):
    if required_permission in permission_list:
        return True
    return False