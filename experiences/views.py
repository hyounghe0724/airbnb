from django.db import transaction
from rest_framework.views import APIView
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, ParseError
from .models import Perk, Experience
from categories.models import Category
from .serializers import (
    PerkSerializer,
    ExperienceSerializer,
    ExperienceDetailSerializer,
)
from bookings.models import Booking
from bookings.serializers import (
    CreateExperienceBookingSerializer,
    PublicBookingSerializer,
)
from rest_framework.response import Response

# Create your views here.


class Perks(APIView):
    def get(self, request):
        all_perks = Perk.objects.all()
        serializer = PerkSerializer(all_perks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PerkSerializer(data=request.data)
        if serializer.is_valid():
            perk = serializer.save()
            return Response(PerkSerializer(perk).data)
        else:
            return Response(serializer.errors)


class PerkDetail(APIView):
    def get_object(self, pk):
        try:
            return Perk.objects.get(pk=pk)
        except Perk.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        perk = self.get_object(pk=pk)
        serializer = PerkSerializer(perk)
        return Response(serializer.data)

    def put(self, request, pk):
        perk = self.get_object(pk=pk)
        serializer = PerkSerializer(perk, data=request.data, partial=True)
        if serializer.is_valid():
            updated_perk = serializer.save()
            return Response(PerkSerializer(updated_perk).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        perk = self.get_object(pk)
        perk.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class Experiences(APIView):  # GET POST All Experience list
    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request):

        experiences = Experience.objects.all()
        serializer = ExperienceSerializer(
            experiences, many=True, context={"request": request}
        )
        return Response(serializer.data)

    def post(self, request):

        serializer = ExperienceSerializer(data=request.data)
        # room or experience ,
        if serializer.is_valid():
            category_pk = request.data.get("category")
            if not category_pk:
                raise ParseError("Category is required.")
            try:
                category = Category.objects.get(pk=category_pk)
                if category.kind == Category.CategoryKindChoices.ROOMS:
                    raise ParseError("The Category kind should be 'experience'")
            except Category.DoesNotExist:
                raise ParseError("Category Not Found")
            try:
                with transaction.atomic():
                    """
                    transaction is search error in this code
                    transaction examine revise infomation in code
                    if error is exist, transaction not push in DB
                    if error isnt exist, transaction push in DB
                    """
                    new_experience = serializer.save(
                        host=request.user,
                        category=category,
                    )
                    perks = request.data.get("perks")
                    for perk_pk in perks:
                        perk = Perk.objects.get(pk=perk_pk)
                        new_experience.perks.add(perk)
                    return Response(serializer(new_experience).data)
            except:
                raise ParseError
        else:
            raise Response(serializer.errors)

class ExperienceDetail(APIView):
    pass
class ExperienceRevise(APIView):  # PUT DELETE
    permission_classes = [IsAuthenticated]

    def get_object(self, ex_pk):
        try:
            experience = Experience.objects.get(pk=ex_pk)
            return experience
        except Experience.DoesNotExist:
            raise NotFound

    def put(self, request, ex_pk):

        experience = self.get_object(ex_pk)
        serializer = ExperienceDetailSerializer(
            experience,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():

            if "category" in request.data:
                category_pk = request.data.get("category")

                try:
                    category = Category.objects.get(pk=category_pk)
                    if category.kind == category.CategoryKindChoices.ROOMS:
                        raise ParseError("Category kind should be Experience")
                    experience.category = category
                except Category.DoesNotExist:
                    raise ParseError("Category model is not exist")

            if "perks" in request.data:
                try:
                    perks = request.data.get("perks")
                    if perks:
                        experience.perks.clear()
                        for perk_pk in perks:
                            perk = Perks.objects.get(pk=perk_pk)
                            experience.perks.add(perk)

                except Exception:
                    raise ParseError("Perks is Not Found")

            update_experience = serializer.save()
            return Response(ExperienceDetailSerializer(update_experience).data)
        else:
            raise Response(serializer.errors)

    def delete(self, request, ex_pk):
        experience = Experience.objects.get(pk=ex_pk)
        experience.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class ExperBooking(APIView):  # GET POST
    permission_classes = [IsAuthenticated]

    def get_object(self, ex_pk):
        try:
            experience = Experience.objects.get(pk=ex_pk)
            return experience
        except Experience.DoesNotExist:
            raise NotFound

    def get(self, request, ex_pk):

        experience = self.get_object(ex_pk)
        serializer = ExperienceDetailSerializer(experience)
        return Response(serializer.data)

    def post(self, request, ex_pk):

        experience = self.get_object(ex_pk)
        serializer = CreateExperienceBookingSerializer(data=request.data)
        if serializer.is_valid():
            booking = serializer.save(
                experience=experience,
                user=request.user,
                kind=Booking.BookingKindChoices.EXPERIENCE,
            )
            serializer = PublicBookingSerializer(booking)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
