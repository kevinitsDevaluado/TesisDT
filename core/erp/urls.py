from django.urls import path

from core.erp.views.ProfileLeague.views import *
from core.erp.views.Referee.views import *
from core.erp.views.Training.views import *
from core.erp.views.client.views import *
from core.erp.views.Quote.views import *
from core.erp.views.DetailsGames.views import *
urlpatterns = [
    path('profile/<int:pk>/', ProfileListView.as_view(), name='profile'),
    # Referees
    path('Referee/', RefereeListView.as_view(), name='referee_list'),
    path('Referee/add/', RefereeCreateView.as_view(), name='referee_create'),
    path('Referee/update/<int:pk>/', RefereeUpdateView.as_view(), name='referee_update'),
    path('Referee/delete/<int:pk>/', RefereeDeleteView.as_view(), name='referee_delete'),
    path('Referee/update/profile/', RefereeUpdateProfileView.as_view(), name='referee_update_profile'),
    path('ProfileLeague/delete/<int:pk>/', ProfileLeagueDeleteView.as_view(), name='profileLeague_delete'),
    path('TeamSoccer/delete/<int:id>/', TeamDeleteView, name='teamSoccer_delete'),
    path('TeamSoccer/update/<int:id>/', updateTeamSoccer, name='teamSoccer_update'),
    path('Stadium/delete/<int:id>/', StadiumDeleteView, name='stadium_delete'),
    path('Game/delete/<int:id>/', DetailsGamesDeleteView, name='game_delete'),
    path('Stadium/update/<int:id>/', updateStadium, name='stadium_update'),
    # Entrenamientos
    path('Training/', TrainingListView.as_view(), name='training_list'),
    path('Training/add/', TrainingCreateView.as_view(), name='training_create'),
    path('Training/update/<int:pk>/', TrainingUpdateView.as_view(), name='training_update'),
    path('Training/delete/<int:pk>/', TrainingDeleteView.as_view(), name='training_delete'),
    path('Training/Profile/<int:pk>/', TrainingProfileListView.as_view(), name='verTraining'),

    # Cuota
    path('Quote/', QuoteListView.as_view(), name='quote_list'),
    path('Quote/add/', QuoteCreateView.as_view(), name='quote_create'),
    path('Quote/update/<int:pk>/', QuoteUpdateView.as_view(), name='quote_update'),
    path('Quote/delete/<int:pk>/', QuoteDeleteView.as_view(), name='quote_delete'),
    path('Quote/Profile/<int:pk>/', QuoteProfileListView.as_view(), name='verCuota'),
     # clients
    path('client/', ClientListView.as_view(), name='client_list'),
    path('client/add/', ClientCreateView.as_view(), name='client_create'),
    path('client/update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('client/delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
    path('client/update/profile/', ClientUpdateProfileView.as_view(), name='client_update_profile'),
    #detailgame
    path('detailsgame/add/<int:pk>/', DetailsGamesListView.as_view(), name='addDetailGame'),
]
