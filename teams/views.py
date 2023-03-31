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
            return Response(dict(error=error.message))
        except ImpossibleTitlesError as error:
            return Response(dict(error=error.message))
        except NegativeTitlesError as error:
            return Response(dict(error=error.message))

        team = Team.objects.create(**team)
        return Response(model_to_dict(team), status.HTTP_201_CREATED)

    def get(self, request):
        teams_raw = Team.objects.all()
        teams_dict = [model_to_dict(t) for t in teams_raw]
        return Response(teams_dict, status.HTTP_200_OK)


