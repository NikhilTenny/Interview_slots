from django.shortcuts import render
from rest_framework import views, response
from .serializers import SlotRegisterSerializer, SlotListingSerializer
from .models import User, TimeSlots


class SlotBooking(views.APIView):
    def get(self, request):
        req_data = request.query_params
        serializer = SlotListingSerializer(data=req_data)
        if not serializer.is_valid():
            error_message = "; ".join(
                f"{field}: {', '.join(messages)}" for field, messages in serializer.errors.items()
            )
            return self.handle_error(error_message, 400)

        serialized_data = serializer.data
        # user = User.objects.get(email=serialized_data['candidate_email'])


        
        return response.Response(data=serialized_data)
    
    def post(self, request):
        #TODO
        # email validation
        # logging
        req_data = request.data
        serializer = SlotRegisterSerializer(data = req_data)

        if not serializer.is_valid():
            error_message = "; ".join(
                f"{field}: {', '.join(messages)}" for field, messages in serializer.errors.items()
            )
            return self.handle_error(error_message, 400)

        serialized_data = serializer.data
        user_exists = User.objects.filter(email=serialized_data['email'])
        if user_exists:
            return self.handle_error("User already exists.", 400)
        else:
            try:    
                user_obj = self.create_user_record(serialized_data)
                self.create_timeslot_record(user_obj, serialized_data)
            except Exception as e:
                return self.handle_error("Something went wrong.", 500)

        return response.Response(data=req_data)
    
    def handle_error(self, error, status):
        return response.Response(
            {"Error": error},
            status=status,
        )
    
    def create_user_record(self, serialized_data):
        user_obj = User(
            user_type = serialized_data['user_type'],
            email = serialized_data['email'],
            first_name = serialized_data['first_name'],
            last_name = serialized_data['last_name'],
        )
        user_obj.save()
        return user_obj


    def create_timeslot_record(self, user_obj, serialized_data):
        time_slot_obj = TimeSlots(
            user = user_obj,
            to_time = serialized_data["to_time"],
            from_time = serialized_data["from_time"]
        )
        time_slot_obj.save()
