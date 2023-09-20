def create_work_order(work_order): 
    # check data in db optional
    return "insert_id"

def get_db():
    return True

def get_work_order(db, work_order_id):
    match work_order_id:
        case "cleaningCreate1":
            work_order = {
                "_id": work_order_id,
                "createdBy": "MaidSupervisor_user",
                "room": 999,
                "type": "CLEANING",
                "status": "CREATED"
            }
        case "cleaningAssigned1":
            work_order = {
                "_id": work_order_id,
                "createdBy": "MaidSupervisor_user",
                "room": 999,
                "type": "CLEANING",
                "status": "ASSIGNED"
            }
        case "cleaningInprogress1":
            work_order = {
                "_id": work_order_id,
                "createdBy": "MaidSupervisor_user",
                "assignedTo": "supervisor_user",
                "room": 999,
                "type": "CLEANING",
                "status": "IN_PROGRESS"
            }
    return work_order

def update_work_order(work_order_id, update_worker):
    # check data in db optional
    return True
