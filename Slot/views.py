from django.shortcuts import render
from rest_framework import views, response
from .serializers import SlotRegisterSerializer, SlotListingSerializer
from .models import User, TimeSlots
from datetime import datetime, timedelta


class SlotBooking(views.APIView):
    def get(self, request):
        """
            API to fetch the interview schedulable time slots for
            and given candidate and interviewer.
        """
        req_data = request.query_params

        serializer = SlotListingSerializer(data=req_data)
        if not serializer.is_valid():
            error_message = "; ".join(
                f"{field}: {', '.join(messages)}" for field, messages in serializer.errors.items()
            )
            return self.handle_error(error_message, 400)

        serialized_data = serializer.data
        
        candidate_id, interviewer_id = serialized_data['candidate'], \
            serialized_data['interviewer']
        cand_slot = self.get_user_slot(candidate_id, 'candidate')
        interv_slot = self.get_user_slot(interviewer_id, 'interviewer')

        if not cand_slot or not interv_slot:
            return  self.handle_error('Please provide a valid user id.', 400)

        available_slots = self.find_available_slots(
            cand_slot, interv_slot
        )

        if not available_slots:
            response_data = {'result': "Sorry, no slots available."}
        else:
            response_data = {"result":available_slots}
        
        return response.Response(response_data, 200)
    
    def get_user_slot(self, user_id, user_type):
        """
            Method to fetch a record from 'TimeSlot' table
            based on the given user_id and user_type
        """
        try:
            user_slot = TimeSlots.objects.get(
                user_id=user_id,
                user__user_type=user_type
            )
        except TimeSlots.DoesNotExist:
            user_slot = None

        return user_slot
    
    def find_available_slots(
            self, cand_slot: datetime, interv_slot: datetime
        )-> list:
        """
            Method to find the list of 1-hour interview time slots from the
            candidate's and interviewer's available time slot.
        """
        cand_to_time = cand_slot.to_time
        cand_from_time = cand_slot.from_time
        interv_to_time = interv_slot.to_time
        interv_from_time = interv_slot.from_time

        # Find the mininum start and end time
        overlap_start = max(cand_from_time, interv_from_time)
        overlap_end = min(cand_to_time, interv_to_time)

        
        available_slots = []
        current_start = overlap_start

        while current_start + timedelta(hours=1) <= overlap_end:
            slot_start_hour = current_start.hour
            slot_end_hour = (current_start + timedelta(hours=1)).hour
            available_slots.append((slot_start_hour,slot_end_hour))
            current_start += timedelta(hours=1)

        return available_slots

    
    def post(self, request):
        """
            API to register an interviewer/candidate with necessary details and 
            their available time.
        """

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
            except Exception:
                return self.handle_error("Something went wrong.", 500)
            
        result = f"Registration succesfull for user id `{user_obj.id}`"

        return response.Response(data={'result':result})
    
    def handle_error(self, error: str, status: int):
        return response.Response(
            {"Error": error},
            status=status,
        )
    
    def create_user_record(self, serialized_data: dict):
        """
            Creates a new record for the 'User' model
        """
        user_obj = User(
            user_type = serialized_data['user_type'],
            email = serialized_data['email'],
            first_name = serialized_data['first_name'],
            last_name = serialized_data['last_name'],
        )
        user_obj.save()
        return user_obj


    def create_timeslot_record(self, user_obj: User, serialized_data: dict):
        """
            Creates a new record for the 'TimeSlots' model
        """
        time_slot_obj = TimeSlots(
            user = user_obj,
            to_time = serialized_data["to_time"],
            from_time = serialized_data["from_time"]
        )
        time_slot_obj.save()
