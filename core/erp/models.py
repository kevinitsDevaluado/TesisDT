import os
from django.db import models
from django.forms import model_to_dict
from datetime import datetime
from config import settings
from core.user.models import User
from core.erp.choices import *


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    gender = models.CharField(max_length=10, choices=gender_person, default=gender_person[0][0], verbose_name='Sexo')
    mobile = models.CharField(max_length=10, unique=True, verbose_name='Teléfono celular')
    phone = models.CharField(max_length=10, null=True, blank=True, verbose_name='Teléfono convencional')
    address = models.CharField(max_length=500, null=True, blank=True, verbose_name='Dirección')
    birthdate = models.DateField(default=datetime.now, verbose_name='Fecha de nacimiento')

    def __str__(self):
        return '{} / {}'.format(self.user.get_full_name(), self.user.dni)

    def toJSON(self):
        item = model_to_dict(self)
        item['user'] = self.user.toJSON()
        item['birthdate'] = self.birthdate.strftime('%Y-%m-%d')
        item['gender'] = {'id': self.gender, 'name': self.get_gender_display()}
        return item

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['-id']

class SportLeague(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre')
    desc = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')
    image = models.ImageField(upload_to='SportLeague/%Y/%m/%d', verbose_name='Imagen', null=True, blank=True)
    coordinates = models.CharField(verbose_name='Coordenadas', max_length=50, blank=True, null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True, default='',related_name='clientSportLegue')
    state = models.BooleanField(default=True, verbose_name='Estado')

    def __str__(self):
        return self.name

    def get_image(self):
        if self.image:
            return '{}{}'.format(settings.MEDIA_URL, self.image)
        return '{}{}'.format(settings.STATIC_URL, 'img/default/empty.png')

    def toJSON(self):
        item = model_to_dict(self)
        item['client'] = {} if self.client is None else self.client.toJSON()
        item['image'] = self.get_image()
        return item

    class Meta:
        verbose_name = 'Liga Deportiva'
        verbose_name_plural = 'Ligas Deportivas'
        ordering = ['-id']

class Stadium(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre')
    desc = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')
    image = models.ImageField(upload_to='Stadium/%Y/%m/%d', verbose_name='Imagen', null=True, blank=True)
    coordinates = models.CharField(verbose_name='Coordenadas', max_length=50, blank=True, null=True)
    sportLeague = models.ForeignKey(SportLeague, on_delete=models.CASCADE)
    state = models.BooleanField(default=True, verbose_name='Estado')

    def __str__(self):
        return self.name

    def get_latitude(self):
        return self.coordinates.split(',')[0].replace(',', '.')

    def get_longitude(self):
        return self.coordinates.split(',')[1].replace(',', '.')

    def get_image(self):
        if self.image:
            return '{}{}'.format(settings.MEDIA_URL, self.image)
        return '{}{}'.format(settings.STATIC_URL, 'img/default/empty.png')

    def toJSON(self):
        item = model_to_dict(self)
        item['image'] = self.get_image()
        return item

    def delete(self, using=None, keep_parents=False):
        try:
            os.remove(self.image.path)
        except:
            pass
        super(Stadium, self).delete()

    class Meta:
        verbose_name = 'Estadio'
        verbose_name_plural = 'Estadios'
        ordering = ['-id']


class Team(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre')
    category = models.CharField(max_length=150, verbose_name='Nombre', default="Senior")
    desc = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')
    image = models.ImageField(upload_to='Stadium/%Y/%m/%d', verbose_name='Imagen', null=True, blank=True)
    sportLeague = models.ForeignKey(SportLeague, on_delete=models.CASCADE)
    state = models.BooleanField(default=True, verbose_name='Estado')

    def __str__(self):
        return self.name

    def get_image(self):
        if self.image:
            return '{}{}'.format(settings.MEDIA_URL, self.image)
        return '{}{}'.format(settings.STATIC_URL, 'img/default/empty.png')

    def toJSON(self):
        item = model_to_dict(self)
        item['image'] = self.get_image()
        return item

    class Meta:
        verbose_name = 'Equipo de Futbol'
        verbose_name_plural = 'Equipos de Futbol'
        ordering = ['-id']

class Referee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, choices=gender_person, default=gender_person[0][0], verbose_name='Sexo')
    mobile = models.CharField(max_length=10, unique=True, verbose_name='Teléfono celular')
    typeReferee = models.CharField(max_length=200, choices=type_referee, default=type_referee[0][0], verbose_name='Tipo de Árbitro')
    phone = models.CharField(max_length=10, null=True, blank=True, verbose_name='Teléfono convencional')
    address = models.CharField(max_length=500, null=True, blank=True, verbose_name='Dirección')
    birthdate = models.DateField(default=datetime.now, verbose_name='Fecha de nacimiento')
    curriculum = models.FileField(upload_to='curriculum/%Y/%m/%d', null=True, blank=True)

    def __str__(self):
        return '{} / {}'.format(self.user.get_full_name(), self.user.dni)

    def get_curriculum(self):
        if self.curriculum:
            return '{}{}'.format(settings.MEDIA_URL, self.curriculum)
        return ''

    def remove_curriculum(self):
        try:
            if self.curriculum:
                os.remove(self.curriculum.path)
        except:
            pass

    def toJSON(self):
        item = model_to_dict(self, exclude=[])
        item['user'] = {} if self.user is None else self.user.toJSON()
        item['gender'] = {'id': self.gender, 'name': self.get_gender_display()}
        item['birthdate'] = self.birthdate.strftime('%Y-%m-%d')
        item['curriculum'] = self.get_curriculum()
        return item

    class Meta:
        verbose_name = 'Arbitro'
        verbose_name_plural = 'Arbitros'
        ordering = ['-id']

class GameFootball(models.Model):
    referee = models.ForeignKey(Referee, on_delete=models.CASCADE,related_name='referee')
    refereeAssistantOne = models.ForeignKey(Referee, on_delete=models.CASCADE, null=True, blank=True,related_name='refereeAssistantOne')
    refereeAssistantTwo = models.ForeignKey(Referee, on_delete=models.CASCADE, null=True, blank=True,related_name='refereeAssistantTwo')
    teamLocal = models.ForeignKey(Team, on_delete=models.CASCADE,related_name='teamLocal')
    teamVisitor = models.ForeignKey(Team, on_delete=models.CASCADE,related_name='teamVisitor')
    stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE,related_name='stadium')
    dateGame = models.DateField(default=datetime.now, verbose_name='Fecha del Partido')
    hourGame = models.TimeField(default=datetime.now().strftime("%H:%M"), verbose_name='Hora del Partido')
    desc = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    typeOfGame = models.CharField(max_length=200, choices=type_game, default=type_game[0][0], verbose_name='Tipo de Encuentro')
    state = models.BooleanField(default=True, verbose_name='Estado')

    def __str__(self):
        return self.name

    def get_image(self):
        if self.image:
            return '{}{}'.format(settings.MEDIA_URL, self.image)
        return '{}{}'.format(settings.STATIC_URL, 'img/default/empty.png')

    def toJSON(self):
        item = model_to_dict(self)
        item['referee'] = {} if self.referee is None else self.referee.toJSON()
        item['refereeAssistantOne'] = {} if self.refereeAssistantOne is None else self.refereeAssistantOne.toJSON()
        item['refereeAssistantTwo'] = {} if self.refereeAssistantTwo is None else self.refereeAssistantTwo.toJSON()
        item['teamLocal'] = {} if self.teamLocal is None else self.teamLocal.toJSON()
        item['teamVisitor'] = {} if self.teamVisitor is None else self.teamVisitor.toJSON()
        item['stadium'] = {} if self.stadium is None else self.stadium.toJSON()
        item['price'] = format(self.price, '.2f')
        item['dateGame'] = self.dateGame.strftime('%Y-%m-%d')
        item['hourGame'] = self.hourGame.strftime('%H:%M')
        return item

    def delete(self, using=None, keep_parents=False):
        try:
            os.remove(self.image.path)
        except:
            pass
        super(GameFootball, self).delete()

    class Meta:
        verbose_name = 'Partido de Futbol'
        verbose_name_plural = 'Partidos de Futbol'
        ordering = ['-id']


class Training(models.Model):
    desc = models.CharField(max_length=150, verbose_name='Descripción')
    date = models.DateField(default=datetime.now, verbose_name='Fecha del Entrenamiento')
    state = models.BooleanField(default=True, verbose_name='Estado')

    def __str__(self):
        return self.desc

    def toJSON(self):
        item = model_to_dict(self)
        item['date'] = self.date.strftime('%Y-%m-%d')
        return item

    class Meta:
        verbose_name = 'Entrenamiento'
        verbose_name_plural = 'Entrenamientos'
        ordering = ['-id']


class TrainingAssistance(models.Model):
    asistencia = models.BooleanField(default=False, verbose_name='Asistencia')
    creada_en = models.DateField(default=datetime.now, verbose_name='Fecha del Entrenamiento')
    referee = models.ForeignKey(Referee, on_delete=models.CASCADE,related_name='refereeAssistance')
    training = models.ForeignKey(Training, on_delete=models.CASCADE,related_name='training')
    state = models.BooleanField(default=True, verbose_name='Estado')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        item['referee'] = {} if self.referee is None else self.referee.toJSON()
        item['training'] = {} if self.training is None else self.training.toJSON()
        item['creada_en'] = self.creada_en.strftime('%Y-%m-%d')
        return item

    class Meta:
        verbose_name = 'Asistencia de Entrenamiento'
        verbose_name_plural = 'Asistencias de Entrenamientos'
        ordering = ['-id']

class Quote(models.Model):
    desc = models.CharField(max_length=150, verbose_name='Descripción')
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    date = models.DateField(default=datetime.now, verbose_name='Fecha de la cuota')
    state = models.BooleanField(default=True, verbose_name='Estado')

    def __str__(self):
        return self.desc

    def toJSON(self):
        item = model_to_dict(self)
        item['price'] = format(self.price, '.2f')
        return item

    class Meta:
        verbose_name = 'Cuota'
        verbose_name_plural = 'Cuotas'
        ordering = ['-id']


class DebtReferee(models.Model):
    referee = models.ForeignKey(Referee, on_delete=models.CASCADE,related_name='refereeDebts')
    cuota = models.ForeignKey(Quote, on_delete=models.CASCADE,related_name='QuoteDebt')
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    date = models.DateField(default=datetime.now, verbose_name='Fecha de la deuda')
    state = models.BooleanField(default=True, verbose_name='Estado')

    def __str__(self):
        return self.price

    def toJSON(self):
        item = model_to_dict(self)
        item['referee'] = {} if self.referee is None else self.referee.toJSON()
        item['cuota'] = {} if self.cuota is None else self.cuota.toJSON()
        item['price'] = format(self.price, '.2f')
        return item

    class Meta:
        verbose_name = 'Deuda'
        verbose_name_plural = 'Deudas'
        ordering = ['-id']

class DebtRepayment(models.Model):
    deuda = models.ForeignKey(DebtReferee, on_delete=models.CASCADE,related_name='Quote')
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    date = models.DateField(default=datetime.now, verbose_name='Fecha de la deuda')
    state = models.BooleanField(default=True, verbose_name='Estado')

    def __str__(self):
        return self.price

    def toJSON(self):
        item = model_to_dict(self)
        item['deuda'] = {} if self.deuda is None else self.deuda.toJSON()
        item['price'] = format(self.price, '.2f')
        return item

    class Meta:
        verbose_name = 'Deuda Avance'
        verbose_name_plural = 'Deudas Avances'
        ordering = ['-id']

class DetailsGames(models.Model):
    game = models.ForeignKey(GameFootball, on_delete=models.CASCADE,related_name='DetailGame')
    desc = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')
    archivo = models.FileField(upload_to='archivos/%Y/%m/%d', blank=True, null=True)
    state = models.BooleanField(default=True, verbose_name='Estado')

    def __str__(self):
        return self.desc

    def toJSON(self):
        item = model_to_dict(self)
        item['game'] = {} if self.game is None else self.game.toJSON()
        return item

    class Meta:
        verbose_name = 'Detalles de juegos'
        verbose_name_plural = 'Detalles de juegos'
        ordering = ['-id']



