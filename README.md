## Для редактирования интерфейса
Используйте **Qt Designer**.

На Windows он обычно лежит в виртуальном окружении:
```text
<venv>\Lib\site-packages\PySide6\designer.exe
```

## Фильтр-плагины
Плагины фильтров лежат в `src/filter_plugins`.

Приложение загружает каждый `*.py` файл из этой папки и автоматически строит по нему чекбоксы в интерфейсе.
Чтобы добавить новый фильтр, достаточно скопировать существующий файл и изменить список `FILTERS`.

Формат описан в [src/filter_plugins/README.md](src/filter_plugins/README.md).

## Сборка exe
```text
pyinstaller main.spec
```
