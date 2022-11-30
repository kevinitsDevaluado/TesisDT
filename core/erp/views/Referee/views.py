import json

from django.contrib.auth.models import Group
from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView

from config import settings
from core.erp.forms import *
from core.security.mixins import ModuleMixin, PermissionMixin


class RefereeListView(PermissionMixin, TemplateView):
    template_name = 'Referee/list.html'
    permission_required = 'view_referee'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search':
                data = []
                for i in Referee.objects.filter():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('referee_create')
        context['title'] = 'Listado de Arbitros'
        return context


class RefereeCreateView(PermissionMixin, CreateView):
    model = Referee
    template_name = 'Referee/create.html'
    form_class = RefereeForm
    success_url = reverse_lazy('referee_list')
    permission_required = 'add_referee'

    def validate_data(self):
        data = {'valid': True}
        try:
            type = self.request.POST['type']
            obj = self.request.POST['obj'].strip()
            if type == 'dni':
                if User.objects.filter(dni=obj):
                    data['valid'] = False
            elif type == 'mobile':
                if Referee.objects.filter(mobile=obj):
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
            if action == 'add':
                with transaction.atomic():
                    user = User()
                    user.first_name = request.POST['first_name']
                    user.last_name = request.POST['last_name']
                    user.dni = request.POST['dni']
                    user.username = user.dni
                    if 'image' in request.FILES:
                        user.image = request.FILES['image']
                    user.create_or_update_password(user.dni)
                    user.email = request.POST['email']
                    user.save()

                    referee = Referee()
                    referee.user_id = user.id
                    referee.gender = request.POST['gender']
                    referee.mobile = request.POST['mobile']
                    referee.phone = request.POST['phone']
                    referee.address = request.POST['address']
                    referee.birthdate = request.POST['birthdate']
                    if 'curriculum' in request.FILES:
                        referee.curriculum = request.FILES['curriculum']
                    referee.save()
                    group = Group.objects.get(pk=settings.GROUPS.get('Referee'))
                    user.groups.add(group)
            elif action == 'validate_data':
                return self.validate_data()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de un Arbitro'
        context['action'] = 'add'
        context['instance'] = None
        return context


class RefereeUpdateView(PermissionMixin, UpdateView):
    model = Referee
    template_name = 'Referee/create.html'
    form_class = RefereeForm
    success_url = reverse_lazy('referee_list')
    permission_required = 'change_referee'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        instance = self.object
        form = RefereeForm(instance=instance, initial={
            'first_name': instance.user.first_name,
            'last_name': instance.user.last_name,
            'dni': instance.user.dni,
            'email': instance.user.email,
            'image': instance.user.image,
        })
        return form

    def validate_data(self):
        data = {'valid': True}
        try:
            instance = self.object
            type = self.request.POST['type']
            obj = self.request.POST['obj'].strip()
            if type == 'dni':
                if User.objects.filter(dni=obj).exclude(id=instance.user.id):
                    data['valid'] = False
            elif type == 'mobile':
                if Referee.objects.filter(mobile=obj).exclude(id=instance.id):
                    data['valid'] = False
            elif type == 'email':
                if User.objects.filter(email=obj).exclude(id=instance.user.id):
                    data['valid'] = False
        except:
            pass
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'edit':
                with transaction.atomic():
                    instance = self.object
                    user = instance.user
                    user.first_name = request.POST['first_name']
                    user.last_name = request.POST['last_name']
                    user.dni = request.POST['dni']
                    user.username = user.dni
                    if 'image-clear' in request.POST:
                        user.remove_image()
                        user.image = None
                    if 'image' in request.FILES:
                        user.image = request.FILES['image']
                    user.email = request.POST['email']
                    user.save()

                    Referee = instance
                    Referee.user_id = user.id
                    Referee.gender = request.POST['gender']
                    Referee.mobile = request.POST['mobile']
                    Referee.phone = request.POST['phone']
                    Referee.address = request.POST['address']
                    Referee.birthdate = request.POST['birthdate']
                    Referee.parish_id = int(request.POST['parish'])
                    Referee.profession_id = int(request.POST['profession'])
                    if 'curriculum-clear' in request.POST:
                        Referee.remove_curriculum()
                        Referee.curriculum = None
                    if 'curriculum' in request.FILES:
                        Referee.curriculum = request.FILES['curriculum']
                    Referee.save()
            elif action == 'validate_data':
                return self.validate_data()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Edición de un Arbitro'
        context['action'] = 'edit'
        context['instance'] = self.object
        return context


class RefereeDeleteView(PermissionMixin, DeleteView):
    model = Referee
    template_name = 'Referee/delete.html'
    success_url = reverse_lazy('referee_list')
    permission_required = 'delete_referee'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            with transaction.atomic():
                instance = self.get_object()
                user = instance.user
                instance.delete()
                user.delete()
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Notificación de eliminación'
        context['list_url'] = self.success_url
        return context


class RefereeUpdateProfileView(ModuleMixin, UpdateView):
    model = Referee
    template_name = 'Referee/profile.html'
    form_class = RefereeForm
    success_url = reverse_lazy('dashboard')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.request.user.Referee

    def get_form(self, form_class=None):
        instance = self.object
        form = RefereeForm(instance=instance, initial={
            'first_name': instance.user.first_name,
            'last_name': instance.user.last_name,
            'dni': instance.user.dni,
            'email': instance.user.email,
            'image': instance.user.image,
        })
        return form

    def validate_data(self):
        data = {'valid': True}
        try:
            instance = self.object
            type = self.request.POST['type']
            obj = self.request.POST['obj'].strip()
            if type == 'dni':
                if User.objects.filter(dni=obj).exclude(id=instance.user.id):
                    data['valid'] = False
            elif type == 'mobile':
                if Referee.objects.filter(mobile=obj).exclude(id=instance.id):
                    data['valid'] = False
            elif type == 'email':
                if User.objects.filter(email=obj).exclude(id=instance.user.id):
                    data['valid'] = False
        except:
            pass
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'edit':
                with transaction.atomic():
                    instance = self.object
                    user = instance.user
                    user.first_name = request.POST['first_name']
                    user.last_name = request.POST['last_name']
                    user.dni = request.POST['dni']
                    user.username = user.dni
                    if 'image-clear' in request.POST:
                        user.remove_image()
                        user.image = None
                    if 'image' in request.FILES:
                        user.image = request.FILES['image']
                    user.email = request.POST['email']
                    user.save()

                    Referee = instance
                    Referee.user_id = user.id
                    Referee.gender = request.POST['gender']
                    Referee.mobile = request.POST['mobile']
                    Referee.phone = request.POST['phone']
                    Referee.address = request.POST['address']
                    Referee.birthdate = request.POST['birthdate']
                    Referee.parish_id = int(request.POST['parish'])
                    Referee.profession_id = int(request.POST['profession'])
                    if 'curriculum-clear' in request.POST:
                        Referee.remove_curriculum()
                        Referee.curriculum = None
                    if 'curriculum' in request.FILES:
                        Referee.curriculum = request.FILES['curriculum']
                    Referee.save()
            elif action == 'validate_data':
                return self.validate_data()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Edición de Perfil'
        context['action'] = 'edit'
        context['instance'] = self.object
        return context
