# -*- coding: utf-8 -*-
"""
cnelib - Forker de base de datos CNE
Copyright 2016, Ismael R. Lugo G.

NOTA: Usar este codigo con precaución y bajo su responsabilidad.
"""

import logging
from progressbar import ProgressBar
from progressbar import Percentage
from progressbar import Bar
from progressbar import ETA
from progressbar import SimpleProgress
from time import sleep


class fork:

    def __init__(self, blend, sps=0.2, nac='', init=0,
                 end=0, now=0, conf=None, pbar=False):
        self.conf = conf
        self.pbar = pbar
        self.__warnnum__ = 100
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

        self.widget = [
            #' ' * 34,
            '[', SimpleProgress(' / '), ']',
            Bar(marker='=', left='[', right=']', fill='-'), ' ',
            '[', Percentage(), ']',
            ' ', ETA(), '  ']

        # Zona de control
        # [ error critico ]
        if self.end <= self.now or self.end <= self.init:
            raise IndexError('Rango final igual o menor al incial.')

        # [ advertencia para rangos muy altos]
        if (self.end - self.now) >= self.__warnnum__:
            logging.warning('Se establecio un rango muy elevado.')
            sleep(1.5)

    @property
    def status_P(self):
        L = float(self.end - self.init)
        D = L - (self.end - self.now)
        return float('%.2f' % (D / L * 100))

    @property
    def status(self):
        return (self.init, self.end, self.now)

    def uppbar(self, pbar):
        if not self.pbar:
            return

        val = pbar.currval + 1
        if val <= pbar.maxval:
            pbar.update(val)

    def fork(self):
        logging.info('Iniciando Forkeo...')
        pbar = ProgressBar(widgets=self.widget, maxval=(self.end - self.now))

        # Iniciando barra de progreso :D
        if self.pbar:
            pbar.start()

        while self.now <= self.end and not self.__stop__:
            try:
                sleep(self.sps)
                if len(self.cedula.search(self.nac, self.now)) == 0:
                    self.now += 1
                    self.uppbar(pbar)
                    continue

                self.now += 1
                if self.conf:
                    self.conf.conf.set('CNE', 'now', str(self.now))
                    self.conf.save()

                # Actualizando barra de progreso :D
                self.uppbar(pbar)
            except KeyboardInterrupt:
                if self.pbar:
                    pbar.finish()
                    print '\n'
                self.stop()
        else:
            logging.info('Forkeo finalizado. Completado: %.2f%s, Detenido: %s.' %
            (self.status_P, '%', 'sí' if self.__stop__ else 'no'))

    def stop(self):
        self.__stop__ = True

    def start(self):
        self.__stop__ = False
        self.fork
