# -*- coding: utf-8 -*-
"""
cnelib - Obtencion de Datos CNE
Copyright 2016, Ismael R. Lugo G.
"""

import re
import logging
from cnelib import equal


class cedula:
    # Zona de expresiones regulares
    __nombre_patt__ = re.compile(
        '<td>'
            '<b>(?P<nombre>.+)</b>'
        '</td>')
    __error_ce__ = re.compile(
        '<td colspan="3">'
            '<strong>'
                '<font color="(.+)">(?P<error>.+)</font>'
            '</strong>'
        '</td>')
    __nombre__ = re.compile(
        '<td align="left">'
            '<b>'
                '<font color="(.+)">Nombre:</font>'
            '</b>'
        '</td>')
    __nombre_ce__ = re.compile(
        '<td align="left">'
            '<b>(?P<nombre>.+)</b>'
        '</td>')
    __estado__ = re.compile(
        '<td align="left">'
            '<b>'
                '<font color="(.+)">Estado:</font>'
            '</b>'
        '</td>')
    __estado_ce__ = re.compile('<td align="left">(?P<estado>.+)</td>')
    __municipio__ = re.compile(
        '<td align="left">'
            '<b>'
                '<font color="(.+)">Municipio:</font>'
            '</b>'
        '</td>')
    __municipio_ce__ = re.compile('<td align="left">(?P<municipio>.+)</td>')
    __parroquia__ = re.compile(
        '<td align="left">'
            '<b>'
                '<font color="(.+)">Parroquia:</font>'
            '</b>'
        '</td>')
    __parroquia_ce__ = re.compile('<td align="left">(?P<parroquia>.+)</td>')
    __centro__ = re.compile(
        '<td align="left">'
            '<b>'
                '<font color="(.+)">Centro:</font>'
            '</b>'
        '</td>')
    __centro_ce__ = re.compile(
        '<td align="left">'
            '<font color="(.+)">(?P<centro>.+)</font>'
        '</td>')
    __direccion__ = re.compile(
        '<td align="left">'
            '<b>'
                '<font color="(.+)">Dirección:</font>'
            '</b>'
        '</td>')
    __direccion_ce__ = re.compile(
        '<td align="left">'
            '<font color="(.+)">(?P<direccion>.+)</font>'
        '</td>')

    # Enlaces
    cne = "http://cne.gob.ve/web"
    rep = cne + "/registro_civil/buscar_rep.php?nac={nac}&ced={ci}"
    ce_ = cne + "/registro_electoral/ce.php?nacionalidad={nac}&cedula={ci}"

    def __init__(self, web):
        """
        Clase para busqueda sobre la web del CNE, consultando en distintos
        metodos, el primero es el registro electoral, el segundo el registro
        civil.

        Argumentos:
        * web -- Clase de consulta web

        >>> import cnelib
        >>> web = cnelib.web.web()
        >>> cneweb = cnelib.getdata.cedula(web)
        >>> cneweb.setNac('V')
        >>>
        """
        self.web = web
        self.defaultNac = None

    def setNac(self, nac):
        """
        Setea una nacionalidad por default
        * nac -- Nacionalidad (V|E)

        >>> cneweb.setNac('E')
        >>> cneweb.search(12345678)
        {'nacionalidad': 'V', 'cedula': 12345678, 'error': '<error code>'}
        >>>
        """
        self.defaultNac = nac

    def search(self, ced, nac=''):
        """
        Busqueda general sobre la web del CNE. Se realiza una consulta en el
        registro electoral, de no estar inscrito, se consulta en el registro
        civil; valor de retorno: dict.

        CONSULTA─┐
                 ╽
            REGISTRO ELECTORAL┑
                 ╽            │
            REGISTRO CIVIL────┤
                              ╽
                        RESULTADOS

        Argumentos:
        * ced -- Numero de cedula
        * nac -- (OPCIONAL) Nacionalidad (V|E).

        >>> cneweb.search(12345678)
        {'nacionalidad': 'V', 'cedula': 12345678, 'nombre': 'Peppa Pig'}
        >>> cneweb.search(12345679, 'V')
        {'nacionalidad': 'V', 'cedula': 12345679, 'nombre': 'George Pig'}
        >>> cneweb.search(12345680, 'E')
        {'nacionalidad': 'V', 'cedula': 12345680, 'nombre': 'Papá Pig'}
        """

        if not nac and not self.defaultNac:
            raise TypeError("Required argument 'nac' (pos 2) not found")
        elif self.defaultNac and not nac:
            nac = self.defaultNac
        nac = nac.upper()
        result = self.registro_electoral(nac, ced)
        if 'error' in result:
            nombre = self.registro_civil(nac, ced)
            if isinstance(nombre, str):
                del result['error']
                result['nombre'] = nombre
            elif nombre is False:
                result['error'] = 'Internet desconectado'
            else:
                result['error'] = 'No registrado en la base de datos'

        result['nacionalidad'] = nac
        result['cedula'] = ced
        if 'error' in result:
            logging.error(result['error'])
        return result

    def registro_civil(self, nac, ced):
        """
        Realiza una busqueda sobre el registro civil. Retorna -> string
        Argumentos:
        * nac - Nacionalidad (V|E)
        * ced - Numero de cedula

        >>> cneweb.registro_civil(12345678, 'V')
        'Peppa Pig'
        >>> cneweb.registro_civil(12345679, 'V')
        'George Pig'
        """
        logging.debug('Buscando en registro civil, %s-%s.' % (nac, ced))
        page = self.rep.format(nac=nac, ci=ced)
        try:
            name = self.web.open(page).replace('\t', '').splitlines()[3]
        except:
            return False
        name = self.__nombre_patt__.match(name)

        if name:
            return name.group('nombre').title()

    def registro_electoral(self, nac, ced):
        """
        Realiza una busqueda sobre el registro electoral. Retorna -> dict
        Argumentos:
        * nac - Nacionalidad (V|E)
        * ced - Numero de cedula

        >>> cneweb.registro_electoral('V', 12345678)
        {'error': 'Cedula no inscrita en el registro electoral.'}
        >>> cneweb.registro_electoral('V', 12345681)
        {'nombre': 'Maestro Roshi', 'estado': 'Isla', 'municipio': 'Isla',
         'parroquia': 'Isla', 'centro': 'Islote',
         'direccion': 'Cerca de la capital del norte, en la Kame House'}
        """
        logging.debug('Buscando en registro electoral, %s-%s.' % (nac, ced))
        result = {}
        page = self.ce_.format(nac=nac, ci=ced)
        try:
            html = self.web.open(page).replace('\t', '').splitlines()
        except Exception as error:
            result['error'] = str(error)
            return result

        if self.__error_ce__.match(html[35]):
            result['error'] = 'Cedula no inscrita en el registro electoral.'
            return result
        elif self.__nombre__.match(html[35]):
            nombre = self.__nombre_ce__.match(html[36]).group('nombre').title()
            result['nombre'] = equal.parse_text(nombre)
        if self.__estado__.match(html[39]):
            estado = self.__estado_ce__.match(html[40]).group('estado').title()
            estado = equal.estado(estado)
            estado = equal.parse_text(estado)
            result['estado'] = estado
        if self.__municipio__.match(html[43]):
            municipio = self.__municipio_ce__.match(html[44])
            municipio = municipio.group('municipio').title()
            municipio = equal.municipio(municipio)
            municipio = equal.parse_text(municipio)
            result['municipio'] = municipio
        if self.__parroquia__.match(html[47]):
            parroquia = self.__parroquia_ce__.match(html[48])
            parroquia = parroquia.group('parroquia').title()
            parroquia = equal.parroquia(parroquia)
            parroquia = equal.parse_text(parroquia)
            result['parroquia'] = parroquia
        if self.__centro__.match(html[51]):
            centro = self.__centro_ce__.match(html[52]).group('centro').title()
            centro = equal.parse_text(centro)
            result['centro'] = centro
        if self.__direccion__.match(html[55]):
            direccion = self.__direccion_ce__.match(html[56])
            direccion = direccion.group('direccion').lower()
            direccion = equal.parse_text(direccion)
            result['direccion'] = direccion

        return result
