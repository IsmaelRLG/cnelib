# -*- coding: utf-8 -*-
"""
cnelib - Base de datos y Consultas
Copyright 2016, Ismael R. Lugo G.
"""

import cnelib.getdata


class cedula:

    def __init__(self, web, database):
        """
        Mezcla entre consultas en base de datos locales y consultas web, primero
        al solicitar informacion se verifica que este contenida en la base de
        datos local, de no ser asi se procede a una consulta web, y al encontrar
        informacion util, se guarda en la base de datos y retorna.
        * database -- Clase de base de datos
        * web -- Clase de consultas web

        Ejemplos de uso:
        >>> import cnelib
        >>> web = cnelib.web.web()
        >>> db = cnelib.database.sqlite_db('/home/user/cne.db')
        >>> cedula = cnelib.blend.cedula(web, db)
        >>>
        """
        self.database = database
        self.cedula = cnelib.getdata.cedula(web)

    def search(self, nac, ced):
        """
        Busca y retorna tupla con los resultados de la busqueda
        * nac -- Nacionalidad (V|E)
        * ced -- Numero de cedula

        Ejemplo de uso:
        >>> cedula.search('V', 12345678)
        ((12345678, 'V', 'Peppa Pig La Cerdita', None, None, None, None, None),)
        >>>
        """
        result = self.database.get(nacionalidad=nac, cedula=ced)
        if len(result) > 0:
            return result[0]
        else:
            result = self.cedula.search(ced, nac)
            if 'error' in result:
                return ()
            else:
                self.database.set(**result)
                return self.database.get(nacionalidad=nac, cedula=ced)
