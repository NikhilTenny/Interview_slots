from rest_framework import serializers
from datetime import datetime
from .models import TimeSlots, User



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'user_type', 'first_name', 'last_name']



class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlots
        fields = ['id', 'user', 'from_time', 'to_time']

    def validate(self, data):
        # Validate that 'from_time' is before 'to_time'
        if data['from_time'] >= data['to_time']:
            raise serializers.ValidationError("`from_time` must be earlier than `to_time`.")
        
    
class SlotRegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    date = serializers.DateField()  # Input in YYYY-MM-DD format
    from_time = serializers.CharField(max_length=8)  # Input as "10:30:PM"
    to_time = serializers.CharField(max_length=8)  # Input as "11:30:PM"
    user_type = serializers.ChoiceField(choices=["candidate", "interviewer"])  


    def validate(self, data):
        date_str = data['date'].strftime('%Y-%m-%d')  # Convert date object to string

        try:
            from_time_str = f"{date_str} {data['from_time']}"
            data['from_time'] = datetime.strptime(from_time_str, "%Y-%m-%d %I:%M:%p")
        except ValueError:
            raise serializers.ValidationError("Invalid `from_time` format. Use 'HH:MM:PM/AM'.")

        try:
            to_time_str = f"{date_str} {data['to_time']}"
            data['to_time'] = datetime.strptime(to_time_str, "%Y-%m-%d %I:%M:%p")
        except ValueError:
            raise serializers.ValidationError("Invalid `to_time` format. Use 'HH:MM:PM/AM'.")

        # Validate time range
        if data['from_time'] >= data['to_time']:
            raise serializers.ValidationError("`from_time` must be earlier than `to_time`.")

        return data
    
class SlotListingSerializer(serializers.Serializer):
    interviewer = serializers.IntegerField()
    candidate = serializers.IntegerField()

        
