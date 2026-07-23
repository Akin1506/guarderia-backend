from firebase_admin import messaging

from apps.usuarios.models import DispositivoFCM


def enviar_notificacion_usuario(usuario, titulo, cuerpo, data=None):
    dispositivos = DispositivoFCM.objects.filter(
        id_usuario=usuario,
        activo=True,
    )

    tokens = list(
        dispositivos.values_list("token", flat=True)
    )

    if not tokens:
        return {
            "enviadas": 0,
            "fallidas": 0,
            "detalle": "El usuario no tiene dispositivos FCM registrados.",
        }

    datos = {
        str(clave): str(valor)
        for clave, valor in (data or {}).items()
    }

    mensaje = messaging.MulticastMessage(
        notification=messaging.Notification(
            title=titulo,
            body=cuerpo,
        ),
        data=datos,
        tokens=tokens,
    )

    respuesta = messaging.send_each_for_multicast(mensaje)

    for indice, resultado in enumerate(respuesta.responses):
        if resultado.success:
            continue

        excepcion = resultado.exception
        codigo = getattr(excepcion, "code", "")

        if codigo in {
            "messaging/registration-token-not-registered",
            "messaging/invalid-registration-token",
        }:
            DispositivoFCM.objects.filter(
                token=tokens[indice]
            ).update(activo=False)

    return {
        "enviadas": respuesta.success_count,
        "fallidas": respuesta.failure_count,
    }