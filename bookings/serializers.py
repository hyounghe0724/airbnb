from django.utils import timezone
from rest_framework import serializers
from .models import Booking


class CreateRoomBookingSerializer(serializers.ModelSerializer):

    check_in = serializers.DateField()
    check_out = serializers.DateField()

    class Meta:
        model = Booking
        fields = (
            "check_in",
            "check_out",
            "guests",
        )

    def validate_check_in(self, value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("Can't book in the past!")
        return value

    def validate_check_out(self, value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("Can't book in the past!")
        return value

    def validate(self, data):
        if data["check_out"] <= data["check_in"]:
            raise serializers.ValidationError(
                "Check in Should be smaller than check out"
            )
        if Booking.objects.filter(
            check_in__lte=data["check_out"],
            check_out__gte=data["check_in"],
        ).exists():
            raise serializers.ValidationError(
                "Those(or some) of those dates are already taken."
            )
        return data


class ReviseRoomBookingSerializer(serializers.ModelSerializer):
    check_in = serializers.DateField()
    check_out = serializers.DateField()

    class Meta:
        model = Booking
        fields = (
            "check_in",
            "check_out",
            "guests",
        )

    def validate_check_in(self, value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("Can't book in the past!")
        return value

    def validate_check_out(self, value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("Can't book in the past!")
        return value


class CreateExperienceBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = (
            "experience_time",
            "guests",
        )

    def validate_experience_time(self, value):
        # value request user send data
        now = timezone.now()
        if now > value:
            raise serializers.ValidationError("Can't book in the past!")
        return value

    """
    experience 라서 시간대별로 체크해야함

    과거의 시간대는 표시 안하고
    현재부터 미래의 시간대만 표시 (날짜)
    
    room 과는 다르게 날짜 시간 둘다 따져야함
    같은 날짜라도 시간이 다르면 이용가능
    """


class ReviseExperBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = (
            "experience_time",
            "guests",
        )

    def validate_experience_time(self, value):
        # value request user send data
        now = timezone.now()
        if now > value:
            raise serializers.ValidationError("Can't book in the past!")
        return value


class PublicBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = (
            "pk",
            "check_in",
            "check_out",
            "experience_time",
            "guests",
        )
