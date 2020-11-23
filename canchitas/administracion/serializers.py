from rest_framework import serializers
from .models import TipoCanchaModel, LocalModel, CanchaModel, Usuario, TipoClienteModel, ClienteModel, ReservaModel
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
 
class LocalSerializer(serializers.ModelSerializer):
    # canchas = CanchaSerializer(source='canchasLocal', many= True, read_only=True)
    class Meta:
        model = LocalModel
        # Se usa fields o exclude
        fields = '__all__'
        # exclude = ['createdAt']

    def update(self):
        self.instance.localNomb = self.validated_data.get('localNomb', self.instance.localNomb)
        self.instance.localDir = self.validated_data.get('localDir', self.instance.localDir)
        self.instance.save()
        return self.instance

    def delete(self):
        self.instance.estado = False
        self.instance.save()
        return self.instance

class CanchaSerializer(serializers.ModelSerializer):
    local = LocalSerializer(source='localId', read_only=True)
    class Meta:
        model = CanchaModel
        # Se usa fields o exclude
        fields = '__all__'
        # exclude = ['createdAt']

    def update(self):
        self.instance.canchaDesc = self.validated_data.get('canchaDesc', self.instance.canchaDesc)
        self.instance.canchaPrecio = self.validated_data.get('canchaPrecio', self.instance.canchaPrecio)

        self.instance.tipocanchaId = self.validated_data.get('tipocanchaId', self.instance.tipocanchaId)
        self.instance.localId = self.validated_data.get('localId', self.instance.canchaPrecio)

        self.instance.save()
        return self.instance

    def delete(self):
        self.instance.estado = False
        self.instance.save()
        return self.instance


  
class TipoCanchaSerializer(serializers.ModelSerializer):
    canchas = CanchaSerializer(source='canchasTipoCancha', many= True, read_only=True)
    class Meta:
        model = TipoCanchaModel
        # Se usa fields o exclude
        fields = '__all__'
        # exclude = ['createdAt']
    
    def update(self):
        self.instance.tipoCanchaDesc = self.validated_data.get('tipoCanchaDesc', self.instance.tipoCanchaDesc)
        self.instance.save()
        return self.instance

    def delete(self):
        self.instance.estado = False
        self.instance.save()
        return self.instance

class ClienteSerializer(serializers.ModelSerializer): 
    class Meta:
        model = ClienteModel
        # Se usa fields o exclude
        fields = '__all__'
        # exclude = ['createdAt']
    
    def update(self):
        self.instance.clienteNomb = self.validated_data.get('clienteNomb', self.instance.clienteNomb)
        self.instance.clienteCel = self.validated_data.get('clienteCel', self.instance.clienteCel)

        self.instance.tipoclienteId = self.validated_data.get('tipoclienteId', self.instance.tipoclienteId)
        self.instance.save()
        return self.instance

    def delete(self):
        self.instance.estado = False
        self.instance.save()

        return self.instance

class TipoClienteSerializer(serializers.ModelSerializer):
    clientes = ClienteSerializer(source='clienteTipoCliente', many= True, read_only=True)
    class Meta:
        model = TipoClienteModel
        # Se usa fields o exclude
        fields = '__all__'
        # exclude = ['createdAt']
    
    def update(self):
        self.instance.tipoClienteDesc = self.validated_data.get('tipoClienteDesc', self.instance.tipoClienteDesc)
        self.instance.tipoClientePrecio = self.validated_data.get('tipoClientePrecio', self.instance.tipoClientePrecio)
        self.instance.save()
        return self.instance

    def delete(self):
        self.instance.estado = False
        self.instance.save()
        return self.instance 
        
class ReservaSerializer(serializers.ModelSerializer):
    # canchas = CanchaSerializer(source='canchasTipoCancha', many= True, read_only=True)
    class Meta:
        model = ReservaModel
        # Se usa fields o exclude
        fields = '__all__'
        # exclude = ['createdAt']
    
    def update(self):
        self.instance.reservaHoraInicio = self.validated_data.get('reservaHoraInicio', self.instance.reservaHoraInicio)
        self.instance.reservaHoraFin = self.validated_data.get('reservaHoraFin', self.instance.reservaHoraFin)
        self.instance.reservaPrecio = self.validated_data.get('reservaPrecio', self.instance.reservaPrecio)

        self.instance.canchaId = self.validated_data.get('canchaId', self.instance.canchaId)
        self.instance.clienteId = self.validated_data.get('clienteId', self.instance.clienteId)
        print('Guardar')
        self.instance.save()

        return self.instance

    def delete(self):
        self.instance.estado = False
        self.instance.save()
        return self.instance

class UsuarioRegistroSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = Usuario
        exclude = ['last_login']

    def save(self):
        password = self.validated_data.get('password')
        is_superuser = self.validated_data.get('is_superuser')
        usuCorreo = self.validated_data.get('usuCorreo')
        usuNombre = self.validated_data.get('usuNombre')
        usuFono = self.validated_data.get('usuFono')
        usuCumple = self.validated_data.get('usuCumple')
        is_staff = self.validated_data.get('is_staff')

        nuevoUsuario = Usuario(is_superuser=is_superuser, usuCorreo=usuCorreo, usuNombre=usuNombre, usuFono=usuFono, usuCumple=usuCumple, is_staff=is_staff)
        nuevoUsuario.set_password(password)
        nuevoUsuario.save()
        return nuevoUsuario

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=50, min_length=5)
    password = serializers.CharField(max_length=50, min_length=6, write_only=True)
    class Meta:
        model = Usuario
        fields = ['email','password', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email','')
        password = attrs.get('password','')
        usuario = auth.authenticate(usuCorreo=email, password=password)
        if not usuario:
            raise AuthenticationFailed('Credenciales invalidas, intentelo de nuevo')
        return {
            'email': usuario.usuCorreo,
            'tokens': usuario.tokens()
        }