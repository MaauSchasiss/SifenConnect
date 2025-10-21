from datetime import datetime, timedelta


def generar_fecha_emision(fecha_transmision: datetime = None, ajuste_horas: int = 0) -> str:
    """
    Genera la fecha de emisión del DE en formato AAAA-MM-DDThh:mm:ss
    con los límites de 720 horas atrás y 120 horas adelante respecto a la fecha de transmisión.
    
    :param fecha_transmision: fecha/hora actual de transmisión (por defecto ahora)
    :param ajuste_horas: ajuste opcional en horas (puede ser negativo o positivo)
    :return: string de fecha en formato KuDE
    """
    if fecha_transmision is None:
        fecha_transmision = datetime.now()
    
    # Límite máximo y mínimo
    max_fecha = fecha_transmision + timedelta(hours=120)   # +5 días
    min_fecha = fecha_transmision - timedelta(hours=720)   # -30 días
    
    # Fecha ajustada
    fecha_ajustada = fecha_transmision + timedelta(hours=ajuste_horas)
    
    # Aplicar límites
    if fecha_ajustada > max_fecha:
        fecha_ajustada = max_fecha
    elif fecha_ajustada < min_fecha:
        fecha_ajustada = min_fecha
    
    # Formato AAAA-MM-DDThh:mm:ss
    return fecha_ajustada.strftime("%Y-%m-%dT%H:%M:%S")
