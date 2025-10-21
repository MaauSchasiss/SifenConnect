from datetime import datetime, timedelta


def generar_fecha_firma(fecha_transmision: datetime = None) -> str:
    """
    Genera la fecha de firma digital del DE en formato AAAA-MM-DDThh:mm:ss.
    La fecha de firma debe ser anterior a la fecha de transmisión.
    """
    if fecha_transmision is None:
        fecha_transmision = datetime.now()
    
    # Para seguridad, se puede poner la firma 1 segundo antes de la transmisión
    fecha_firma = fecha_transmision - timedelta(seconds=1)
    
    return fecha_firma.strftime("%Y-%m-%dT%H:%M:%S")