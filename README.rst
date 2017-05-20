cnelib
======
¿Que es cnelib?
Es una librería que permite hacer consultas sobre cedulas de identidad
inscritas o no, en el registro del **Consejo Nacional Electoral (CNE)**,
además de tener la capacidad de salvaguardar los datos obtenidos, en una
base de datos local, usando **MySQL**, **SQLite**, **PostgreSQL** como 
motores de base de datos, dando mayores posibilidades, como búsqueda por
nombre, estado, posibilidad de trabajo offline, etc.

=================
Instalando cnelib
=================
Instalando dependencias:
    - pip install -r requirements.txt

Una vez instaladas las dependencias procedemos con la instalación de cnelib:
    - **git clone https://github.com/IsmaelRLG/cnelib.**
    - **# python setup.py install**
    - Ahora a puede ser usado como libreria o en linea de comandos 
    - línea de comandos: **$ cedula --help**

Tambien puede ser instalado mediante pip:
    - **pip install cnelib**

=============
Documentación
=============
Para leer la documentación viste `aquí`__

===========
Aviso Legal
===========

De acuerdo a lo establecido en la `Ley Orgánica del Registro Civil`__, en sus
artículos **6** y **59**, la información contenida en el Registro Civil es de
carácter publico, por lo tanto toda persona puede acceder a la información de
los archivos y datos del Registro Civil, salvo a las limitaciones establecidas
en la Constitución de la Republica, en dicha ley y en demás leyes vigentes.

Este software ha sido desarrollado con la intención comercial o no comercial,
distribuido bajo la `licencia MIT`__, siendo gratuito y otorgando libertades
para usar, copiar y distribuir este software, todo esto para motivar e
incentivar el desarrollo de aplicaciones, realización de investigaciones
o análisis que sean beneficiosos para la sociedad.

=============================
Limitación de responsabilidad
=============================
EN NINGÚN CASO LOS AUTORES O TITULARES DEL COPYRIGHT DE ESTE SOFTWARE SERÁN
RESPONSABLES POR LAS POSIBLES VIOLACIONES A LA CONSTITUCIÓN DE LA REPUBLICA,
LA LEY ORGÁNICA DEL REGISTRO CIVIL Y DEMÁS LEYES VIGENTES, QUE SURJAN DE O
EN CONEXIONES CON EL SOFTWARE, EL USO U OTRO TIPO DE ACCIONES EN EL SOFTWARE.

========
Licencia
========
Copyright (c) 2016-2017 Ismael Lugo

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

__ docs/rst/index.rst
__ http://www.cne.gob.ve/registrocivil/images/publico/LORC_2009.pdf
__ LICENSE
