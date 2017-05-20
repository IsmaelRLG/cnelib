# -*- coding: utf-8 -*-
# cnelib: módulo para la obtención de datos
# Copyright 2016-2017, Ismael R. Lugo G.
#-------------------------------------------+
# Este módulo consulta, parsea y devuelve   |
# la información de la cedula de identidad, |
# como por ejemplo:                         |
#    Si se encuentra registrada o no.       |
#    Nombre completo                        |
#-------------------------------------------+
from __future__ import unicode_literals
import time
import re
import logging
#logging.basicConfig(level=10)

try: from . import config
except: import config  # lint:ok
from datetime import datetime
from six.moves import urllib
from six.moves import range
from six.moves import _thread
from six import string_types
from scrapy.selector import Selector

# alias
logging = logging.getLogger('cnelib')
ProxyHandler = urllib.request.ProxyHandler
build_opener = urllib.request.build_opener
install_opener = urllib.request.install_opener
HTTPHandler = urllib.request.HTTPHandler
AuthHandler = urllib.request.HTTPBasicAuthHandler


class getdata(object):
    # Meta
    proxy = False
    replace_ci = ['.', ',', ' ']
    replace_edo = {'Edo. ': '', 'Dtto. Capital': 'Distrito Capital'}
    replace_mp = {'Mp. ': '', 'Ce. Blvno Libertador': 'Libertador', 'Ce. ': '',
        'Mp.': '',}
    replace_pq = {'Pq. ': '', 'Cm. ': ''}
    replace_txt = {
        '\xc3\x83\xc2\x93': '\xc3\xb3',  # ó
        '\xc3\x83\xc2\x8d': '\xc3\xad',  # í
        '\xc3\x90': 'ñ',  # ñ
        '\xf3': 'o', '\xf1': 'ñ', ''

        'Á': 'a', 'á': 'a', 'À': 'a', 'à': 'a', 'Ä': 'a', 'ä': 'a',
        'É': 'e', 'é': 'e', 'È': 'e', 'è': 'e', 'Ë': 'e', 'ë': 'e',
        'Í': 'i', 'í': 'i', 'Ì': 'i', 'ì': 'i', 'Ï': 'i', 'ï': 'i',
        'Ó': 'o', 'ó': 'o', 'Ò': 'o', 'ò': 'o', 'Ö': 'o', 'ö': 'o',
        'Ú': 'u', 'ú': 'u', 'Ù': 'u', 'ù': 'u', 'Ü': 'u', 'ü': 'u'}

    main_page = 'http://cne.gob.ve/web/registro_'
    reg_civ = main_page + 'civil/buscar_rep.php?nac={nac}&ced={ci}'
    reg_ele = main_page + 'electoral/ce.php?nacionalidad={nac}&cedula={ci}'
    re_xpath = '//td/b/font/text()|//td/b/text()|//td/text()|//td/font/text()'
    rc_xpath = '//td//b/text()'

    @classmethod
    def set_proxy(cls, host, port, user=None, passwd=None):
        if cls.proxy:
            return

        l_auth = '%s:%s@' % (user, passwd) if user and passwd else ''
        proxy = ProxyHandler({'http': 'http://%s%s:%s' % (l_auth, host, port)})

        if l_auth != '':
            opener = build_opener(proxy, AuthHandler(), HTTPHandler())
        else:
            opener = build_opener(proxy)

        install_opener(opener)
        cls.proxy = True

    @classmethod
    def parse_args(cls, nac, ci):
        if isinstance(ci, string_types):
            for rep in cls.replace_ci:
                ci = ci.replace(rep, '')

        ci = int(ci)
        nac = nac.upper()
        assert nac in ('V', 'E')
        return nac, ci

    @staticmethod
    def get_ci(nac, ci):
        return '%s-%s' % (nac, ci)

    @staticmethod
    def parse_data(dict, data):
        for to_replace, new in dict.items():
            data = data.replace(to_replace, new, 1)
        return data

    @classmethod
    def parse_txt(cls, data):
        return cls.parse_data(cls.replace_txt, data)

    @classmethod
    def parse_edo(cls, data):
        return cls._parse_edo(cls.parse_txt(data).title())

    @classmethod
    def parse_mp(cls, data):
        return cls._parse_mp(cls.parse_txt(data).title())

    @classmethod
    def parse_pq(cls, data):
        return cls._parse_pq(cls.parse_txt(data).title())

    @classmethod
    def _parse_edo(cls, data):
        return cls.parse_data(cls.replace_edo, data)

    @classmethod
    def _parse_mp(cls, data):
        return cls.parse_data(cls.replace_mp, data)

    @classmethod
    def _parse_pq(cls, data):
        return cls.parse_data(cls.replace_pq, data)

    def __init__(self, pr_host=None, pr_port=None, pr_user=None, pr_pass=None):
        if pr_host and pr_port:
            self.set_proxy(pr_host, pr_port, pr_user, pr_pass)

    @classmethod
    def request(self, url, nac, ci):
        url = url.format(nac=nac, ci=ci)
        logging.debug('Intentando abrir: %s', url)
        try:
            page = urllib.request.urlopen(url)
        except Exception as error:  # lint:ok
            return #logging.error(repr(error))
        logging.debug('Pagina aperturada: %s', url)
        return page

    @classmethod
    def request_rc(cls, nac, ci):
        return cls.request(cls.reg_civ, nac, ci)

    @classmethod
    def request_re(cls, nac, ci):
        return cls.request(cls.reg_ele, nac, ci)

    @classmethod
    def registro_civil(cls, nac, ci):
        html = cls.request_rc(nac, ci)
        if html is None:
            return config.failed
        html = html.read().decode('utf-8')
        data = Selector(text=html).xpath(cls.rc_xpath).extract()
        if len(data) == 0:
            return config.failed
        return {
            'ci': '%s-%d' % (nac, ci),
            'nacionalidad': nac,
            'cedula': ci,
            'nombre': cls.parse_txt(data[0]).title()}

    @classmethod
    def registro_electoral(cls, nac, ci):
        html = cls.request_re(nac, ci)
        if html is None:
            return config.failed
        html = html.read().decode('utf-8')
        html = html.replace('\t', '').replace('\n', '').replace('\r', '')
        data = Selector(text=html).xpath(cls.re_xpath).extract()
        if not 'Nombre:' in data:
            return config.failed

        return {
            'ci': cls.get_ci(nac, ci),
            'nacionalidad': nac,
            'cedula': ci,
            'nombre': cls.parse_txt(data[data.index('Nombre:') + 1]).title(),
            'estado': cls.parse_edo(data[data.index('Estado:') + 1]),
            'municipio': cls.parse_mp(data[data.index('Municipio:') + 1]),
            'parroquia': cls.parse_pq(data[data.index('Parroquia:') + 1]),
            'centro': cls.parse_txt(data[data.index('Centro:') + 1]).capitalize(),
            'direccion': cls.parse_txt(data[data.index('Dirección:') + 1]).capitalize()
            }

    @classmethod
    def search(cls, nac, ci):
        # Primera busqueda
        data = cls.registro_electoral(nac, ci)

        if data == config.failed:
            # Falló la primera busqueda!
            # Segunda busqueda
            data = cls.registro_civil(nac, ci)

        if data == config.failed:
            # WTF! Falló la segunda!!
            # Cédula no registrada!!
            return config.failed
        else:
            return data


