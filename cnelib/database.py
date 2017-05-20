# -*- coding: utf-8 -*-
# cnelib: módulo de base de datos
# Copyright 2016-2017, Ismael R. Lugo G.
#-------------------------------------------+
# Bases de datos soportadas:                |
#    MySQL                                  |
#    PostgreSQL                             |
#    SQLite                                 |
#                                           |
# ORM utilizada: peewee                     |
#-------------------------------------------+

import logging
import datetime
try: from . import config
except: import config
from peewee import MySQLDatabase, PostgresqlDatabase, SqliteDatabase
from peewee import Model, CharField, DateTimeField, Check
from peewee import IntegerField, TextField

# Silenciando los logs!
peewee_logger = logging.getLogger('peewee')
peewee_logger.setLevel(logging.ERROR)
logging = logging.getLogger('cnelib')


class BaseModel(Model):
    ci = CharField(primary_key=True)
    nacionalidad = CharField(1)
    cedula = IntegerField(constraints=[Check('cedula > 0')])
    nombre = CharField()

    estado = CharField(null=True)
    municipio = CharField(null=True)
    parroquia = CharField(null=True)
    centro = TextField(null=True)
    direccion = TextField(null=True)
    consultado = DateTimeField(default=datetime.datetime.now)


def gendb(type, path, host, port, db, user, passwd, tablename=config.DB_TABLE):
    if type == 'sqlite':
        db = SqliteDatabase(config.DB_PATH)
    elif type == 'mysql':
        if host is None or port is None or user is None or passwd is None:
            return config.failed
        db = MySQLDatabase(db, host=host, port=port, user=user, passwd=passwd)

    elif type == 'postgresql':
        if host is None or port is None or user is None or passwd is None:
            return config.failed
        db = PostgresqlDatabase(db, host=host, port=port, user=user, password=passwd)
    else:
        logging.error('Tipo de base de datos no soportado o inválido: %s', type)
        return config.failed

    class table(BaseModel):
        class Meta:
            database = db
    table._meta.db_table = tablename
    return (db, table)
