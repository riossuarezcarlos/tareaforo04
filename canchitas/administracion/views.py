from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from .models import TipoCanchaModel, LocalModel, CanchaModel, Usuario, TipoClienteModel, ClienteModel, ReservaModel
from .serializers import TipoCanchaSerializer, LocalSerializer, CanchaSerializer, UsuarioRegistroSerializer, LoginSerializer, TipoClienteSerializer, ClienteSerializer, ReservaSerializer

from rest_framework.permissions import  IsAuthenticated


# Vista para Login y Registro

class RegistroView(CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioRegistroSerializer
    def post(self, request):
        # Validar que no exista un usuario con ese correo
        correo = request.data.get('usuCorreo')

        usuarios = self.get_queryset().filter(usuCorreo=correo).first()
        if usuarios:
            return Response({
                'ok': False,
                'message': 'El usuario con el correo {} ya existe'.format(correo,)
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            respuesta = self.get_serializer(data=request.data)
            if respuesta.is_valid(raise_exception=True):
                resultado = respuesta.save()
                return Response({
                    'ok': True,
                    'content': self.get_serializer(resultado).data,
                    'message': 'Usuario creado exitosamente'
                }, status=201)
            else:
                return Response({
                    'ok': False,
                    'message': 'Data incorrecta'
                }, status=status.HTTP_400_BAD_REQUEST)

class LoginView(CreateAPIView):
    serializer_class = LoginSerializer
    def post(self, request):
        serializador = self.get_serializer(data=request.data)
        serializador.is_valid(raise_exception=True)
        return Response({
            'ok': True,
            'content': serializador.data
        })



# Create your views here.

class TipoCanchasView(ListCreateAPIView):
    queryset = TipoCanchaModel.objects.all()
    serializer_class = TipoCanchaSerializer
    permission_classes = (IsAuthenticated, )
    def get(self, request):
        respuesta = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            'ok': True,
            'content': respuesta.data,
            'message': None
        })

    def post(self, request):
        print(request.data)
        respuesta = self.get_serializer(data=request.data)
        if respuesta.is_valid(raise_exception=True):
            # Registrar en la BD
            respuesta.save()
            return Response({
                'ok': True,
                'content': respuesta.data,
                'message': None
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'ok': False,
                'content': None,
                'message': "Ocurrió un erro al crear el Tipo Cancha"
            }, status=status.HTTP_400_BAD_REQUEST)

class TipoCanchaView(RetrieveUpdateDestroyAPIView):
    serializer_class = TipoCanchaSerializer
    queryset =  TipoCanchaModel.objects.all()
    permission_classes = (IsAuthenticated, )
    def get(self, request, tipoCanchaId):
        # el get devuelve todas las coincidencias, mediante un filtro
        # Devuelve la primera coincidencia
        print(self.get_queryset().filter(tipoCanchaId=tipoCanchaId))
        print(self.get_queryset().get(tipoCanchaId=tipoCanchaId))

        respuesta = self.get_serializer(self.get_queryset().get(tipoCanchaId=tipoCanchaId))
        
        return Response({
            'ok': True,
            'content': respuesta.data,
            'message': None
        })

    def put(self, request, tipoCanchaId):
        respuesta = self.serializer_class(self.get_queryset().get(tipoCanchaId=tipoCanchaId), data=request.data)
        if respuesta.is_valid():
            resultado = respuesta.update()
            return Response({
                'ok': True,
                'content': self.serializer_class(resultado).data,
                'message': None
            })
        else:
            return Response({
                'ok': False,
                'content': None,
                'message': 'Ocurrió un error en la actualización'
            })


    def delete(self, request, tipoCanchaId):
        respuesta = self.get_serializer(self.get_queryset().get(tipoCanchaId=tipoCanchaId))
        print(respuesta)
        if respuesta:
            resultado = respuesta.delete()
            return Response({
                'ok': True,
                'content': self.serializer_class(resultado).data,
                'message': 'Se deshanilitó el tipo de cancha'
            }, status=status.HTTP_200_OK)


class LocalesView(ListCreateAPIView):
    queryset = LocalModel.objects.all()
    serializer_class = LocalSerializer
    permission_classes = (IsAuthenticated, )
    def get(self, request):
        respuesta = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            'ok': True,
            'content': respuesta.data,
            'message': None
        })

    def post(self, request):
        print(request.data)
        respuesta = self.get_serializer(data=request.data)
        if respuesta.is_valid(raise_exception=True):
            # Registrar en la BD
            respuesta.save()
            return Response({
                'ok': True,
                'content': respuesta.data,
                'message': None
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'ok': False,
                'content': None,
                'message': "Ocurrió un error al crear el Local"
            }, status=status.HTTP_400_BAD_REQUEST)

