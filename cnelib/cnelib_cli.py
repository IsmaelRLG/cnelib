#!/usr/bin/env python
# -*- coding: utf-8 -*-
# cnelib: módulo para la interacción con la lib via comandos
# Copyright 2016-2017, Ismael R. Lugo G.
from __future__ import unicode_literals

import argparse
import cnelib
import logging
import time
import prettytable
from os import system
from cnelib import config
from progressbar import ProgressBar
from progressbar import Percentage
from progressbar import Bar
from progressbar import Timer
from progressbar import SimpleProgress



cli = argparse.ArgumentParser(version=cnelib.__version__)
cli.add_argument("-d", "--debug",
    help   ='Habilita los mensajes de depuración',
    action ='store_true')
#cli.add_argument("-v", "--version",
    #help   ='Muestra la versión actual de cnelib',
    #action ='store_true')


# Configuración
cfg = cli.add_argument_group('Opciones de configuración')
cfg.add_argument("-g", "--genconf",
    help   ='Genera el archivo de configuración',
    action ='store_true')
cfg.add_argument("-c", "--conf",
    metavar=('<config file>',),
    default=config.CFG_PATH,
    help   ='Ubicación del archivo de configuración. Por defecto: %(default)s')
cfg.add_argument("-e", "--edit",
    help   ='Apertura el archivo de configuración con su editor preferido',
    action ='store_true')


# sondeo
prb = cli.add_argument_group('Opciones de sondeo/busqueda')
prb.add_argument("-r", "--rango",
    metavar=('<rango de cédulas>',),
    help   ='Rango de número de cédulas a sondear',
    type   =str)
prb.add_argument("-n", "--nacionalidad",
    metavar=('<V|E>',),
    choices=('V', 'E'),
    help   ='Nacionalidad para la cédula o el rango a sondear. Por defecto: %(default)s',
    default=config.NAC,
    type   =str)
prb.add_argument("-s", "--sondas",
    metavar=('<número de sondas>',),
    help   ='Número de sondas a utilizar para el sondeo. Por defecto: %(default)s',
    default=config.THR,
    type   =int)
prb.add_argument("-ex", "--expiracion",
    metavar=('<tiempo de expiracion>',),
    help   ='Tiempo de expiracion de los resultados (en segundos). Por defecto: %(default)s',
    default=config.EXPIRE,
    type   =int)
prb.add_argument("-S", "--solicitudes",
    metavar=('<intervalo de solicitudes>',),
    help   ='Intervalo de solicitudes (en segundos). Por defecto: %(default)s',
    default=config.SPS,
    type   =int)
prb.add_argument("--show",
    help   ='Muestra el resultado encontrado.',
    dest   ='show',
    action ='store_true')


# proxy
prx = cli.add_argument_group('Opciones del proxy')
prx.add_argument("-ph", "--proxy-host",
    metavar=('<nombre del host>',),
    default=config.PR_HOST or config.null,
    help   ='Dirección del proxy a utilizar. Por defecto: %(default)s',
    type   =str)
prx.add_argument("-pp", "--proxy-port",
    metavar=('<número del puerto>',),
    #default=config.PR_PORT or config.null,
    help   ='Número del puerto a utilizar para el proxy. Por defecto: %s' % config.null,
    type   =int)

prx.add_argument("-pu", "--proxy-user",
    metavar=('<usuario del proxy>',),
    default=config.PR_USER or config.null,
    help   ='Nombre de usuario para el proxy. Por defecto: %(default)s',
    type   =str)
prx.add_argument("-pP", "--proxy-password",
    metavar=('<contraseña del proxy>',),
    default=config.PR_PASS or config.null,
    help   ='Contraseña del usuario para el proxy. Por defecto: %(default)s',
    type   =str)


# bases de datos
db = cli.add_argument_group('Opciones de la base de datos')

db.add_argument("-dt", "--db-type",
    metavar=('<sqlite|mysql|postgresql>',),
    choices=('sqlite', 'mysql', 'postgresql'),
    default=config.DB_TYPE,
    help   ='Tipo de base de datos a utilizar. Por defecto: %(default)s',
    type   =str)
db.add_argument("-dF", "--db-file",
    metavar=('<path de la db>',),
    default=config.DB_PATH or config.null,
    help   ='Ubicación de la db (solo si se necesita). Por defecto: %(default)s',
    type   =str)

db.add_argument("-dn", "--db-name",
    metavar=('<nombre de la db>',),
    default=config.DB_NAME or config.null,
    help   ='Nombre de la base de datos (solo si se necesita). Por defecto: %(default)s',
    type   =str)
db.add_argument("-dh", "--db-host",
    metavar=('<nombre del host>',),
    default=config.DB_HOST or config.null,
    help   ='Dirección de la base de datos a utilizar. Por defecto: %(default)s',
    type   =str)
