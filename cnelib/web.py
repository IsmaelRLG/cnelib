# -*- coding: utf-8 -*-
"""
cnelib - Visualizador web
Copyright 2016, Ismael R. Lugo G.
"""

import sys


#lint:disable
if sys.version_info >= (3, 0):  # Python 3
    from urllib.request import ProxyHandler
    from urllib.request import build_opener
    from urllib.request import install_opener
    from urllib.request import Request
    from urllib.request import urlopen
    TorCtl = None
else:  # Python 2
    try:
        from TorCtl import TorCtl
    except ImportError:
        TorCtrl = None

    from urllib2 import ProxyHandler
    from urllib2 import build_opener
    from urllib2 import install_opener
    from urllib2 import Request
    from urllib2 import urlopen
#lint:enable


class web:

    def __init__(self, addr='', port=0, passwd=''):
        """
        Clase para aperturar paginas web.
        Esta clase da la posibilidad de salir a la web con Tor (Proxy). Para
        activar este modo hay que usar los siguientes argumentos:
        * addr -- Direccion de control (ControlAddr)
        * port -- Numero de puerto (ControlPort)
        * passwd -- Contraseña de control

        En caso de no usar algunos de estos argumentos, o no tener instalada la
        libreria 'TorCtl', se desactivara la navegacion con proxy.

        >>> import cnelib
        >>> web = cnelib.web.web()
        >>> # Soy visible, todos me ven.
        >>> html1 = web.open('http://www.google.com')
        >>> # Soy invisible, nadie me ve.
        >>> web.proxy('localhost', 9051, 'AbreteSesamo')
        >>> html2 = web.open('http://www.google.com')

        Intencion del Proxy
            La intención del proxy es saltar ciertas restricciones de algun
            limite de solicitudes que pudiera existir.
        """
        if (addr, port, passwd) != ('', 0, '') and TorCtl is not None:
            self.proxy(addr, port, passwd)
        else:
            self.proxy_status = False

    def proxy(self, addr, port, passwd):
        """
        Setea la configuracion proxy, en caso de no existir, y en caso de que
        exista se actualiza.
        * addr -- Direccion de control (ControlAddr)
        * port -- Numero de puerto (ControlPort)
        * passwd -- Contraseña de control
        """
        self.proxy_status = True
        self.addr = addr
        self.port = port
        self.passwd = passwd
        self.header = {'User-Agent': ('Mozilla/5.0 (Windows; U; Windows NT 5.1;'
                       ' es-VE; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7')}

    def open(self, url):
        """
        Apertura una pagina web con Proxy o no, y retorna lo leido.
        * url -- URL de la pagina web
        """
        if self.proxy_status:
            tor = TorCtl.connect(
                controlAddr=self.addr,
                controlPort=self.port,
                passphrase=self.passwd)
            tor.send_signal('NEWNYM')
            tor.close()

            proxy = ProxyHandler({'http': '127.0.0.1:8118'})
            proxy = build_opener(proxy)
            install_opener(proxy)
            request = Request(url, None, self.header)
            return urlopen(request).read()
        else:
            return urlopen(url).read()
