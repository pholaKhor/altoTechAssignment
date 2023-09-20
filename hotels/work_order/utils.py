 
from enum import Enum 

class WORK_ORDER_TYPE(Enum):
    CLEANING = 0,
    MAID_REQUEST = 1,
    TECHNICIAN_REQUEST = 2,
    AMENITY_REQUEST = 3

class WORK_ORDER_STATUS(Enum):
    CREATED = 0,
    ASSIGNED = 1,
    IN_PROGRESS = 2,
    DONE = 3,
    CANCEL = 4,
    CANCELLED_BY_GUEST = 5

def get_work_order_type_enum(work_order_type):
    match work_order_type.upper():
        case "CLEANING":
            return WORK_ORDER_TYPE.CLEANING
        case "MAID_REQUEST":
            return WORK_ORDER_TYPE.MAID_REQUEST
        case "TECHNICIAN_REQUEST":
            return WORK_ORDER_TYPE.TECHNICIAN_REQUEST
        case "AMENITY_REQUEST":
            return WORK_ORDER_TYPE.AMENITY_REQUEST
    return None

def get_work_order_status_string(work_order_status):
    match work_order_status:
        case WORK_ORDER_STATUS.CREATED:
            return "CREATED"
        case  WORK_ORDER_STATUS.ASSIGNED:
            return "ASSIGNED"
        case WORK_ORDER_STATUS.IN_PROGRESS:
            return "IN_PROGRESS"
        case WORK_ORDER_STATUS.DONE:
            return "DONE"
        case WORK_ORDER_STATUS.CANCEL:
            return "CANCEL"
    return "UNKNOW"

def get_work_order_status_enum(work_order_status):
    match work_order_status.upper():
        case "CREATED":
            return WORK_ORDER_STATUS.CREATED
        case "ASSIGNED":
            return WORK_ORDER_STATUS.ASSIGNED
        case "IN_PROGRESS":
            return WORK_ORDER_STATUS.IN_PROGRESS
        case "DONE":
            return WORK_ORDER_STATUS.DONE
        case "CANCEL":
            return WORK_ORDER_STATUS.CANCEL
    return None