db.add_argument("-dp", "--db-port",
    metavar=('<número del puerto>',),
    #default=config.DB_PORT or config.null,
    help   ='Número del puerto a utilizar para la base de datos. Por defecto: %s' % config.null,
    type   =int)

db.add_argument("-du", "--db-user",
    metavar=('<usuario de la db>',),
    default=config.DB_USER or config.null,
    help   ='Nombre del usuario para la base de datos. Por defecto: %(default)s',
    type   =str)
db.add_argument("-dP", "--db-password",
    metavar=('<contraseña de la db>',),
    default=config.DB_PASS or config.null,
    help   ='Contraseña del usuario para la base de datos. Por defecto: %(default)s',
    type   =str)


def set_debug(level, format='%(levelname)s: %(message)s'):
    logging.basicConfig(level=level, format=format)


def main():
    cmd = cli.parse_args()
    #if cmd.version:
        #print('cnelib v' + cnelib.__version__)
        #print('Copyright 2016-2017, Ismael Lugo')
        #return

    if cmd.debug:
        set_debug(10)
        config.debug = True
    else:
        set_debug(40)

    default = config.__dict__.copy()
    if config.check_conf(cmd.conf) and cmd.genconf:
        return logging.error('La configuración ya existe: %s', cmd.conf)
    elif not config.check_conf(cmd.conf) and cmd.genconf:
        return config.save_conf(cmd.conf)
    elif config.check_conf(cmd.conf) and cmd.edit:
        return system('editor ' + cmd.conf)
    elif config.check_conf(cmd.conf) and not cmd.genconf:
        config.CFG_PATH = cmd.conf  # feedback
        config.read_conf(cmd.conf)
        new_values = config.__dict__

    def not_null(cmd_value, name, null=False):
        if cmd_value != default['null' if null else name]:
            return cmd_value
        else:
            return new_values[name]

    config.PR_HOST = not_null(cmd.proxy_host, 'PR_HOST', null=True)
    config.PR_PORT = not_null(cmd.proxy_port, 'PR_PORT', null=True)

    if cmd.proxy_user != config.null and cmd.proxy_password != config.null:
        config.PR_USER = cmd.proxy_user
        config.PR_PASS = cmd.proxy_password

    config.DB_TYPE = not_null(cmd.db_type, 'DB_TYPE')
    config.DB_PATH = not_null(cmd.db_file, 'DB_PATH')
    config.DB_NAME = not_null(cmd.db_name, 'DB_NAME')
    config.DB_HOST = not_null(cmd.db_host, 'DB_HOST', null=True)
    config.DB_PORT = not_null(cmd.db_port, 'DB_PORT', null=True)
    config.DB_USER = not_null(cmd.db_user, 'DB_USER', null=True)
    config.DB_PASS = not_null(cmd.db_password, 'DB_PASS', null=True)

    # Segmento de la busqueda...
    config.C_RANG = cmd.rango or config.C_RANG
    config.NAC = not_null(cmd.nacionalidad, 'NAC')
    config.THR = not_null(cmd.sondas, 'THR')
    config.EXPIRE = not_null(cmd.expiracion, 'EXPIRE')
    config.SPS = not_null(cmd.solicitudes, 'SPS')

    if config.C_RANG is None:
        return cli.print_usage()

    from cnelib.database import gendb
    from cnelib.getdata import blend

    db = gendb(config.DB_TYPE, config.DB_PATH, config.DB_HOST, config.DB_PORT,
               config.DB_NAME, config.DB_USER, config.DB_PASS, config.DB_TABLE)
    if db is config.failed:
        return logging.error('No se puedo crear o conectar a la base de datos.')

    db, Table = db
    db.connect()
    db.create_tables([Table], True)
    scanner = blend(Table, config.EXPIRE, config.NAC, config.C_RANG, config.THR, config.SPS)
    widget = ['[', SimpleProgress(' / '), ']',
              Bar(marker='=', left='[', right=']', fill='-'), ' ',
              '[', Percentage(), ']', ' ', Timer(), '  ']

    list(scanner.calc_range())
    if scanner.total_ci == 0:
        return logging.info('No hay nada que buscar! Saliendo..')

    scanner.start(cmd.show)
    pbar = ProgressBar(widgets=widget, maxval=scanner.total_ci)
    if not config.debug and not cmd.show:
        pbar.start()

    last_value = [scanner.complete[0]]
    try:
        while last_value[0] < scanner.total_ci:
            time.sleep(0.5)

            curr_value = scanner.complete[0]
            if not config.debug and not cmd.show:
                pbar.update(curr_value)
            if last_value[0] != curr_value:
                last_value.pop()
                last_value.append(curr_value)
            else:
                continue
    except KeyboardInterrupt:
        scanner.stop()
        time.sleep(1)
    finally:
        db.close()

    if not config.debug and not cmd.show:
        print('\n')


if __name__ == '__main__':
    main()