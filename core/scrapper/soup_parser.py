from bs4 import BeautifulSoup
import bs4.element as elements
from typing import List
import re

from .decorators import nonetype_error_to_none, raise_for_missing_data


PATT_COMUNICADO=r"COMUNICADO\s*(?:[Nn][º°]\s*)?\d+/\d+"

class Parser:

    def __init__(self, html:str)->None:

        self.sopa = self.__build_soup(html)

    def __build_soup(self, html:str)->BeautifulSoup:

        return BeautifulSoup(html, features="html.parser")
    
    @raise_for_missing_data('ultima_atualizacao')
    @nonetype_error_to_none
    def ultima_autualizacao_pagina(self)->str:

        parent = self.sopa.find('span', {'class' : 'documentModified'})
        child = parent.find('span', {'class' : 'value'})

        return child.text

    @raise_for_missing_data('artigos')
    @nonetype_error_to_none
    def __lst_artigos(self)->List[elements.Tag]:

        div_artigos = self.sopa.find('div', {'class' : 'entries'})
        lst_artigos = div_artigos.find_all('article')

        return lst_artigos
    
    @raise_for_missing_data('resumo')
    @nonetype_error_to_none
    def __resumo_artigo(self, artigo:elements.Tag)->elements.Tag:

        return artigo.find('span', {'class' : 'summary'}).find('a')
    
    @raise_for_missing_data('resumo')
    @nonetype_error_to_none
    def __titulo_artigo_raw(self, resumo_artigo:elements.Tag)->str:

        return resumo_artigo.contents[0]
    
    def titulo_comunicado(self, titulo_raw:str)->str:
        
        titulo = re.sub(PATT_COMUNICADO, '', titulo_raw, 
                        flags=re.IGNORECASE, count=1)

        titulo_limpo =  titulo.strip()
        titulo_limpo = re.sub('^(- |– )', '', titulo_limpo)

        return titulo_limpo
    
    def numero_comunicado(self, titulo_raw:str)->str:

        num_string = re.search(PATT_COMUNICADO, titulo_raw, 
                               flags=re.IGNORECASE).group()

        patt_num = r"(\d+/\d+)"
        apenas_num = re.search(patt_num, num_string).group()

        return apenas_num
    

    def parse_comunicado(self, artigo:elements.Tag)->dict:

        resumo = self.__resumo_artigo(artigo)
        titulo_raw = self.__titulo_artigo_raw(resumo)

        titulo  =  self.titulo_comunicado(titulo_raw)
        numero_tudo = self.numero_comunicado(titulo_raw)
        apenas_numero  = numero_tudo.split('/')[0]
        apenas_ano = numero_tudo.split('/')[1]


        parsed = {
            'titulo' : titulo,
            'numero' : apenas_numero,
            'ano' : apenas_ano

        }

        return parsed
    

    def parse_comunicados(self)->List[dict]:

        artigos = self.__lst_artigos()
        
        parsed_data = []
        for artigo in artigos:
            try:
                comunicado_parsed = self.parse_comunicado(artigo)
                parsed_data.append(comunicado_parsed)
            except Exception as e:
                print(e)
                print(artigo)
        
        return parsed_data





