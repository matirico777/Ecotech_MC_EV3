from dominio.validaciones import texto_obligatorio, fecha_valida, numero_positivo

class RegistroTiempo:
    def __init__(self, horas_trabajadas, fecha_trabajada, descripcion_tarea,
                empleado, proyecto, id_registro=None):
        self._id_registro = id_registro
        self._horas_trabajadas = numero_positivo(horas_trabajadas, "Las horas", 24)
        self._fecha_trabajada = fecha_valida(fecha_trabajada, "La fecha trabajada", permitir_futura=False)
        self._descripcion_tarea = texto_obligatorio(descripcion_tarea, "La descripcion de la tarea")
        if empleado is None or proyecto is None:
            raise ValueError("Debe seleccionar un empleado y un proyecto validos.")
        self._empleado = empleado
        self._proyecto = proyecto

    def calculo_horas(self, registros):
        total_horas = 0
        for registro in registros:
            mismo_empleado = registro._empleado == self._empleado
            if self._empleado._id is not None:
                if registro._empleado._id == self._empleado._id:
                    mismo_empleado = True
            if mismo_empleado:
                total_horas += registro._horas_trabajadas
        return total_horas

    def calculo_horas_proyecto(self, registros, proyecto):
        total_horas = 0
        for registro in registros:
            mismo_empleado = registro._empleado == self._empleado
            mismo_proyecto = registro._proyecto == proyecto
            if self._empleado._id is not None:
                if registro._empleado._id == self._empleado._id:
                    mismo_empleado = True
            if proyecto._id_proyecto is not None:
                if registro._proyecto._id_proyecto == proyecto._id_proyecto:
                    mismo_proyecto = True
            if mismo_empleado and mismo_proyecto:
                total_horas += registro._horas_trabajadas
        return total_horas
