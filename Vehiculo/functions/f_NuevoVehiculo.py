from datetime import datetime
import models as model
import Usuario.functions.f_AccionesUsuario as faccu

def AltaConductor(idUsuario,idVehiculo):
    nuevoConductor = model.Conductor(
        id_usuario=idUsuario,
        id_vehiculo=idVehiculo
    )
    model.Conductor.save_to_db(nuevoConductor)

    faccu.ConvertirEnConductor(idUsuario)

    return nuevoConductor

def CrearVehiculo(patente,cantidad_asientos,descripcion):
    nuevoVehiculo = model.Vehiculo(
            patente=patente,
            cantidad_asientos=cantidad_asientos,
            descripcion = descripcion,
            fecha_actualizacion=datetime.now(),
            fecha_creacion=datetime.now(),
            id_estado_vehiculo=1
        )
    model.Vehiculo.save_to_db(nuevoVehiculo)
    vehiculo = model.Vehiculo.query.get(nuevoVehiculo.id)
    
    return vehiculo