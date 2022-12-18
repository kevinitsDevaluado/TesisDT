import json

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db import transaction
from django.http import JsonResponse, HttpResponse

from core.erp.forms import Quote, QuoteForm
from core.security.mixins import PermissionMixin
from core.erp.models import *
from django.contrib import messages
from decimal import Decimal

class QuoteListView(PermissionMixin, ListView):
    model = Quote
    template_name = 'Quote/list.html'
    permission_required = 'view_quote'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add_asistencia':
                with transaction.atomic():
                    pass
            elif action == 'searchListAsistencia':
                with transaction.atomic():
                    pass
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('quote_create')
        context['QuoteListaTotal'] = Quote.objects.all()
        context['title'] = 'Listado de Cuotas'
        context['referee'] = Referee.objects.all()
        return context

class QuoteProfileListView(PermissionMixin, ListView):
    model = DebtReferee
    template_name = 'Quote/listProfile.html'
    permission_required = 'view_quote'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('verCuota', kwargs={'pk': pk})

    def validate_data(self):
        data = {'valid': True}
        try:
            type = self.request.POST['type']
            obj = self.request.POST['obj'].strip()
            if type == 'id_price_cuota':
                if User.DebtReferee.filter(dni=obj):
                    data['valid'] = False
            elif type == 'mobile':
                if Client.objects.filter(mobile=obj):
                    data['valid'] = False
            elif type == 'email':
                if User.objects.filter(email=obj):
                    data['valid'] = False
        except:
            pass
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add_cuotapago':
                with transaction.atomic():
                    cuota_id = self.kwargs['pk']
                    referee_id = request.POST['id_refereeList']
                    valor = request.POST['id_price_cuota']
                    query = DebtReferee.objects.get(cuota_id = cuota_id, referee_id = referee_id)
                    if Decimal(valor) <= Decimal(query.price):
                        model = DebtRepayment()
                        model.deuda_id = query.id
                        model.price = valor
                        model.save()
                        #actualizamos la deuda
                        query.price = query.price - Decimal(valor)
                        query.save()
                    else :
                        messages.info(request, 'Valor fuera de rango')
                        

            elif action == 'searchListAsistencia':
                with transaction.atomic():
                    pass
            elif action == 'validate_data':
                return self.validate_data()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query  = DebtReferee.objects.filter(cuota_id = self.kwargs['pk'])
        context['listTotal'] = DebtRepayment.objects.filter(deuda__cuota__id = self.kwargs['pk']).distinct().order_by('deuda__cuota__id')
        context['getPerfil'] = Quote.objects.get(id = self.kwargs['pk'])
        context['arbitros'] = Referee.objects.all()
        context['listDebt'] = query
        context['title'] = 'Listado de Cuotas Arbitro'
        context['referee'] = Referee.objects.all()
        return context


class QuoteCreateView(PermissionMixin, CreateView):
    model = Quote
    template_name = 'Quote/create.html'
    form_class = QuoteForm
    success_url = reverse_lazy('quote_list')
    permission_required = 'add_quote'


   

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                data = self.get_form().save()
                query = Quote.objects.first()
                refereeList = Referee.objects.all()
                for i in refereeList:
                    print(i.id)
                    asistencia = DebtReferee()
                    asistencia.cuota_id = query.id
                    asistencia.price = query.price
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
        context['title'] = 'Nuevo registro de una Cuota'
        context['action'] = 'add'
        return context


class QuoteUpdateView(PermissionMixin, UpdateView):
    model = Quote
    template_name = 'Quote/create.html'
    form_class = QuoteForm
    success_url = reverse_lazy('quote_list')
    permission_required = 'change_quote'

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
        context['title'] = 'Edición de una Cuota'
        context['action'] = 'edit'
        return context


class QuoteDeleteView(PermissionMixin, DeleteView):
    model = Quote
    template_name = 'Quote/delete.html'
    success_url = reverse_lazy('quote_list')
    permission_required = 'delete_quote'

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
