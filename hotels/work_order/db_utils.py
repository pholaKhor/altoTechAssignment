from bson import ObjectId
from pymongo import MongoClient
from hotels.settings import MONGO_DB_CONNECTION_STRING, MONGO_DB_NAME



COLLECTION_NAME = "work_order"

def get_db():
    try:
        client = MongoClient(MONGO_DB_CONNECTION_STRING)
        db = client[MONGO_DB_NAME]
    except Exception as e:
        print("Error:" + str(e))
        return None
    return db[COLLECTION_NAME]

def get_all_work_order():
    db = get_db()
    try:
        work_orders = list(db.find())
    except Exception as e:
        print("Error:" + str(e))
        return None
    return work_orders

def get_work_order(db, work_order_id):
    try:
        work_order = db.find_one({"_id": ObjectId(work_order_id)})
    except Exception as e:
        print("Error:" + str(e))
        return None
    return work_order

def create_work_order(work_order):
    db = get_db()
    if db is None:
        return None
    try:
        _id = db.insert_one(work_order)
    except Exception as e:
        print("Error:" + str(e))
        return None
    return str(_id.inserted_id)

def update_work_order(work_order_id, update_worker):
    db = get_db()
    if db is None:
        return False
    try:
        db.update_one(
            {'_id':ObjectId(work_order_id)}, # filter
            {"$set": update_worker} # update value
            )
    except Exception as e:
        print("Error:" + str(e))
        return False
    return True

def aggregate_work_order(cmd):
    db = get_db()
    try:
        result = list(db.aggregate(cmd))
    except Exception as e:
        print("Error:" + str(e))
        return None
    return result

