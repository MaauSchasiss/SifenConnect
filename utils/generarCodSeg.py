import secrets

def generar_codigo_seguridad() -> str:
    """
    Genera un código de seguridad (dCodSeg) válido para SIFEN.
    - Número positivo de 9 dígitos
    - Aleatorio, no secuencial
    - No relacionado con datos del DE
    """
    # genera un número aleatorio entre 1 y 999999999
    codigo = secrets.randbelow(999_999_999) + 1
    
    # convierte a string y completa con ceros a la izquierda si hace falta
    return f"{codigo:09d}"