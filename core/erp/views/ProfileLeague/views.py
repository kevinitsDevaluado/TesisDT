import json
import random
from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView,TemplateView, View
from django.db import transaction
from django.db.models import Q
from datetime import datetime
from django.utils import timezone
from core.security.mixins import PermissionMixin
from core.homepage.models import *
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse,HttpResponseRedirect
from django.template.loader import get_template
from weasyprint import HTML, CSS
from crum import get_current_user
from core.erp.models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from core.erp.forms import *
from django.views.decorators.csrf import csrf_exempt, csrf_protect


class ProfileListView(LoginRequiredMixin, CreateView):
    model = SportLeague
    template_name = 'ProfileLeague/Profile.html'
    form_class = SportLeagueForm

    #permission_required = 'change_juegos'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('profile', kwargs={'pk': pk})
    
    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        data = {}
        try:
            if action == 'addTeam':
                with transaction.atomic():
                    form = TeamLeagueForm(request.POST, files=request.FILES)
                    if form.is_valid():
                        form.instance.sportLeague_id = self.kwargs['pk']
                        form.save()
                        print("guardado") 
                    else :
                        print("error")
            elif action == 'listTeam':
                data = []
                for i in Team.objects.filter(state= True, sportLeague = self.kwargs['pk']).order_by('id'):
                    data.append(i.toJSON())
            elif action == 'addStadium':
                with transaction.atomic():
                    form = StadiumForm(request.POST, files=request.FILES)
                    if form.is_valid():
                        form.instance.sportLeague_id = self.kwargs['pk']
                        form.save()
                        print("guardado") 
                    else :
                        print("error")
            elif action == 'listStadium':
                data = []
                for i in Stadium.objects.filter(state= True, sportLeague = self.kwargs['pk']).order_by('id'):
                    data.append(i.toJSON())
            elif action == 'addGame':
                with transaction.atomic():
                    form = GameForm(request.POST, files=request.FILES)
                    if form.is_valid():
                        #form.instance.sportLeague_id = self.kwargs['pk']
                        form.save()
                        print("guardado") 
                    else :
                        print("error")
            elif action == 'listGame':
                data = []
                for i in GameFootball.objects.filter(state= True,teamLocal__sportLeague_id = self.kwargs['pk']).order_by('id'):
                    data.append(i.toJSON())
            elif action == 'editSportLeague':
                with transaction.atomic():
                    query = SportLeague.objects.get(id=self.kwargs['pk'])
                    form = SportLeagueForm(request.POST, instance=query, files=request.FILES)
                    if form.is_valid():
                        form.save()
            elif action == 'search_team':
                data = []
                term = request.POST['term']
                for i in Team.objects.filter(name__icontains=term, sportLeague_id = self.kwargs['pk']):
                    item = {'id': i.id, 'text': i.__str__(), 'data': i.toJSON()}
                    data.append(item)
            elif action == 'search_stadium':
                data = []
                term = request.POST['term']
                for i in Stadium.objects.filter(name__icontains=term, sportLeague_id = self.kwargs['pk'])[0:10]:
                    item = {'id': i.id, 'text': i.__str__(), 'data': i.toJSON()}
                    data.append(item)
            elif action == 'validate_data':
                return self.validate_data()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        query = SportLeague.objects.get(id=self.kwargs['pk'])
        context['getProfileLegue'] = SportLeague.objects.get(id=self.kwargs['pk'])
        context['getProfileLegueCount'] = Team.objects.filter(id=self.kwargs['pk']).count()
        context['formTeam'] = TeamLeagueForm()
        context['formStadium'] = StadiumForm()
        context['formLeague'] = SportLeagueForm()
        context['formEdit'] = TeamLeagueForm(instance=query)
        context['title'] = "Perfil"
        context['formGame'] = GameForm()
        return context

class ProfileLeagueDeleteView(DeleteView):
    model = SportLeague
    template_name = 'ProfileLeague/delete.html'
    success_url = reverse_lazy('dashboard')
    #permission_required = 'delete_category'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de la Liga'
        context['list_url'] = self.success_url
        context['entity'] = 'Liga'
        return context
        

def TeamDeleteView(request,id):
    id_id = id
    team = Team.objects.get(id = id_id)
    team.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def DetailsGamesDeleteView(request,id):
    id_id = id
    team = GameFootball.objects.get(id = id_id)
    team.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def TeamDeleteView(request,id):
    id_id = id
    team = Team.objects.get(id = id_id)
    team.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def StadiumDeleteView(request,id):
    id_id = id
    stadium = Stadium.objects.get(id = id_id)
    stadium.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@csrf_exempt
def updateTeamSoccer(request,id):
    imageSoccer_edit = request.FILES.get('imageSoccer_edit')
    nameSoccer_edit = request.POST.get('nameSoccer_edit')
    descSoccer_edit = request.POST.get('descSoccer_edit')
    team = Team.objects.get(id = id)
    team.name = nameSoccer_edit
    team.desc = descSoccer_edit
    if(imageSoccer_edit is not None):
        team.image = imageSoccer_edit
    team.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@csrf_exempt
def updateStadium(request,id):
    imageSoccer_edit = request.FILES.get('imageSoccer_editStadium')
    nameSoccer_edit = request.POST.get('nameSoccer_editStadium')
    descSoccer_edit = request.POST.get('descSoccer_editStadium')
    stadium = Stadium.objects.get(id = id)
    stadium.name = nameSoccer_edit
    stadium.desc = descSoccer_edit
    if(imageSoccer_edit is not None):
        stadium.image = imageSoccer_edit
    stadium.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))