class probe(getdata):
    _stop_probes = False

    @classmethod
    def stop_probes(cls):
        cls._stop_probes = True

    def __init__(self, nac, s_ci, e_ci, antiddos):
        self.nac = nac.upper()
        self.s_ci = s_ci
        self.e_ci = e_ci
        self.counter = 0
        self.finished = False
        self.antiddos = antiddos
        self.stop_probe = False

    def __repr__(self):
        return "<probe %s:%s-%s>" % (self.nac, self.s_ci, self.e_ci)

    def __call__(self):
        return self.probe()

    def _probe(self):
        for ci in range(self.s_ci, self.e_ci +1):
            if self._stop_probes or self.stop_probe:
                break

            yield (self.nac, ci)

    def probe(self):
        for nac, ci in self._probe():
            yield self.search(nac, ci)
            self.counter += 1
            if self.antiddos:
                time.sleep(self.antiddos)
        self.finished = True

    def stop_probe(self):
        self.stop_probe = True


class scanner(getdata):
    range_regex = re.compile(',?((V|E):)?(\d{1,})(-(\d{1,}))?', re.IGNORECASE)

    @classmethod
    def _calc_range(cls, default_nac, ci_range):
        ranges = []
        for res_range in cls.range_regex.findall(ci_range):
            nac = (res_range[1] or default_nac).upper()
            s_ci = int(res_range[2])  # Rango inicial
            e_ci = res_range[4]

            if e_ci == '' or e_ci == res_range[2]:
                e_ci = s_ci
            else:
                e_ci = int(e_ci)

            if s_ci == 0 or e_ci == 0:
                logging.warning('Se indicó un rango nulo: rango obviado')
                continue

            c_range = (nac, s_ci, e_ci)

            if c_range in ranges:
                logging.warning('Se indicó un rango duplicado: rango obviado')
                continue
            else:
                yield c_range

    def __init__(self, nac, ci_range, n_probes=1, s=config.SPS):
        self.nac = nac
        self.ci_range = ci_range
        self.total_ci = 0
        self.n_probes = n_probes
        self.antiddos = s
        self.probe_stack = []

    def calc_range(self):
        total_ci = 0
        for ci_range in self._calc_range(self.nac, self.ci_range):
            s_ci, e_ci = ci_range[1:3]
            if s_ci == 0 or e_ci == 0 or e_ci < s_ci:
                logging.error("Rango de cédulas inválido: %s-%s", s_ci, e_ci)
                continue
            total_ci += ci_range[2] - ci_range[1]
            yield ci_range
        self.total_ci = total_ci

    def gen_probes(self, force=False):
        if len(self.probe_stack) > 0 and not force:
            for pr in self.probe_stack:
                yield pr
        else:
            if force:
                logging.warning('Se está generando un duplicado de las sondas!')
            for ci_range in self.calc_range():
                nac, s_ci, e_ci = ci_range
                t = (e_ci - s_ci)
                p = t / self.n_probes
                if p < 1:
                    p = 1
                else:
                    p = int(p)  # Esto para PY3 que devuelve float...

                n = 1
                while s_ci <= e_ci:
                    if p == 1:
                        c = e_ci
                        a = s_ci
                    if (s_ci + p) < e_ci:
                        c = s_ci + p
                        if n == 1:
                            a = s_ci
                            n += 1
                        else:
                            a = s_ci + 1
                    elif (s_ci + p) == e_ci:
                        c = e_ci
                        a = s_ci if n == 1 else (s_ci + 1)
                    else:
                        break

                    pr = probe(nac, a, c, self.antiddos)
                    s_ci += p
                    self.probe_stack.append(pr)
                    yield pr
                    if p == 1:
                        break


