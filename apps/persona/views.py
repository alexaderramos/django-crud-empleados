from django.shortcuts import render

from django.views.generic import (
    ListView,
    DetailView,
    CreateView, TemplateView, UpdateView, DeleteView
)

from django.urls import reverse_lazy

# models
from .models import Empleado

#forms
from .forms import EmpleadoForm


class InicioView(TemplateView):
    """ Vista que carga la pagina de inicio """
    template_name = 'inicio.html'


# 1.- Listar todos los empleados de la empresa
class ListAllEmpleados(ListView):
    template_name = 'persona/list_all.html'
    paginate_by = 5
    ordering = 'id'
    context_object_name = 'empleados'

    def get_queryset(self):
        palabra_clave = self.request.GET.get("kword", '')
        lista = Empleado.objects.filter(
            first_name__icontains=palabra_clave  # como like en mysql
        )
        return lista


# 1.- Listar todos los empleados de la empresa para administrar
class ListaEmpleadosAdmin(ListView):
    template_name = 'persona/lista_empleados.html'
    paginate_by = 10
    ordering = 'id'
    model = Empleado
    context_object_name = 'empleados'


# 2.- Listar todos los empleados que pertenecen a un area
class ListByAreaEmpleado(ListView):
    template_name = 'persona/list_by_area.html'
    model = Empleado
    context_object_name = 'empleados'

    # para aplicar filtros
    # queryset = Empleado.objects.filter(
    #    departamento__name='Contabilidad'
    # )
    def get_queryset(self):
        area = self.kwargs['shorname']
        lista = Empleado.objects.filter(
            departamento__shor_name=area  # 'Contabilidad'
        )
        return lista


# 4.- Listar habilidades de un empleado
class ListEmpleadosByKword(ListView):
    template_name = 'persona/by_kword.html'
    context_object_name = 'empleados'

    def get_queryset(self):
        print('****************')
        palabra_clave = self.request.GET.get('kword', '')
        print(f'======= {palabra_clave}')
        lista = Empleado.objects.filter(
            first_name=palabra_clave  # 'Contabilidad'
        )
        print(lista)
        return lista

    # listar habilidades de empleado


class ListHabilidadesEmpleado(ListView):
    template_name = 'persona/habilidades.html'
    context_object_name = 'habilidades'

    def get_queryset(self):
        empleado = Empleado.objects.get(id=1)
        print(empleado.habilidades.all())  # many to many
        return empleado.habilidades.all()


# 3.- Listar los empleados por el trabajo


"""
    Usando DetailView
"""


class EmpleadoDetailView(DetailView):
    template_name = 'persona/detail-empleado.html'
    model = Empleado
    context_object_name = 'empleado'

    # agregar atributos al context
    def get_context_data(self, **kwargs):
        context = super(EmpleadoDetailView, self).get_context_data(**kwargs)
        # aqui t odo el preoceso
        context['titulo'] = 'Empleado del mes'
        return context


"""
    Usando CreateView
"""


class SuccessView(TemplateView):
    template_name = 'persona/success.html'


class EmpleadoCreateView(CreateView):
    template_name = 'persona/add.html'
    model = Empleado
    form_class = EmpleadoForm
    # fields = [
    #     'first_name',
    #     'last_name',
    #     'job',
    #     'departamento',
    #     'habilidades',
    #     'avatar'
    # ]  # '__all__'
    # success_url = '/success'  # redirección no recomendadq
    success_url = reverse_lazy('persona_app:empleados_admin')  # recomendado para usar

    def form_valid(self, form):
        # LOGICA DE PROCESO NO OPTIMA
        empleado = form.save(commit=False)  # guarda los datos en la base de datos
        print(empleado)
        empleado.full_name = empleado.first_name + ' ' + empleado.last_name
        empleado.save()
        return super(EmpleadoCreateView, self).form_valid(form)


"""
    UpdateView
"""


class EmpleadoUpdateView(UpdateView):
    model = Empleado
    template_name = 'persona/update.html'
    fields = [
        'first_name',
        'last_name',
        'job',
        'departamento',
        'habilidades',
    ]  # '__all__'
    success_url = reverse_lazy('persona_app:empleados_admin')  # recomendado para usar

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        print('******** METODO POST ************')
        print('************************')
        print(request.POST)
        print(request.POST['last_name'])
        return super(EmpleadoUpdateView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        print('******** METODO FORM VALID ************')
        print('************************')
        empleado = form.save(commit=False)  # no guarda los datos en la base de datos
        print(empleado)
        empleado.full_name = empleado.first_name + ' ' + empleado.last_name
        empleado.save()
        return super(EmpleadoUpdateView, self).form_valid(form)


"""
    DeleteView
"""


class EmpleadoDeleteView(DeleteView):
    model = Empleado
    template_name = 'persona/delete.html'
    success_url = reverse_lazy('persona_app:empleados_admin')  # recomendado para usar
