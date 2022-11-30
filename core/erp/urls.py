from django.urls import path

from core.erp.views.ProfileLeague.views import *
from core.erp.views.Referee.views import *
from core.erp.views.Training.views import *
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
    path('Stadium/update/<int:id>/', updateStadium, name='stadium_update'),


    # Entrenamientos
    path('Training/', TrainingListView.as_view(), name='training_list'),
    path('Training/add/', TrainingCreateView.as_view(), name='training_create'),
    path('Training/update/<int:pk>/', TrainingUpdateView.as_view(), name='training_update'),
    path('Training/delete/<int:pk>/', TrainingDeleteView.as_view(), name='training_delete'),
]
