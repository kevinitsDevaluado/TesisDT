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
from core.erp.models import *

class DetailsGamesListView(CreateView):
    model = DetailsGames
    template_name = 'DetailsGames/create.html'
    form_class = DetailsGamesForm

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                form = DetailsGamesForm(request.POST, files=request.FILES)
                if form.is_valid():
                    form.instance.game_id = self.kwargs['pk']
                    form.save()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        query = GameFootball.objects.get(id = self.kwargs['pk'])
        context['list_url'] = reverse_lazy('profile', kwargs={'pk': query.teamLocal.sportLeague.id})
        context['title'] = 'Nuevo'
        context['action'] = 'add'
        return context
