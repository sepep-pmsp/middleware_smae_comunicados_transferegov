from fastapi import HTTPException

class MissingData(HTTPException):
    '''Raises quando o site retorna um html que nao contém o elemento/dado esperado'''
    def __init__(self, nom_atributo: str = None, headers: dict = None):

        detail = f'Dados faltantes: {nom_atributo}'

        super().__init__(status_code=404, detail=detail, headers=headers)
