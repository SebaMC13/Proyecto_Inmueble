from .models import Inmueble


def crear_inmueble(
    nombre,
    descripcion,
    m2_construidos,
    m2_totales,
    estacionamientos,
    habitaciones,
    banos,
    direccion,
    comuna_id,
    tipo_inmueble,
    precio_mensual,
    dueno_id,
):
    Inmueble(
        nombre=nombre,
        descripcion=descripcion,
        m2_construidos=m2_construidos,
        m2_totales=m2_totales,
        estacionamientos=estacionamientos,
        habitaciones=habitaciones,
        banos=banos,
        direccion=direccion,
        comuna_id=comuna_id,
        tipo_inmueble=tipo_inmueble,
        precio_mensual=precio_mensual,
        dueno_id=dueno_id,
    ).save()


def listar_inmuebles():
    return Inmueble.objects.all()


def actualizar_inmueble(id: int, descripcion: str):
    inmueble1 = Inmueble.objects.get(id=id)
    inmueble1.descripcion = descripcion
    inmueble1.save()


def eliminar_inmueble(id: int):
    inmueble1 = Inmueble.objects.get(id=id)
    inmueble1.delete()
    
