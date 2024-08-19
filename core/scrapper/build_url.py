from typing import Literal, Optional


DOMAIN ='www.gov.br'

BASE_URL='transferegov/pt-br/comunicados/'

MAPPER_ENDPOINTS = {
    'gerais' : 'comunicados-gerais',
    'cronogramas' : {
        'base' : 'cronogramas-de-emendas-parlamentares/',
        'individuais' :'cronograma-emendas-individuais-rp6-finalidade-definida',
        'especiais' :'cronograma-emendas-individuais-rp6-transferencias-especiais',
        'bancada' : 'cronograma-emendas-de-bancada-rp7'
    }
}

class UrlBuilder:

    def __init__(self, https:bool=True):

        self.base_url = self.__build_base_url(https)

    def __build_base_url(self, https:bool=True)->str:

        protocol = 'https://' if https else 'http://'
        
        base_url = protocol + DOMAIN + '/' + BASE_URL

        return base_url

    def __build_endpoint(self, *args, gerais:bool, tipo_emenda:Optional[
                            Literal['individuais', 'especiais', 'bancada']]=None)->str:
        
        
        if gerais:
            return self.base_url + MAPPER_ENDPOINTS['gerais']
        
        if not gerais and tipo_emenda is None:
            raise ValueError('Se não buscar comunicados gerais deve definir tipo emenda')
        
        base_url= self.base_url + MAPPER_ENDPOINTS['cronogramas']['base']
        
        return base_url + MAPPER_ENDPOINTS['cronogramas'][tipo_emenda]

    def __build_url(self, *args, gerais:bool, ano:int, tipo_emenda:Optional[
                        Literal['individuais', 'especiais', 'bancada']]=None, )->str:
        
        endpoint = self.__build_endpoint(gerais=gerais, tipo_emenda=tipo_emenda)

        #neste caso não tem ano
        if not gerais and tipo_emenda == 'especiais':
            return endpoint
        
        return endpoint + f'/{ano}'

    
    def __call__(self, gerais:bool, ano:int, tipo_emenda:Optional[
                    Literal['individuais', 'especiais', 'bancada']]=None)->str:
        
        return self.__build_url(gerais=gerais, ano=ano, tipo_emenda=tipo_emenda)