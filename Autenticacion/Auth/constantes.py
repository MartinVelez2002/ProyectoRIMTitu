class Opciones:

    @staticmethod
    def rol():
        Roles = (('S', 'Supervisor'), ('AC', 'Agente de Control'))
        return Roles

    
    @staticmethod
    def permiso():
        Administrador = {'crear', 'leer', 'eliminar', 'editar'}
        Supervisor = {}
        Agente_Control = {'crear', 'leer', 'editar'}
        return Administrador, Supervisor, Agente_Control

    @staticmethod
    def prioridad():
        Prioridades = (('A', 'Alto'), ('M', 'Medio'), ('B', 'Bajo'))
        return Prioridades 
    
    @staticmethod
    def estado_incidente():
        Estados = (('R','Resuelto'),('E','En Proceso'),('N','Notificado')) 
        return Estados
