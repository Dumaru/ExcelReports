# Proceso genereacion archivo ejecutable .exe
https://pyinstaller.readthedocs.io/en/stable/usage.html

## Sin dependencias
> pip install pyinstaller
> cd filePath
> pyinstaller --onefile filepath
Queda guardado en el dir de pyinstaller 

Se crean carpetas dist y build, el ejecutable esta en dist

## Creando archivo python 
> pyuic5 -x .\InicioSubirDatos.ui -o ..\UIPyfiles\InicioSubirDatos.py
> pyuic5 -x .\VistaGeneralDatos.ui -o ..\UIPyfiles\VistaGeneralDatos.py
> pyuic5 -x .\VistaDetalleHoras.ui -o ..\UIPyfiles\VistaDetalleHoras.py
> pyuic5 -x .\VistaFiltros.ui -o ..\UIPyfiles\VistaFiltros.py
> pyuic5 -x .\VistaAnalisisDatos.ui -o ..\UIPyfiles\VistaAnalisisDatos.py

Chequear los hooks de pyinstaller y los dlls

Comando pipwin para tener ambiente 

> cd C:\Users\robin\Anaconda3\Scripts
> pyinstaller --onedir --windowed pythonFilePathMadeWithPyinstaller
Poner comillas si tiene espacio

Con la carpeta de platforms añadir librerias que estan en anaconda


Opcional
Pyinstaller spec/build/dist location paths can be configured as part of pyinstaller command. Refer below example

pyinstaller --specpath /opt/bk/spec --distpath /opt/bk/dist --workpath /opt/bk/build testscript.py