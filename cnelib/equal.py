# -*- coding: utf-8 -*-
"""
cnelib - Parseador
Copyright 2016, Ismael R. Lugo G.
"""

ps_txt = {'\xc3\x83\xc2\x93': '\xc3\xb3',  # ó
          '\xc3\x83\xc2\x8d': '\xc3\xad',  # í
          '\xc3\x90': '\xc3\xb1'  # ñ
          }
ls_edo = {'Dtto. Capital': 'Distrito Capital'}
ls_mp = {'Ce. Blvno Libertador': 'Libertador'}
ls_pq = {}


def estado(edo):
    """
    Parsea el nombre del estado, eliminando el prefijo "Edo.", entre otras.
    retorna --> string
    """
    if edo.startswith('Edo. '):
        return edo.split('Edo. ')[1]
    else:
        return ls_edo[edo] if edo in ls_edo else edo


def municipio(mp):
    """
    Parsea el nombre del municipio, eliminando el prefijo "Mp.", entre otras.
    retorna --> string
    """
    if mp.startswith('Mp. '):
        return mp.split('Mp. ')[1]
    else:
        return ls_mp[mp] if mp in ls_mp else mp


def parroquia(pq):
    """
    Parsea el nombre de la parroquia, eliminando el prefijo "Pq." y "Cm.".
    retorna --> string
    """
    if pq.startswith('Pq. '):
        return pq.split('Pq. ')[1]
    elif pq.startswith('Cm. '):
        return pq.split('Cm. ')[1]
    else:
        return ls_pq[pq] if pq in ls_pq else pq


def parse_text(string):
    """
    Parsea el texto, convirtiendo caracteres a unicode.
    retorna --> string
    """
    string = [string]
    for to_find, to_replace in ps_txt.items():
        string[0] = string[0].replace(to_find, to_replace)
    return string[0]