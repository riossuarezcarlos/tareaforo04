from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken

class ManejoUsuario(BaseUserManager):
    use_in_migrations = True
    def _create_user(self, usuCorreo, usuNombre, usuFono, usuPass, **extra_fields):
        values = [usuCorreo, usuFono, usuNombre]
        field_value_map = dict(zip(self.model.REQUIRED_FIELDS, values))
        for field_name, value in field_value_map.items():
            if not value:
                raise ValueError("El valor de {} debe estar definido".format(field_name))
        usuCorreo = self.normalize_email(usuCorreo)
        user = self.model(
            usuCorreo = usuCorreo,
            usuNombre=usuNombre,
            usuFono=usuFono,
            **extra_fields
        )
        user.set_password(usuPass)
        user.save(using=self._db)
        return user

    def create_user(self, usuCorreo, usuNombre, usuFono, usuPass=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser',False)
        return self._create_user(usuCorreo, usuNombre, usuFono, usuPass, **extra_fields)
    
    def create_superuser(self,  usuCorreo, usuNombre, usuFono, usuPass, **extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('El super usuario debe de ser staff')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El super usuario debe de ser superusuario')
        return self._create_user( usuCorreo, usuNombre, usuFono, usuPass, **extra_fields)



class Usuario(AbstractBaseUser, PermissionsMixin):
    usuId = models.AutoField(db_column='usu_id', primary_key=True)
    usuCorreo = models.EmailField(db_column='usu_correo', unique=True)
    usuNombre = models.CharField(db_column='usu_nombre', max_length=50)
    usuFono = models.CharField(db_column='usu_fono', max_length=15)
    usuCumple = models.DateField(db_column='usu_cumple', blank=True, null=True)
    password = models.TextField(db_column='usu_pass', null=True)
    # CAMPOS OBLIGATORIAMENTE EN INGLES y si o si tienen que ir
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    #

    date_joined = models.DateTimeField(default = timezone.now)
    last_login = models.DateTimeField(null=True)

    objects = ManejoUsuario()

    USERNAME_FIELD = 'usuCorreo'
    REQUIRED_FIELDS = ['usuNombre','usuFono']

    def tokens(self):
        tokens = RefreshToken.for_user(self)
        return{
            'acceso': str(tokens.access_token),
            'refresh': str(tokens)
        }

    class Meta:
        db_table = 't_usuario'
 

# Create your models here. 
# Crear modelo local
class LocalModel(models.Model):
    # Definir los atributos de la tabla
    # Si no se crear PK, Django crea la columna ID

    localId = models.AutoField(db_column='local_id', primary_key=True, null=False, unique=True)
    localNomb = models.CharField(db_column='local_nomb', max_length=50)
    localDir = models.CharField(db_column='local_dir', null=False, unique=True, max_length=100)
    estado = models.BooleanField(db_column='estado',null=False, default=True)
    # Campos para auditoria
    createAt = models.DateTimeField(db_column='created_at', auto_now_add=True)
    updateAt = models.DateTimeField(db_column='updated_at', auto_now=True)
    class Meta:
        db_table = 't_local'

class TipoCanchaModel(models.Model):
    tipoCanchaId = models.AutoField(db_column='tc_id', primary_key=True, null=False, unique=True)
    tipoCanchaDesc = models.CharField(db_column='tc_desc', max_length=50)
    # Para gestionar el eliminar
    estado = models.BooleanField(db_column='estado',null=False, default=True)
    createAt = models.DateTimeField(db_column='created_at', auto_now_add=True)
    updateAt = models.DateTimeField(db_column='updated_at', auto_now=True)
    class Meta:
        db_table = 't_tipocancha'

class CanchaModel(models.Model):
    canchaId = models.AutoField(db_column='cancha_id', primary_key=True, null=False, unique=True)
    canchaPrecio = models.DecimalField(db_column='cancha_prec', max_digits=5, decimal_places=2)
    canchaDesc = models.CharField(db_column='cancha_desc', max_length=50)
    # 
    tipocanchaId = models.ForeignKey(TipoCanchaModel, on_delete = models.PROTECT, db_column='tc_id', related_name='canchasTipoCancha')
    localId = models.ForeignKey(LocalModel, on_delete = models.PROTECT, db_column='local_id', related_name='canchasLocal')
    estado = models.BooleanField(db_column='estado',null=False, default=True)
    createAt = models.DateTimeField(db_column='created_at', auto_now_add=True)
    updateAt = models.DateTimeField(db_column='updated_at', auto_now=True)
    class Meta:
        db_table = 't_cancha'

class TipoClienteModel(models.Model):
    tipoClienteId = models.AutoField(db_column='tcli_id', primary_key=True, null=False, unique=True)
    tipoClienteDesc = models.CharField(db_column='tcli_desc', max_length=50)
    tipoClientePrecio = models.DecimalField(db_column='tcli_prec', max_digits=5, decimal_places=2)
    estado = models.BooleanField(db_column='estado',null=False, default=True)
    createAt = models.DateTimeField(db_column='created_at', auto_now_add=True)
    updateAt = models.DateTimeField(db_column='updated_at', auto_now=True)
    class Meta:
        db_table = 't_tipocliente'

class ClienteModel(models.Model):
    clienteId = models.AutoField(db_column='cli_id', primary_key=True, null=False, unique=True)
    clienteNomb = models.CharField(db_column='cli_nomb', max_length=50)
    clienteCel = models.CharField(db_column='cli_cel', max_length=12)
    # 
    tipoclienteId = models.ForeignKey(TipoClienteModel, on_delete = models.PROTECT, db_column='tcli_id', related_name='clienteTipoCliente')
    estado = models.BooleanField(db_column='estado',null=False, default=True)
    createAt = models.DateTimeField(db_column='created_at', auto_now_add=True)
    updateAt = models.DateTimeField(db_column='updated_at', auto_now=True)
    class Meta:
        db_table = 't_cliente'


class ReservaModel(models.Model):
    reservaId = models.AutoField(db_column='res_id', primary_key=True, null=False, unique=True)
    reservaHoraInicio = models.DateTimeField(db_column='res_inicio')
    reservaHoraFin = models.DateTimeField(db_column='res_fin')
    reservaPrecio = models.DecimalField(db_column='res_prec', max_digits=5, decimal_places=2)
    # 
    canchaId = models.ForeignKey(CanchaModel, on_delete = models.PROTECT, db_column='cancha_id', related_name='reservasCancha')
    clienteId = models.ForeignKey(ClienteModel, on_delete = models.PROTECT, db_column='cli_id', related_name='reservasCliente')
    estado = models.BooleanField(db_column='estado',null=False, default=True)
    createAt = models.DateTimeField(db_column='created_at', auto_now_add=True)
    updateAt = models.DateTimeField(db_column='updated_at', auto_now=True)
    class Meta:
        db_table = 't_reserva'