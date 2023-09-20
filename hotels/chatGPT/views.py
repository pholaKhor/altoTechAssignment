import openai
import json
import re
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from work_order.response_utils import convert_mongo_object_to_response
from work_order.db_utils import aggregate_work_order, get_all_work_order
from hotels.settings import CHAT_GPT_KEY

openai.api_key = CHAT_GPT_KEY

# Create your views here.
class GetWorkOrderByOpenAiAPIView(APIView):
    def post(self, request):
        data = request.data
        query_cmd = data["command"]        
        temperature = 0.1
        # Description work order structure data
        full_cmd = "I have a mongoDb with this structure :" \
             " { id,status,room,type,startedAt,finishedAt } " \
             + query_cmd + ". Generate string JSON format for the MongoDB aggregation pipeline." \
             " Provide your answer in JSON form. Reply with only the answer in JSON form and include no other commentary"
        messages = [{"role": "user", "content": full_cmd}]
        # call the openai API
        response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=temperature,
                max_tokens=1000,
            )            
        # format the response
        formatted_response = response['choices'][0]['message']['content'].replace('\n', '')
        clean_json  = re.compile('ISODate\(("[^"]+")\)').sub('\\1', formatted_response)
        json_response = json.loads('[' + clean_json + ']')
        result = aggregate_work_order(json_response)
        if result is None:
            return Response({}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        convert_mongo_object_to_response(result)
        return Response(result, status=status.HTTP_200_OK)
    
class AnalyzeWorkOrderAPIView(APIView):
    def post(self, request):
        data = request.data
        query_cmd = data["command"]
        temperature = 0.1
        work_order = get_all_work_order()
        full_cmd = "I have a mongoDb with this structure :" \
             " { id,status,room,type,startedAt,finishedAt } " \
             " type can only be [CLEANING, MAID_REQUEST, TECHNICIAN_REQUEST, AMENITY_REQUEST] " \
             " status can only be [CREATED, ASSIGNED, IN_PROGRESS, DONE, CANCEL, CANCELLED_BY_GUEST] " \
             " this is all data:" + str(work_order) + ". " + query_cmd + \
             " Generate only string JSON format for each element." \
             " Provide your answer in JSON form. Reply with only the answer in JSON form and include no other commentary"
        
        messages = [{"role": "user", "content": full_cmd}]
        # call the openai API
        response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=temperature,
                max_tokens=1000,
            )
        formatted_response = response['choices'][0]['message']['content'].replace('\n', '')
        clean_json  = re.compile('ISODate\(("[^"]+")\)').sub('\\1', formatted_response)
        json_response = json.loads('[' + clean_json + ']')
        return Response(json_response, status=status.HTTP_200_OK)
    