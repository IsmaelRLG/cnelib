=========================
Base de datos y Consultas
=========================
Se dispone de una clase de nombre **cedula** para realizar una mezcla entre
consultas a la base de datos local y consultas a la web.

Clase cedula
------------
**METODOS:**
 **__init__**: Instancia y construye la clase, retorna clase instanciada

 .. table:: **ATRIBUTOS**

   ================ ====================== ====================================
   NOMBRE           TIPO                   DESCRIPCIÓN
   ================ ====================== ====================================
   `web`__          instance               Instancia de consultas web
   `database`__     instance               Instancia de base de datos
   ================ ====================== ====================================
 __ cnelib.web.rst
 __ cnelib.database.rst

 **search**: Busca y retorna tupla con los resultados de la búsqueda

 .. table:: **ATRIBUTOS**

   ================ ====================== ====================================
   NOMBRE           TIPO                   DESCRIPCIÓN
   ================ ====================== ====================================
   nac              string                 Nacionalidad (**V|E**)
   ced              int                    Numero de cedula
   ================ ====================== ====================================

 MODELO DE CONSULTA

 .. code-block::

   CONSULTA─┐
   ┌──╼BASE DE DATOS╾──╼RESULTADOS
   │        ╽
   │     WEB CNE
   │        │┍REGISTRO ELECTORAL┑
   │        ┕┥                  ├┐
   │         ┕REGISTRO CIVIL────┙│
   └─────────────────────────────┘

**EJEMPLOS DE USO**

.. code-block:: python

    >>> import cnelib
    >>> web = cnelib.web.web()
    >>> db = cnelib.database.sqlite_db('/home/user/cne.db')
    >>> cedula = cnelib.blend.cedula(web, db)
    >>> cedula.search('V', 12345678)
    ((12345678, 'V', 'Peppa Pig La Cerdita', None, None, None, None, None),)
    >>> 