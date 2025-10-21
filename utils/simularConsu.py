from datetime import datetime


def simular_consulta_set(cdc: str):
    """
    Simula la respuesta de la SET.
    Devuelve un diccionario con dFecProc, dCodRes y dMsgRes.
    """
    return {
        "dFecProc": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "dCodRes": "0301",  # aprobado
        "dMsgRes": "Documento procesado correctamente (simulado)"
    }