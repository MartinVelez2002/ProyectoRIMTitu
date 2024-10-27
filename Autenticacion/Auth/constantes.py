class Opciones:

    @staticmethod
    def rol():
        Roles = (('C', 'Coordinador'), ('AC', 'Agente de Control'))
        return Roles

    
    @staticmethod
    def permiso():
        Permisos_Coordinador = {'crear', 'leer', 'eliminar', 'editar'}
        Agente_Control = {'crear', 'leer', 'editar'}
        return Permisos_Coordinador, Agente_Control

    @staticmethod
    def prioridad():
        Prioridades = (('A', 'Alto'), ('M', 'Medio'), ('B', 'Bajo'))
        return Prioridades 
    
    @staticmethod
    def estado_incidente():
        Estados = (('R','Resuelto'),('E','En Proceso'),('N','Notificado')) 
        return Estados
