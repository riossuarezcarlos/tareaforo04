from django.urls import path
from .views import TipoCanchasView, TipoCanchaView, LocalesView, LocalView, CanchasView, CanchaView, RegistroView, LoginView, TipoClientesView, TipoClienteView, ClientesView, ClienteView, ReservasView, ReservaView

urlpatterns = [
    path('tipocancha', TipoCanchasView.as_view(), name="TipoCancha"),
    path('tipocancha/<int:tipoCanchaId>', TipoCanchaView.as_view()),
    path('local', LocalesView.as_view(), name="Local"),
    path('local/<int:localId>', LocalView.as_view()),
    path('cancha', CanchasView.as_view(), name="Cancha"),
    path('cancha/<int:canchaId>', CanchaView.as_view()),
    path('tipocliente', TipoClientesView.as_view(), name="TipoCliente"),
    path('tipocliente/<int:tipoClienteId>', TipoClienteView.as_view()),
    path('cliente', ClientesView.as_view(), name="Cliente"),
    path('cliente/<int:clienteId>', ClienteView.as_view()),

    path('reserva', ReservasView.as_view(), name="Reserva"),
    path('reserva/<int:reservaId>', ReservaView.as_view()),

    path('registro', RegistroView.as_view()),
    path('login', LoginView.as_view()),
]