from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

# Register your models here.


admin.site.register(RedesSocialesUsuario)
admin.site.register(Oferta)
admin.site.register(TipoDeOferta)
admin.site.register(AplicacionOferta)



class MyAdmin(UserAdmin):
    model = Usuario

    fieldsets = UserAdmin.fieldsets + (
        (
            None,
            {
                "fields": (
                    "biografia",
                    "foto_perfil",
                    "rol",
                    
                    "num_trabajos",
                    "puntuacion_promedio",
                )
            },
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            None,
            {
                "fields": (
                    "biografia",
                    "foto_perfil",
                    "rol",
                    
                    "num_trabajos",
                    "puntuacion_promedio",
                )
            },
        ),
    )


# Registra el Admin
admin.site.register(Usuario, MyAdmin)