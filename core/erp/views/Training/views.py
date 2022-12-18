import json

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db import transaction

from core.erp.forms import Training, TrainingForm
from core.security.mixins import PermissionMixin
from core.erp.models import *

class TrainingListView(PermissionMixin, ListView):
    model = Training
    template_name = 'Training/list.html'
    permission_required = 'view_training'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add_asistencia':
                with transaction.atomic():
                    id_training = request.POST['id_training']
                    check = request.POST.getlist('checks[]') 
                    for u in check:
                        asis = TrainingAssistance.objects.get(training_id = id_training,referee_id = u)
                        asis.asistencia = True
                        asis.save()
                    training = Training.objects.get(id=id_training)
                    training.state = False
                    training.save()
            elif action == 'searchListAsistencia':
                with transaction.atomic():
                    data = []
                    estado = request.POST['estado_list']
                    id_Asistencia = request.POST['id_traininglist']
                    search = TrainingAssistance.objects.filter(training_id = id_Asistencia)
                    if len(estado):
                        if estado == "True":
                            search = search.filter(asistencia=True)
                        elif estado == "False":
                            search = search.filter(asistencia=False)
                        elif estado == "all":
                            search = search.filter()
                    pos = 1
                    for m in search.order_by('id'):
                        item = m.toJSON()
                        item['pos'] = pos
                        data.append(item)
                        pos += 1
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('training_create')
        context['trainingListaTotal'] = Training.objects.all()
        context['title'] = 'Listado de Entrenamientos'
        context['referee'] = Referee.objects.all()
        return context


class TrainingCreateView(PermissionMixin, CreateView):
    model = Training
    template_name = 'Training/create.html'
    form_class = TrainingForm
    success_url = reverse_lazy('training_list')
    permission_required = 'add_training'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                data = self.get_form().save()
                query = Training.objects.first()
                refereeList = Referee.objects.all()
                for i in refereeList:
                    print(i.id)
                    asistencia = TrainingAssistance()
                    asistencia.training_id = query.id
                    asistencia.referee_id = i.id
                    asistencia.save()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de un Entrenamiento'
        context['action'] = 'add'
        return context


class TrainingUpdateView(PermissionMixin, UpdateView):
    model = Training
    template_name = 'Training/create.html'
    form_class = TrainingForm
    success_url = reverse_lazy('training_list')
    permission_required = 'change_training'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'edit':
                data = self.get_form().save()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Edición de un Entrenamiento'
        context['action'] = 'edit'
        return context


class TrainingDeleteView(PermissionMixin, DeleteView):
    model = Training
    template_name = 'Training/delete.html'
    success_url = reverse_lazy('training_list')
    permission_required = 'delete_training'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.get_object().delete()
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Notificación de eliminación'
        context['list_url'] = self.success_url
        return context
