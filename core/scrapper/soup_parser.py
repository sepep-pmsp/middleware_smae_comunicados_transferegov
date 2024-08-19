from bs4 import BeautifulSoup

from .decorators import nonetype_error_to_none, raise_for_missing_data

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
