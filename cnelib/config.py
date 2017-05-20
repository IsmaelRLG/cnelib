# -*- coding: utf-8 -*-
# cnelib: módulo de configuraciones
# Copyright 2016-2017, Ismael R. Lugo G.
#-------------------------------------------+
# Este módulo se encarga de crear, cargar   |
# y guardar la configuración. El formato    |
# utilizado es el definido en el RFC 822.   |
#-------------------------------------------+
from __future__ import unicode_literals
from six.moves import configparser
import os
import logging
logging = logging.getLogger('cnelib')

################################################################################
#                  Segmento: Variables de configuraciones                      #
################################################################################

# Variables de entorno
#--------------------------------------------
HOME = os.environ['HOME']  # Carpeta personal
USER = os.environ['USER']  # Nombre del usuario
CONF = os.path.join(HOME, '.config')

# Archivo de configuración
#--------------------------------------------
CFG_EXT = '.conf'
CFG_NAME = 'cedulas-ve'
CFG_PATH = os.path.join(CONF, CFG_NAME + CFG_EXT)

# Bases de datos
#--------------------------------------------
DB_TYPE = 'sqlite'  # Tipos soportados: SQLite, MySQL, PostgreSQL
DB_NAME = 'cedulas'
DB_FILE = 'cedulas-ve.db'
DB_PATH = os.path.join(CONF, DB_FILE)
DB_HOST = None
DB_PORT = None
DB_USER = None
DB_PASS = None
DB_TABLE = 'cedulas'

# Evasión de restricciones (Proxys)
#--------------------------------------------
PR_HOST = None
PR_PORT = None
PR_USER = None
PR_PASS = None

# Opciones de escaneo
#--------------------------------------------
SPS = 0.3  # Una solicitud cada X segundos
THR = 1  # Número de hilos a ejecutar
C_RANG = None  # Rango de cedulas a escanear
NAC = 'V'
#       secs * mins * hours --> day * day mon -->
EXPIRE = 60 * 60 * 24 * 30 * 6


################################################################################
#                  Segmento: Manejador de configuraciones                      #
################################################################################
cfg_parser = configparser.ConfigParser()
cfg_types = {int: 'getint', float: 'getfloat', bool: 'getbolean', str: 'get'}
failed = False
sucess = True
null = 'ninguno'
debug = False


def check_conf(abspath):

    return os.path.exists(abspath) and os.path.isfile(abspath)


def read_conf(abspath):
    if not check_conf(abspath):
        return logging.error('Archivo de configuración "%s" inválido.', abspath)

    try:
        cfg = file(abspath, 'r')
    except IOError as e:
        if e.errno == 13:
            logging.error('Permiso denegado: %s', abspath)
        return failed

    try:
        cfg_parser.readfp(cfg)
    except:
        logging.error('Archivo de configuración "%s" inválido.', abspath)
        return failed

    def get(s, opt, default=None, type=str):
        if not cfg_parser.has_section(s) or not cfg_parser.has_option(s, opt):
            return default
        try:  value = getattr(cfg_parser, cfg_types[type])(s, opt)
        except: return default

        if type == str and value == '':
            return default
        else:
            return value

    global CFG_PATH
    global DB_TYPE, DB_NAME, DB_FILE, DB_PATH, DB_HOST, DB_PORT, DB_USER
    global DB_PASS, DB_TABLE
    global PR_HOST, PR_PORT, PR_USER, PR_PASS
    global SPS, THR, C_RANG, NAC

    # section: conf
    CFG_PATH = get('conf', 'CFG_PATH', CFG_PATH)

    # section: database
    DB_TYPE = get('database', 'DB_TYPE', DB_TYPE)
    DB_NAME = get('database', 'DB_NAME', DB_NAME)
    DB_FILE = get('database', 'DB_FILE', DB_FILE)
    DB_PATH = get('database', 'DB_PATH', DB_PATH)
    DB_HOST = get('database', 'DB_HOST', DB_HOST)
    DB_PORT = get('database', 'DB_PORT', DB_PORT, type=int)
    DB_USER = get('database', 'DB_USER', DB_USER)
    DB_PASS = get('database', 'DB_PASS', DB_PASS)
    DB_TABLE = get('database', 'DB_TABLE', DB_TABLE)

    # section: proxy
    PR_HOST = get('proxy', 'PR_HOST', PR_HOST)
    PR_PORT = get('proxy', 'PR_PORT', PR_PORT, type=int)
    PR_USER = get('proxy', 'PR_USER', PR_USER)
    PR_PASS = get('proxy', 'PR_PASS', PR_PASS)

    # section: scan options
    SPS = get('scan-options', 'SPS', SPS, type=float)
    THR = get('scan-options', 'THR', THR, type=int)
    NAC = get('scan-options', 'SPS', NAC)
    C_RANG = get('scan-options', 'C_RANG', C_RANG)


def save_conf(abspath=CFG_PATH):
    try:
        cfg = file(abspath, 'w')
    except IOError as e:
        if e.errno == 13:
            logging.error('Permiso denegado: %s', abspath)
        return failed

    def set(s, opt):
        if opt is None:
            return
        if not cfg_parser.has_section(s):
            cfg_parser.add_section(s)
        if isinstance(opt, bool):
            opt = 'yes' if opt else 'no'
        else:
            opt = str(opt)
        cfg_parser.set(s, opt)

    # section: conf
    set('conf', 'CFG_PATH', CFG_PATH)

    # section: database
    set('database', DB_TYPE)
    set('database', DB_NAME)
    set('database', DB_FILE)
    set('database', DB_PATH)
    set('database', DB_HOST)
    set('database', DB_PORT)
    set('database', DB_USER)
    set('database', DB_PASS)
    set('database', DB_TABLE)

    # section: proxy
    set('proxy', PR_HOST)
    set('proxy', PR_PORT)
    set('proxy', PR_USER)
    set('proxy', PR_PASS)

    # section: scan options
    set('scan-options', SPS)
    set('scan-options', THR)
    set('scan-options', NAC)
    set('scan-options', C_RANG)

    cfg_parser.write(cfg)
