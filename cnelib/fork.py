# -*- coding: utf-8 -*-
"""
cnelib - Forker de base de datos CNE
Copyright 2016, Ismael R. Lugo G.

NOTA: Usar este codigo con precaución y bajo su responsabilidad.
"""

import logging
from time import sleep


class fork:

    def __init__(self, blend, sps='', nac='', init='', end='', now='', conf=''):
        self.conf = conf
        if self.conf:
            self.nac = conf('nac').upper()
            self.sps = float(conf('sps'))
            self.init = int(conf('init'))
            self.end = int(conf('init'))
            self.now = int(conf('init'))
        else:
            self.nac = nac.upper()
            self.sps = sps
            self.init = init
            self.end = end
            self.now = now
            self.cedula = blend
        self.cedula = blend
        self.__stop__ = False

    @property
    def status_P(self):
        L = float(self.end - self.init)
        D = L - (self.end - self.now)
        return float('%.2f' % (D / L * 100))

    @property
    def status(self):
        return (self.init, self.end, self.now)

    def fork(self):
        logging.info('Iniciando Forkeo...')
        while self.now <= self.end and not self.__stop__:
            try:
                logging.info('Rango: %d / %d. Cedula: %s-%d. Completado: %.2f%s' %
                (self.init, self.end, self.nac, self.now, self.status_P, '%'))
                if len(self.cedula.search(self.nac, self.now)) == 0:
                    self.now += 1
                    sleep(self.sps)
                    continue
                self.now += 1
                if self.conf:
                    self.conf.conf.set('CNE', 'now', str(self.now))
                    self.conf.save()
                sleep(self.sps)
            except KeyboardInterrupt:
                self.stop()
        else:
            logging.info('Forkeo finalizado. Completado: %.2f%s, Detenido: %s.' %
            (self.status_P, '%', 'sí' if self.__stop__ else 'no'))

    def stop(self):
        self.__stop__ = True

    def start(self):
        self.__stop__ = False
        self.fork
