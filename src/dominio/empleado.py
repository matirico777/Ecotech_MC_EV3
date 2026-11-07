from dominio.validaciones import texto_obligatorio, correo_valido, fecha_valida, numero_positivo


class Empleado:
    def __init__(self, nombre, direccion, numero, correo, fecha_contrato, salario, cargo, id=None):
        self._id = id
        self._nombre = texto_obligatorio(nombre, "El nombre")
        self._direccion = texto_obligatorio(direccion, "La direccion")
        self._numero = texto_obligatorio(numero, "El telefono")
        digitos = ''.join(c for c in self._numero if c.isdigit())
        if any(c not in '0123456789 +()-' for c in self._numero) or not 8 <= len(digitos) <= 12:
            raise ValueError("El telefono debe contener entre 8 y 12 digitos.")
        self._correo = correo_valido(correo)
        self._fecha_contrato = fecha_valida(fecha_contrato, "La fecha de contrato", permitir_futura=False)
        self._salario = numero_positivo(salario, "El salario")
        self._cargo = texto_obligatorio(cargo, "El cargo")
        self._registros_tiempo = []

    def mostrar_datos(self):
        return f"{self._id} - {self._nombre} - {self._cargo} - {self._correo} - {self._direccion}"

    def ver_salario(self):
        return self._salario

    def registrar_horas(self, registro):
        if registro is None or registro._empleado != self:
            raise ValueError("El registro pertenece a otro empleado o es invalido")
        numero_positivo(registro._horas_trabajadas, "Las horas", 24)
        if registro in self._registros_tiempo:
            raise ValueError("Este registro ya fue agregado")
        self._registros_tiempo.append(registro)
        return sum(r._horas_trabajadas for r in self._registros_tiempo)
