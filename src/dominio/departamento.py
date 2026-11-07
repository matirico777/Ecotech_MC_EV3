from dominio.validaciones import texto_obligatorio
from dominio import empleado
from dominio import proyecto
from dominio.empleado import Empleado
from dominio.proyecto import Proyecto

class Departamento:

    def __init__(self, nombre, id_departamento=None, id_gerente=None):
        self._id_departamento = id_departamento
        self._nombre = texto_obligatorio(nombre, "El nombre del departamento")
        self._id_gerente = id_gerente
        self._empleados = []
        self._proyectos = []



    def contratar_empleado(self, empleado: Empleado, encargado: Empleado) -> bool:
        if empleado is None or encargado is None:
            return False
        if encargado._cargo.strip().casefold() != "recursos humanos":
            return False
        if empleado in self._empleados:
            return False
        self._empleados.append(empleado)
        return True


    def agregar_empleado(self, empleado: Empleado) -> bool:
        if empleado is None or empleado in self._empleados:
            return False
        self._empleados.append(empleado)
        return True

    def eliminar_empleado(self, empleado: Empleado) -> None:
        if empleado not in self._empleados:
            return
        self._empleados.remove(empleado)

    def crear_proyecto(self, proyecto) -> bool:
        if proyecto is None or proyecto in self._proyectos:
            return False
        self._proyectos.append(proyecto)
        return True

    def editar_proyecto(self, proyecto, nuevo_nombre: str) -> bool:
        if proyecto not in self._proyectos:
            return False
        if not isinstance(nuevo_nombre, str) or not nuevo_nombre.strip():
            return False
        proyecto._nombre = nuevo_nombre.strip()
        return True

    def eliminar_proyecto(self, proyecto) -> bool:
        if proyecto not in self._proyectos:
            return False
        self._proyectos.remove(proyecto)
        return True

    @property
    def empleados(self) -> tuple:
        return tuple(self._empleados)
    def cantidad_empleados(self) -> int:
        return len(self._empleados)












































































































































































































































































