class LocalView(RetrieveUpdateDestroyAPIView):
    serializer_class = LocalSerializer
    queryset =  LocalModel.objects.all()
    permission_classes = (IsAuthenticated, )
    def get(self, request, localId):
        respuesta = self.get_serializer(self.get_queryset().get(localId=localId))        
        return Response({
            'ok': True,
            'content': respuesta.data,
            'message': None
        })

    def put(self, request, localId):
        respuesta = self.serializer_class(self.get_queryset().get(localId=localId), data=request.data)
        if respuesta.is_valid():
            resultado = respuesta.update()
            return Response({
                'ok': True,
                'content': self.serializer_class(resultado).data,
                'message': None
            })
        else:
            return Response({
                'ok': False,
                'content': None,
                'message': 'Ocurrió un error en la actualización'
            }) 

    def delete(self, request, localId):
        respuesta = self.get_serializer(self.get_queryset().get(localId=localId))
        if respuesta:
            resultado = respuesta.delete()
            return Response({
                'ok': True,
                'content': self.serializer_class(resultado).data,
                'message': 'Se deshanilitó el local'
            }, status=status.HTTP_200_OK)

class CanchasView(ListCreateAPIView):
    queryset = CanchaModel.objects.all()
    serializer_class = CanchaSerializer
    permission_classes = (IsAuthenticated, )
    def get(self, request):
        respuesta = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            'ok': True,
            'content': respuesta.data,
            'message': None
        })

    def post(self, request):
        respuesta = self.get_serializer(data=request.data)
        if respuesta.is_valid(raise_exception=True):
            # Registrar en la BD
            respuesta.save()
            return Response({
                'ok': True,
                'content': respuesta.data,
                'message': None
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'ok': False,
                'content': None,
                'message': "Ocurrió un error al crear la cancha"
            }, status=status.HTTP_400_BAD_REQUEST)

class CanchaView(RetrieveUpdateDestroyAPIView):
    serializer_class = CanchaSerializer
    queryset =  CanchaModel.objects.all()
    permission_classes = (IsAuthenticated, )
    def get(self, request, canchaId):
        respuesta = self.get_serializer(self.get_queryset().get(canchaId=canchaId))        
        return Response({
            'ok': True,
            'content': respuesta.data,
            'message': None
        })

    def put(self, request, canchaId):
        respuesta = self.serializer_class(self.get_queryset().get(canchaId=canchaId), data=request.data)
        if respuesta.is_valid():
            resultado = respuesta.update()
            return Response({
                'ok': True,
                'content': self.serializer_class(resultado).data,
                'message': None
            })
        else:
            return Response({
                'ok': False,
                'content': None,
                'message': 'Ocurrió un error en la actualización'
            }) 

    def delete(self, request, canchaId):
        respuesta = self.get_serializer(self.get_queryset().get(canchaId=canchaId))
        if respuesta:
            resultado = respuesta.delete()
            return Response({
                'ok': True,
                'content': self.serializer_class(resultado).data,
                'message': 'Se deshanilitó la cancha'
            }, status=status.HTTP_200_OK)

class TipoClientesView(ListCreateAPIView):
    queryset = TipoClienteModel.objects.all()
    serializer_class = TipoClienteSerializer
    permission_classes = (IsAuthenticated, )
    def get(self, request):
        respuesta = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            'ok': True,
            'content': respuesta.data,
            'message': None
        })

    def post(self, request):
        print(request.data)
        respuesta = self.get_serializer(data=request.data)
        if respuesta.is_valid(raise_exception=True):
            # Registrar en la BD
            respuesta.save()
            return Response({
                'ok': True,
                'content': respuesta.data,
                'message': None
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'ok': False,
                'content': None,
                'message': "Ocurrió un erro al crear el Tipo Cliente"
            }, status=status.HTTP_400_BAD_REQUEST)

