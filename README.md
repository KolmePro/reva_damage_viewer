## Для редактирования интерфейса
Используйте **Qt Designer**  
На Windows он обычно в папке виртуального окружения:  
```
<venv>\Lib\site-packages\PySide6\designer.exe
```
Собрать exe-файл:  
```
cd /src
pyinstaller --onefile --noconsole --add-data "resources;resources" main.pyw
```