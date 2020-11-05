from django.contrib import admin

# Register your models here.
from .models import Empleado, Habilidades

admin.site.register(Habilidades)


class EmpleadoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'first_name',
        'last_name',
        'departamento',
        'job',
        'full_name',  # columna extra
    )

    def full_name(self, obj):
        return obj.first_name + ' ' + obj.last_name

    search_fields = ('first_name',)
    list_filter = ('job', 'departamento',)

    # solo funciona para muchos a muchos
    filter_horizontal = ('habilidades',)

    # ordenar por id
    ordering = ('id',)


admin.site.register(Empleado, EmpleadoAdmin)
