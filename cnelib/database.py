# -*- coding: utf-8 -*-
"""
cnelib - Base de datos
Copyright 2016, Ismael R. Lugo G.
"""

import sqlite3
import logging


class sql_db:
    """
    Clase padre para bases de datos con sintaxis SQL.
    """

    def execute(self, query, commit=False):
        """
        Ejecuta algun codigo SQL
        Argumentos:
        * query -- Codigo SQL
        * commit -- Marca si se guardaran o no los cambios, si los hubiere.
        """
        logging.debug('SQL: ' + query)
        self.cursor.execute(query)
        if commit:
            self.connection.commit()

    def set(self, nacionalidad, cedula, nombre, **kwargs):
        """
        Setea alguna cedula
        Argumentos:
        * nacionalidad -- Nacionalidad (V|E)
        * cedula -- Numero de cedula
        * nombre -- Nombre del ciudadano
        * kwargs -- Argumentos clave disponibles:
            - estado -- Estado de residencia
            - municipio - Municipio de residencia
            - parroquia -- Parroquia de residencia
            - centro_votacion -- Centro de votacion
            - direccion -- Direccion de residencia

        >>> db.set('V', 12345678, 'Peppa Pig')
        >>> db.set('V', 12345681, 'Maestro Roshi',
        ... estado='Isla',
        ... municipio='Isla',
        ... parroquia='Isla',
        ... centro_votacion='Islote',
        ... direccion='Cerca de la capital del norte, en la Kame House')
        >>>
        """
        camps = []
        values = []
        if 'estado' in kwargs:
            camps.append('estado')
            values.append("'%s'" % kwargs['estado'])
        if 'municipio' in kwargs:
            camps.append('municipio')
            values.append("'%s'" % kwargs['municipio'])
        if 'parroquia' in kwargs:
            camps.append('parroquia')
            values.append("'%s'" % kwargs['parroquia'])
        if 'centro_votacion' in kwargs:
            camps.append('centro_votacion')
            values.append("'%s'" % kwargs['centro_votacion'])
        if 'direccion' in kwargs:
            camps.append('direccion')
            values.append("'%s'" % kwargs['direccion'])

        if len(camps) > 0 and len(values) > 0:
            camps.insert(0, '')
            values.insert(0, '')

        self.execute("""INSERT INTO
            cedula(ci, nacionalidad, nombre%s)
            VALUES(%d, '%s', '%s'%s)%s""" % (', '.join(camps), cedula,
            nacionalidad, nombre, ', '.join(values),
            ';' if self.type == 'mysql' else ''), commit=True)

    def ultima_cedula(self):
        """
        Retorna el ultimo numero de cedula registrado
        """
        self.execute(
        "SELECT nacionalidad, ci "
        "FROM cedula "
        "WHERE ci=("
            "SELECT MAX(ci) "
            "FROM cedula)" + (';' if self.type == 'mysql' else ''))
        return self.cursor.fetchall()


try:
    import MySQLdb
except ImportError:
    logging.debug('Falta la libreia: MySQLdb, opcion desactivada.')