class TipoClienteView(RetrieveUpdateDestroyAPIView):
    serializer_class = TipoClienteSerializer
    queryset =  TipoClienteModel.objects.all()
    permission_classes = (IsAuthenticated, )
    def get(self, request, tipoClienteId):
        # el get devuelve todas las coincidencias, mediante un filtro
        # Devuelve la primera coincidencia
        print(self.get_queryset().filter(tipoClienteId=tipoClienteId))
        print(self.get_queryset().get(tipoClienteId=tipoClienteId))

        respuesta = self.get_serializer(self.get_queryset().get(tipoClienteId=tipoClienteId))
        
        return Response({
            'ok': True,
            'content': respuesta.data,
            'message': None
        })

    def put(self, request, tipoClienteId):
        respuesta = self.serializer_class(self.get_queryset().get(tipoClienteId=tipoClienteId), data=request.data)
        if respuesta.is_valid():
            resultado = respuesta.update()
            return Response({
                'ok': True,
                'content': self.serializer_class(resultado).data,
                'message': None
            })
        else:
            return Response({
                'ok': False,
                'content': None,
                'message': 'Ocurrió un error en la actualización'
            })


    def delete(self, request, tipoClienteId):
        respuesta = self.get_serializer(self.get_queryset().get(tipoClienteId=tipoClienteId))
        print(respuesta)
        if respuesta:
            resultado = respuesta.delete()
            return Response({
                'ok': True,
                'content': self.serializer_class(resultado).data,
                'message': 'Se deshanilitó el tipo de Cliente'
            }, status=status.HTTP_200_OK)


class ClientesView(ListCreateAPIView):
    queryset = ClienteModel.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = (IsAuthenticated, )
    def get(self, request):
        respuesta = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            'ok': True,
            'content': respuesta.data,
            'message': None
        })

    def post(self, request):
        respuesta = self.get_serializer(data=request.data)
        if respuesta.is_valid(raise_exception=True):
            # Registrar en la BD
            respuesta.save()
            return Response({
                'ok': True,
                'content': respuesta.data,
                'message': None
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'ok': False,
                'content': None,
                'message': "Ocurrió un error al crear la Cliente"
            }, status=status.HTTP_400_BAD_REQUEST)

class ClienteView(RetrieveUpdateDestroyAPIView):
    serializer_class = ClienteSerializer
    queryset =  ClienteModel.objects.all()
    permission_classes = (IsAuthenticated, )
    def get(self, request, clienteId):
        respuesta = self.get_serializer(self.get_queryset().get(clienteId=clienteId))        
        return Response({
            'ok': True,
            'content': respuesta.data,
            'message': None
        })

    def put(self, request, clienteId):
        respuesta = self.serializer_class(self.get_queryset().get(clienteId=clienteId), data=request.data)
        if respuesta.is_valid():
            resultado = respuesta.update()
            return Response({
                'ok': True,
                'content': self.serializer_class(resultado).data,
                'message': None
            })
        else:
            return Response({
                'ok': False,
                'content': None,
                'message': 'Ocurrió un error en la actualización'
            }) 

    def delete(self, request, clienteId):
        respuesta = self.get_serializer(self.get_queryset().get(clienteId=clienteId))
        if respuesta:
            resultado = respuesta.delete()
            return Response({
                'ok': True,
                'content': self.serializer_class(resultado).data,
                'message': 'Se deshanilitó la Cliente'
            }, status=status.HTTP_200_OK)

class ReservasView(ListCreateAPIView):
    queryset = ReservaModel.objects.all()
    serializer_class = ReservaSerializer
    permission_classes = (IsAuthenticated, )
    def get(self, request):
        respuesta = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            'ok': True,
            'content': respuesta.data,
            'message': None
        })

    def post(self, request):
        respuesta = self.get_serializer(data=request.data)
        if respuesta.is_valid(raise_exception=True):
            # Registrar en la BD
            respuesta.save()
            return Response({
                'ok': True,
                'content': respuesta.data,
                'message': None
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'ok': False,
                'content': None,
                'message': "Ocurrió un error al crear la Reserva"
            }, status=status.HTTP_400_BAD_REQUEST)

class ReservaView(RetrieveUpdateDestroyAPIView):
    serializer_class = ReservaSerializer
    queryset =  ReservaModel.objects.all()
    permission_classes = (IsAuthenticated, )
    def get(self, request, reservaId):
        respuesta = self.get_serializer(self.get_queryset().get(reservaId=reservaId))        
        return Response({
            'ok': True,
            'content': respuesta.data,
            'message': None
        })

    def put(self, request, reservaId):
        print(reservaId)
        respuesta = self.serializer_class(self.get_queryset().get(reservaId=reservaId), data=request.data)
        if respuesta.is_valid():
            resultado = respuesta.update()
            return Response({
                'ok': True,
                'content': self.serializer_class(resultado).data,
                'message': None
            })
        else:
            return Response({
                'ok': False,
                'content': None,
                'message': 'Ocurrió un error en la actualización'
            }) 

    def delete(self, request, reservaId):
        respuesta = self.get_serializer(self.get_queryset().get(reservaId=reservaId))
        if respuesta:
            resultado = respuesta.delete()
            return Response({
                'ok': True,
                'content': self.serializer_class(resultado).data,
                'message': 'Se deshanilitó la Reserva'
            }, status=status.HTTP_200_OK)