class blend(scanner):
    f = ['%(ci)s', '%(nombre)s', '%(estado)s', '%(municipio)s', '%(parroquia)s']

    def __init__(self, database, expire=config.EXPIRE, *args, **kwargs):
        super(blend, self).__init__(*args, **kwargs)
        self.database = database
        self.expire = expire

    @classmethod
    def _db_search(cls, database, nac, ci):
        try:
            return database.get(database.ci == cls.get_ci(nac, ci))
        except database.DoesNotExist:
            return

    @classmethod
    def _set(cls, database, **kw):
        cedula = cls._db_search(database, kw['nacionalidad'], kw['cedula'])
        if cedula is None:
            database.create(**kw)
        else:
            for attr, val in kw.values():
                setattr(cedula, attr, val)
            cedula.save()

    def db_search(self, nac, ci):
        return self._db_search(self.database, nac, ci)

    def set(self, **kwargs):
        self._set(self.dabatase, **kwargs)

    def get(self, nac, ci):
        cedula = self.db_search(nac, ci)
        if cedula is None:
            data = self.search(nac, ci)
            if not data:
                return logging.debug('Cédula no encontrada: %s-%s', nac, ci)
            logging.debug('Ciudadano encontrado: %(ci)s: %(nombre)s' % data)
            self.database.create(**data)
            return self.get(nac, ci)
        elif (datetime.now() - cedula.consultado).total_seconds() > self.expire:
            for attr, val in self.search(nac, ci).values():
                setattr(cedula, attr, val)
            cedula.consultado = datetime.now()
            cedula.save()

        data = {
            'ci': cedula.ci,
            'nacionalidad': cedula.nacionalidad,
            'cedula': cedula.cedula,
            'nombre': cedula.nombre,
            'estado': cedula.estado,
            'municipio': cedula.municipio,
            'parroquia': cedula.parroquia,
            'centro': cedula.centro,
            'direccion': cedula.direccion
        }

        return data

    def dump(self, probe, show=False):
        for nac, ci in probe._probe():
            data = self.get(nac, ci)
            if show:
                if data:
                    row = []

                    for c in self.f:
                        c = c % data
                        if c == 'None':
                            continue
                        row.append(c)
                    print(', '.join(row))
                else:
                    print('%s-%s: Cédula no registrada.' % (nac, ci))
            probe.counter += 1
            if probe.antiddos:
                time.sleep(probe.antiddos)
        probe.finished = True

    @property
    def complete(self):
        complete = 0
        for probe in self.probe_stack:
            complete += probe.counter
        return (complete, self.total_ci)

    def start(self, show=False):
        for probe in self.gen_probes():
            _thread.start_new(self.dump, (probe, show))

    def stop(self):
        for probe in self.probe_stack:
            probe.stop_probe = True
