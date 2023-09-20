from rest_framework.response import Response
from rest_framework import status
from bson import ObjectId

def convert_mongo_object_to_response(results):
    for result in results:
        for key, value in result.items():
            if type(value) == ObjectId:
                result[key] = str(value)

def get_internal_error_response():
    return Response({"detail":"Internal error."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def get_not_found_response(param):
    return Response({"detail": param + " not found."},
                    status=status.HTTP_404_NOT_FOUND)

def get_no_permission_response():
    return Response({"detail": "No permission."},
                    status=status.HTTP_403_FORBIDDEN)

def get_invalid_param_response(param):
    return Response({"detail": "Invalid parameter: " + param},
                  status=status.HTTP_400_BAD_REQUEST)

def get_missing_require_param_response(require_param):
    return Response({"detail": "Missing require parameter: " + require_param},
                  status=status.HTTP_400_BAD_REQUEST)