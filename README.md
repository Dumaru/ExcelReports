# ExcelReports
Excel reports project with graphical user interface in PyQt5 using pandas

## Creando archivos python desde el xml del designer
pyuic5.exe -x interfaz.ui -o interfazIO.py

> pyuic5 -x .\InicioSubirDatos.ui -o ..\UIPyfiles\InicioSubirDatos.py
> pyuic5 -x .\VistaGeneralDatos.ui -o ..\UIPyfiles\VistaGeneralDatos.py
> pyuic5 -x .\VistaDetalleHoras.ui -o ..\UIPyfiles\VistaDetalleHoras.py
> pyuic5 -x .\VistaFiltros.ui -o ..\UIPyfiles\VistaFiltros.py
> pyuic5 -x .\VistaAnalisisDatos.ui -o ..\UIPyfiles\VistaAnalisisDatos.py

# Proceso genereacion archivo ejecutable .exe
https://pyinstaller.readthedocs.io/en/stable/usage.html

## Sin dependencias
> pip install pyinstaller
> cd filePath
> pyinstaller --onefile filepath
Queda guardado en el dir de pyinstaller 

Se crean carpetas dist y build, el ejecutable esta en dist

Chequear los hooks de pyinstaller y los dlls
git clone https://github.com/pyinstaller/pyinst...
cd pyinstaller
git pull origin +refs/pull/3024/merge
pip install .

Comando pipwin para tener ambiente 
poner en los archivos generados por pyuic5

Ir a C:\Users\robin\anaconda3\Lib\site-packages\PyInstaller\hooks para anclar librerias como pandas

Ir a platforms C:\Users\robin\anaconda3\Library\plugins\platforms


Abrir el pipwin y poner comando > venv -c -i  pyi-env-name
ir hasta el pyinstaller > cd C:\Users\robin\anaconda3\Scripts
y correr el pyinstaller
> pyinstaller --onedir --windowed --name="ExcelReports" "C:\Users\robin\Google Drive\WORK\ExcelReports\ExcelReports\Interfaz\ExcelReports.py"    


Ir al dist y a la applicacion y pegar las librerias de platforms dentro del folder de la app


Opcional
Pyinstaller spec/build/dist location paths can be configured as part of pyinstaller command. Refer below example

Correr comando para generar modulo python con todos los recursos de qrc
pyrcc5 -o images_rc.py images.qrc


pyinstaller --specpath /opt/bk/spec --distpath /opt/bk/dist --workpath /opt/bk/build testscript.py


pyinstaller -n "Hello World" app.py
# or
pyinstaller --name "Hello World" app.py



Manual: https://www.learnpyqt.com/courses/packaging-and-distribution/packaging-pyqt5-pyside2-applications-windows-pyinstaller/



Problemas recursion: Reinstalar openpixl
https://stackoverflow.com/questions/38977929/pyinstaller-creating-exe-runtimeerror-maximum-recursion-depth-exceeded-while-ca