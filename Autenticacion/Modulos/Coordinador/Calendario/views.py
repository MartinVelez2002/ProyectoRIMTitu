from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from Modulos.Coordinador.Calendario.models import *
from Modulos.Coordinador.Calendario.forms import *
# Create your views here.

