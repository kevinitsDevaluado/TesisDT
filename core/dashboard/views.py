import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, FloatField
from django.db.models.functions import Coalesce
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import requires_csrf_token
from django.views.generic import TemplateView
from core.erp.forms import SportLeagueForm
from django.db import transaction
from core.homepage.models import *
from core.security.models import Dashboard
from core.user.models import User
from core.erp.models import *
from django.http import JsonResponse, HttpResponse
from django.contrib import messages

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'vtcpanel.html'
    
    def validate_data(self):
            data = {'valid': True}
            try:
                type = self.request.POST['type']
                obj = self.request.POST['obj'].strip()
                obj2 = self.request.POST['obj2'].strip()
                obj3 = 'Evaluacion'
                pk = self.kwargs['pk']

                if type == 'estudiante':
                    if SportLeagueForm.objects.filter(estudiante_id=obj,curso_id=pk):
                        data['valid'] = False
                elif type == 'name':
                    if SportLeagueForm.objects.filter(name__icontains=obj,curso_id=pk):
                        data['valid'] = False
            except:
                pass
            return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        data = {}
        try:
            if action == 'addSportLeague':
                with transaction.atomic():
                    form = SportLeagueForm(request.POST, files=request.FILES)
                    if form.is_valid():
                        form.save()
                        #messages.info(request, 'Máquina registrada correctamente')
            elif action == 'listSportLeague':
                data = []
                user = User.objects.get(id=self.request.user.id)
                if Client.objects.filter(user_id=user.id).exists():
                    id_client= Client.objects.get(user_id=user.id)
                    for i in SportLeague.objects.filter(state= True,client_id = id_client).order_by('id'):
                        data.append(i.toJSON()) 
                else:
                    for i in SportLeague.objects.filter(state= True).order_by('id'):
                        data.append(i.toJSON())   
            elif action == 'validate_data':
                return self.validate_data()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')


    def get(self, request, *args, **kwargs):
        request.user.set_group_session()
        context = self.get_context_data()
        dashboard = Dashboard.objects.filter()
        if dashboard.exists():
            context['SportLeague'] = SportLeagueForm()
            return render(request, 'vtcpanel.html', context)
        return render(request, 'hztpanel.html', context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Panel de administración'
        return context


@requires_csrf_token
def error_404(request, exception):
    return render(request, '404.html', {})


@requires_csrf_token
def error_500(request, exception):
    return render(request, '500.html', {})
