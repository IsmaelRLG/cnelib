# -*- coding: utf-8 -*-
"""cnelib

¿Que es cnelib? Es una libreria que permite hacer consultas sobre cedulas de
identidad inscritas o no, en el registro de el Consejo Nacional Electoral (CNE),
además de tener la capacidad de salvaguardar los datos obtenidos, en una base de
datos local, usando MySQL y SQLite como motores de base de datos, dando mayores
posibilidades, como busqueda por nombre, estado, posibilidad de trabajo offline,
etc.
"""

__author__ = 'Ismael Lugo'
__version__ = '1.0.4'

#lint:disable
from . import getdata
from . import blend
from . import config
from . import database
from . import equal
from . import fork
from . import web
#lint:enable