else:
    class mysql_db(sql_db):

        def __init__(self, host='', user='', passwd='', name='', conf=None):
            """
            Clase para MySQL
            Argumentos:
            * host -- Direccion del host
            * user -- Nombre de usuario
            * passwd -- Contaseña
            * name -- Nombre de la base de datos
            * conf -- Clase de configuracion

            Al indicar el argumento "conf", tiene prioridad sobre los otros
            argumentos que pudieran ser indicados.

            >>> import cnelib
            >>> db = cnelib.database.mysql_db('127.0.0.7', 'root', 'pass')
            >>>
            """
            if conf:
                self.DB_DAT = conf('DB_HOST', 'DB_USER', 'DB_PASS', 'DB_NAME')
            else:
                self.DB_DAT = (host, user, passwd, name)

            self.type = 'mysql'
            self.connection = MySQLdb.connect(*self.DB_DAT)
            self.cursor = self.connection.cursor()

            self.execute("""
                CREATE TABLE IF NOT EXISTS cedula(
                    ci INT NOT NULL PRIMARY KEY,
                    nacionalidad CHAR(1) NOT NULL,
                    nombre CHAR(255) NOT NULL,
                    estado CHAR(50),
                    municipio CHAR(100),
                    parroquia CHAR(100),
                    centro_votacion CHAR(255),
                    direccion VARCHAR(1000),
                    FULLTEXT(
                        nombre, estado, municipio, parroquia,
                        centro_votacion, direccion))
                    ENGINE=MyISAM;""")

        def get(self, **kwargs):
            """
            Consulta en la base de datos y retorna.
            Argumentos claves:

            - Grupo: 1
            * nacionalidad -- Nacionalidad (V|E)
            * cedula -- Numero de cedula
            - --- accion ---> Busca por numero de cedula

            - Grupo: 2
            * text -- Texto para busqueda
            - --- accion ---> Busca por texto

            - Grupo: 3
            * items -- Items para su busqueda
            * compl -- (OPCIONAL) Valores complementarios para busqueda
            - --- accion ---> Busca por expresiones regulares

            >>> db.get(nacionalidad='V', cedula=12345678)
            ((12345678, 'V', 'Peppa Pig', None, None, None, None, None),)
            >>> db.get(text='Kame')
            ('V', 12345681, 'Maestro Roshi', 'Isla', 'Isla', 'Isla', 'Islote',
            'Cerca de la capital del norte, en la Kame House')
            >>> db.get(items={'nombre': '%Pig%'}.items())
            ((12345678, 'V', 'Peppa Pig', None, None, None, None, None),
            (12345679, 'V', 'George Pig', None, None, None, None, None),
            (12345680, 'V', 'Papá Pig', None, None, None, None, None))
            >>> db.get(items={'nombre': '%Gokü%'}.items())
            ()
            >>>

            NOTA: Es imposible entre mezclar los grupos.
            """
            if 'nacionalidad' in kwargs and 'cedula' in kwargs:
                query = """
                SELECT nacionalidad, ci, nombre, estado, municipio,
                       parroquia, centro_votacion, direccion
                FROM cedula
                WHERE nacionalidad='%s' AND ci=%s;""" % (
                kwargs['nacionalidad'], kwargs['cedula'])

            elif 'text' in kwargs:
                query = """
                SELECT *
                FROM cedula
                WHERE MATCH (nombre, estado,
                    municipio, parroquia,
                    centro_votacion, direccion)
                AGAINST ('%s');""" % kwargs['text']
            elif 'items' in kwargs:
                compl = []
                if 'compl' in kwargs:
                    for column, patt in kwargs['compl']:
                        compl.append(' AND %s LIKE "%s"' % (column, patt))
                compl = ''.join(compl)

                items = []
                for column, patt in kwargs['items']:
                    items.append('%s LIKE "%s"' % (column, patt))
                items = ' OR'.join(items)

                query = """
                SELECT *
                FROM cedula
                WHERE %s%s;""" % (items, compl)
            else:
                raise KeyError('No se indicaron las claves o valores.')

            self.execute(query)
            return self.cursor.fetchall()


class sqlite_db(sql_db):

    def __init__(self, abspath):
        """
        Clase para SQLite3.
        Argumentos:
        * abspath -- Direccion absoluta del archivo

        >>> import cnelib
        >>> db = cnelib.database.sqlite_db('/home/{user}/sqlite.db')
        >>>
        """
        self.connection = sqlite3.connect(abspath)
        self.cursor = self.connection.cursor()
        self.type = 'sqlite'
        self.execute("""
            CREATE TABLE IF NOT EXISTS cedula(
                ci INT NOT NULL PRIMARY KEY,
                nacionalidad CHAR(1) NOT NULL,
                nombre CHAR(255) NOT NULL,
                estado CHAR(50),
                municipio CHAR(100),
                parroquia CHAR(100),
                centro_votacion CHAR(255),
                direccion VARCHAR(1000))""")

    def get(self, **kwargs):
        """
        Consulta en la base de datos y retorna.
        Argumentos claves:

        - Grupo: 1
        * nacionalidad -- Nacionalidad (V|E)
        * cedula -- Numero de cedula
        - --- accion ---> Busca por numero de cedula

        >>> db.get(nacionalidad='V', cedula=12345678)
        ((12345678, 'V', 'Peppa Pig', None, None, None, None, None),)
        >>>
        """
        if 'nacionalidad' in kwargs and 'cedula' in kwargs:
            query = """
            SELECT nacionalidad, ci, nombre, estado, municipio,
                   parroquia, centro_votacion, direccion
            FROM cedula
            WHERE nacionalidad='%s' AND ci=%s""" % (
            kwargs['nacionalidad'], kwargs['cedula'])
        else:
            raise KeyError('No se indicaron las claves o valores.')

        self.execute(query)
        return self.cursor.fetchall()