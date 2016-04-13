# -*- coding: utf-8 -*-
"""
cnelib - Archivo de configuracion
Copyright 2016, Ismael R. Lugo G.

Actualmente solo se soportan dos tipos de bases de datos, MySQL y SQLite3, acá
se dara una breve descripcion de su funcionamiento y su uso, en una forma mas
detallada.
"""

import os
import sys
import logging

if sys.version_info >= (2, 7):
    import configparser as ConfigParser
else:
    import ConfigParser  # lint:ok


class config:

    def __init__(self, abspath, SystemExit=False):
        """
        Clase para facilitar las configuraciones.
        * abspath -- Indica la posicion absoluta del archivo de configuracion

        * SystemExit -- Indica que al no encontrar el archivo de configuracion
        se arrojara una excepcion de tipo "SystemExit", y por consecuencia,
        termina con la salida del interprete.
        """

        self.ABSOLUTE_PATH = abspath

        self.conf = ConfigParser.ConfigParser()

        if not os.path.exists(self.ABSOLUTE_PATH):
            if SystemExit:
                logging.error('Archivo de configuración faltante.')
                exit()
        else:
            self.conf.read(self.ABSOLUTE_PATH)

    def __call__(self, *args):
        """
        Metodo el cual permite llamar al objeto una vez instanciado, podiendo
        solicitar opciones de la configuracion, unicamente contenidas en la
        seccion "CNE".
        * args -- Se da la posibilidad de pasar "ilimitadamente" opciones,
        siempre y cuando esten contenidas en la configuracion.

        >>> config = cnelib.config.config('cnelib.conf')
        >>> config('DB_HOST', 'DB_USER')
        ('localhost', 'root')
        """
        stack = []
        for option in args:
            try:
                stack.append(self.conf.get('CNE', option))
            except ConfigParser.NoOptionError:
                logging.error('Opción faltante: "%s".' % option)

        return tuple(stack) if len(stack) > 1 else stack[0]

    def make(self):
        """
        Crea una plantilla de configuracion en el path previamente dado
        Acerca de los valores de las opciones.

        En caso de usar MySQL
        - DB_HOST -- nombre del host
        - DB_USER -- nombre del usuario
        - DB_PASS -- Contraseña
        - DB_PASS -- Nombre de la base de datos

        En caso de usar SQLite3
        - ABSPATH -- Nombre absoluto de la posicion del archivo

        En caso de querer usar Proxy
        - tor -- Indica si se usara o no proxy
        - addr -- Direccion de control (ControlAddr)
        - port -- Numero de puerto (ControlPort)
        - pass -- Contraseña de control

        En caso de estar en proceso de forkeo
        - init -- Numero de cedula inicial
        - end -- Numero de cedula final
        - now -- Numero de cedula actual
        - sps -- Solicitudes por segundo

        Otros valores:
        - fork -- Indica si hay un proceso de fork andando
        - pid -- Inidica el pid del ultimo proceso andando
        - nac -- Inidica la nacionalidad a buscar por default
        """

        try:
            self.conf.add_section('CNE')
        except ConfigParser.DuplicateSectionError:
            pass

        self.conf.set('CNE', 'DB_HOST', 'localhost')
        self.conf.set('CNE', 'DB_USER', 'root')
        self.conf.set('CNE', 'DB_PASS', 'password')
        self.conf.set('CNE', 'DB_NAME', 'CNE')
        self.conf.set('CNE', 'ABSPATH', '/home/{user}/cne.db')
        self.conf.set('CNE', 'fork', 'no')
        self.conf.set('CNE', 'pid', '0')
        self.conf.set('CNE', 'nac', 'V')
        self.conf.set('CNE', 'init', '0')
        self.conf.set('CNE', 'end', '0')
        self.conf.set('CNE', 'now', '0')
        self.conf.set('CNE', 'sps', '1.2')
        self.conf.set('CNE', 'tor', 'no')
        self.conf.set('CNE', 'addr', 'localhost')
        self.conf.set('CNE', 'port', '9051')
        self.conf.set('CNE', 'pass', 'password')
        self.save()
        logging.info('Configuración inicial creada.')

    def save(self):
        """
        Guarda el estado actual de la configuracion en un archivo.
        """
        with file(self.ABSOLUTE_PATH, 'w') as config:
            self.conf.write(config)
