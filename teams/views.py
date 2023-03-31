from django.forms import model_to_dict
from rest_framework.views import APIView, status
from rest_framework.response import Response
from .utils import data_processing
from .models import Team
from .constrains import FIRST_CUP, TITLES
from .exceptions import InvalidYearCupError, ImpossibleTitlesError, NegativeTitlesError


class TeamViewAll(APIView):
    def post(self, request):
        team = request.data
        try:
            data_processing(dict(first_cup=team[FIRST_CUP], titles=team[TITLES]))
        except InvalidYearCupError as error:
            return Response(dict(error=error.message), status.HTTP_400_BAD_REQUEST)
        except ImpossibleTitlesError as error:
            return Response(dict(error=error.message), status.HTTP_400_BAD_REQUEST)
        except NegativeTitlesError as error:
            return Response(dict(error=error.message), status.HTTP_400_BAD_REQUEST)

        team = Team.objects.create(**team)
        return Response(model_to_dict(team), status.HTTP_201_CREATED)

    def get(self, request):
        teams_raw = Team.objects.all()
        teams_dict = [model_to_dict(t) for t in teams_raw]
        return Response(teams_dict, status.HTTP_200_OK)


class TeamViewSpecific(APIView):
    not_found = dict(message='Team not found')

    def get(self, request, pk):
        try:
            team_raw = Team.objects.get(pk=pk)
        except Team.DoesNotExist:
            return Response(self.not_found, status.HTTP_404_NOT_FOUND)
        team_dict = model_to_dict(team_raw)
        return Response(team_dict, status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            Team.objects.get(pk=pk).delete()
        except Team.DoesNotExist:
            return Response(dict(self.not_found), status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk):
        try:
            team = Team.objects.get(pk=pk)
        except Team.DoesNotExist:
            return Response(self.not_found, status.HTTP_404_NOT_FOUND)
        team_request = request.data
        [setattr(team, k, v) for k, v in team_request.items()]
        team.save()
        team_dict = model_to_dict(team)
        return Response(team_dict, status.HTTP_200_OK)
