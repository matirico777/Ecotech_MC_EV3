from dominio.validaciones import texto_obligatorio, correo_valido
import hashlib
import hmac
import secrets


class Usuario:
    def __init__(self, nombre, mail, contrasenia, empleado, id_usuario=None):
        self._id_usuario = id_usuario
        self._nombre = texto_obligatorio(nombre, "El nombre")
        self._mail = correo_valido(mail)
        if empleado is None:
            raise ValueError("El usuario debe estar asociado a un empleado.")
        if not isinstance(contrasenia, str) or len(contrasenia) < 8:
            raise ValueError("La contrasena debe tener al menos 8 caracteres.")
        self._empleado = empleado
        self._permisos = []
        self._contrasenia_hash = self._crear_hash(contrasenia)

    def _crear_hash(self, contrasenia):
        sal = secrets.token_bytes(16)
        resultado = hashlib.pbkdf2_hmac(
            "sha256", contrasenia.encode(), sal, 600000
        )
        return sal.hex() + ":" + resultado.hex()

    def autenticar(self, contrasenia):
        if not contrasenia:
            return False
        partes = self._contrasenia_hash.split(":")
        if len(partes) != 2:
            return False
        try:
            sal = bytes.fromhex(partes[0])
            hash_guardado = bytes.fromhex(partes[1])
        except ValueError:
            return False
        hash_ingresado = hashlib.pbkdf2_hmac(
            "sha256", contrasenia.encode(), sal, 600000
        )
        return hmac.compare_digest(hash_ingresado, hash_guardado)

    def cambiar_contrasenia(self, contrasenia_actual, contrasenia_nueva):
        if not self.autenticar(contrasenia_actual):
            return False
        if not contrasenia_nueva or len(contrasenia_nueva) < 8:
            return False
        if contrasenia_actual == contrasenia_nueva:
            return False
        self._contrasenia_hash = self._crear_hash(contrasenia_nueva)
        return True


    def agregar_permiso(self, permiso, encargado):
        if encargado is None:
            return False
        if "administrar_permisos" not in encargado._permisos:
            return False
        if not isinstance(permiso, str) or not permiso.strip():
            return False
        permiso = permiso.strip()
        if permiso in self._permisos:
            return False
        self._permisos.append(permiso)
        return True
