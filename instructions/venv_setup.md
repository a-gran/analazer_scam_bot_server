# Настройка виртуального окружения Python

Эта инструкция помогает создать и включить виртуальное окружение `.venv` для проекта.

Виртуальное окружение нужно, чтобы библиотеки проекта устанавливались отдельно от других Python-проектов на компьютере.

Для этого проекта желательно использовать Python `3.12`.

---

# Windows

## 1. Установите Python

1. Откройте PowerShell.
2. Проверьте, установлен ли Python:

```powershell
py --version
```

Если команда не сработала, попробуйте:

```powershell
python --version
```

Если Python не установлен, скачайте его с официального сайта:

```text
https://www.python.org/downloads/
```

При установке обязательно включите галочку `Add python.exe to PATH`.

## 2. Перейдите в папку проекта

В PowerShell выполните команду `cd` и укажите путь к папке проекта.

Пример:

```powershell
cd C:\Users\User\projects\analyzer_scam_bot
```

Проверьте, что вы находитесь в правильной папке:

```powershell
dir
```

В списке файлов должны быть `main.py` и `requirements.txt`.

Если в VS Code выбран терминал `Git Bash`, путь пишется в стиле Linux:

```bash
cd /c/Users/User/projects/analyzer_scam_bot
```

Проверьте папку в Git Bash:

```bash
ls
```

В списке файлов также должны быть `main.py` и `requirements.txt`.

## 3. Создайте виртуальное окружение

Создать окружение нужно один раз:

```powershell
py -m venv .venv
```

Если команда `py` не работает, используйте:

```powershell
python -m venv .venv
```

После выполнения команды в проекте появится папка `.venv`.

## 4. Активируйте виртуальное окружение

В PowerShell выполните:

```powershell
.\.venv\Scripts\Activate.ps1
```

Если окружение включилось, в начале строки терминала появится `(.venv)`.

Если вы используете обычный `cmd`, команда другая:

```cmd
.venv\Scripts\activate.bat
```

Если вы используете `Git Bash` в VS Code, команда такая:

```bash
source .venv/Scripts/activate
```

## 5. Установите зависимости

Когда окружение активно, установите библиотеки проекта:

```powershell
python -m pip install -r requirements.txt
```

В `Git Bash` используется такая же команда:

```bash
python -m pip install -r requirements.txt
```

## 6. Запустите проект

```powershell
python main.py
```

В `Git Bash` команда такая же:

```bash
python main.py
```

## 7. Завершите работу с окружением

Когда работа закончена, можно выйти из окружения:

```powershell
deactivate
```

## Частые проблемы на Windows

### PowerShell запрещает запуск `Activate.ps1`

Если появилась ошибка про `Execution Policy`, выполните:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

После этого снова активируйте окружение:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Команда `python` или `py` не найдена

Обычно причина в том, что Python не установлен или не добавлен в `PATH`.

Что сделать:

1. Переустановите Python с сайта `python.org`.
2. Во время установки включите `Add python.exe to PATH`.
3. Закройте PowerShell и откройте его заново.
4. Проверьте команду:

```powershell
py --version
```

### Окружение включилось, но зависимости не ставятся

Обновите `pip` внутри окружения:

```powershell
python -m pip install --upgrade pip
```

Затем снова выполните:

```powershell
python -m pip install -r requirements.txt
```

### Файл `requirements.txt` не найден

Скорее всего, терминал открыт не в папке проекта.

Проверьте текущую папку:

```powershell
pwd
```

Проверьте список файлов:

```powershell
dir
```

Если `requirements.txt` нет в списке, перейдите в правильную папку проекта через `cd`.

### В VS Code открыт Git Bash, и команда PowerShell не работает

В Git Bash не нужно использовать команду PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Для Git Bash используйте:

```bash
source .venv/Scripts/activate
```

Если путь начинается с диска `C:`, в Git Bash он пишется так:

```bash
cd /c/Users/User/projects/analyzer_scam_bot
```

---

# Linux

## 1. Проверьте Python

Откройте терминал и выполните:

```bash
python3 --version
```

Если команда не работает, попробуйте:

```bash
python --version
```

Для проекта желательно использовать Python `3.12`.

## 2. Установите пакет для `venv`, если он отсутствует

На Ubuntu и Debian иногда нужно отдельно установить модуль `venv`:

```bash
sudo apt update
sudo apt install python3-venv
```

На Fedora обычно достаточно установленного Python. Если `venv` не создается, установите Python-инструменты:

```bash
sudo dnf install python3
```

## 3. Перейдите в папку проекта

Пример:

```bash
cd ~/projects/analyzer_scam_bot
```

Проверьте, что вы в нужной папке:

```bash
ls
```

В списке файлов должны быть `main.py` и `requirements.txt`.

## 4. Создайте виртуальное окружение

```bash
python3 -m venv .venv
```

Если у вас Python запускается командой `python`, используйте:

```bash
python -m venv .venv
```

После выполнения команды появится папка `.venv`.

## 5. Активируйте виртуальное окружение

```bash
source .venv/bin/activate
```

Если окружение включилось, в начале строки терминала появится `(.venv)`.

## 6. Установите зависимости

```bash
python -m pip install -r requirements.txt
```

## 7. Запустите проект

```bash
python main.py
```

## 8. Завершите работу с окружением

```bash
deactivate
```

## Частые проблемы на Linux

### Ошибка `No module named venv`

Установите пакет `python3-venv`:

```bash
sudo apt update
sudo apt install python3-venv
```

Затем заново создайте окружение:

```bash
python3 -m venv .venv
```

### Команда `python` не найдена

На многих Linux-системах Python запускается командой `python3`, а не `python`.

Используйте:

```bash
python3 --version
python3 -m venv .venv
```

После активации окружения команда `python` обычно начинает работать внутри `.venv`.

### Нет прав на установку пакетов

Если окружение активно, `sudo` для установки зависимостей не нужен.

Правильная команда:

```bash
python -m pip install -r requirements.txt
```

Если вы видите ошибку прав, проверьте, что окружение активно и путь к Python указывает на `.venv`:

```bash
which python
```

### Файл `requirements.txt` не найден

Проверьте, что терминал открыт в папке проекта:

```bash
pwd
ls
```

Если файла нет в списке, перейдите в папку проекта через `cd`.

---

# macOS

## 1. Проверьте Python

Откройте Terminal и выполните:

```bash
python3 --version
```

Если команда не работает, попробуйте:

```bash
python --version
```

Для проекта желательно использовать Python `3.12`.

Если Python не установлен, установите его с официального сайта:

```text
https://www.python.org/downloads/macos/
```

Также можно установить Python через Homebrew:

```bash
brew install python
```

## 2. Перейдите в папку проекта

Пример:

```bash
cd ~/projects/analyzer_scam_bot
```

Проверьте, что вы в нужной папке:

```bash
ls
```

В списке файлов должны быть `main.py` и `requirements.txt`.

## 3. Создайте виртуальное окружение

```bash
python3 -m venv .venv
```

Если у вас Python запускается командой `python`, используйте:

```bash
python -m venv .venv
```

После выполнения команды появится папка `.venv`.

## 4. Активируйте виртуальное окружение

```bash
source .venv/bin/activate
```

Если окружение включилось, в начале строки терминала появится `(.venv)`.

## 5. Установите зависимости

```bash
python -m pip install -r requirements.txt
```

## 6. Запустите проект

```bash
python main.py
```

## 7. Завершите работу с окружением

```bash
deactivate
```

## Частые проблемы на macOS

### Команда `python` открывает старую версию или не работает

На macOS чаще всего нужно использовать `python3`:

```bash
python3 --version
python3 -m venv .venv
```

После активации `.venv` используйте команду `python`:

```bash
python --version
```

### Команда `brew` не найдена

Homebrew не установлен. Это не ошибка проекта.

Можно установить Python напрямую с сайта:

```text
https://www.python.org/downloads/macos/
```

### Ошибка при установке зависимостей

Сначала обновите `pip` внутри окружения:

```bash
python -m pip install --upgrade pip
```

Затем снова установите зависимости:

```bash
python -m pip install -r requirements.txt
```

### Файл `requirements.txt` не найден

Проверьте текущую папку и список файлов:

```bash
pwd
ls
```

Если `requirements.txt` нет в списке, перейдите в папку проекта через `cd`.

---

# Проверка, что все работает

После активации окружения выполните:

## Windows

```powershell
where python
python --version
```

## Linux и macOS

```bash
which python
python --version
```

Путь к Python должен указывать на папку `.venv`.

---

# Краткая шпаргалка

## Windows PowerShell

```powershell
cd C:\Users\User\projects\analyzer_scam_bot
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

## Windows Git Bash в VS Code

```bash
cd /c/Users/User/projects/analyzer_scam_bot
py -m venv .venv
source .venv/Scripts/activate
python -m pip install -r requirements.txt
python main.py
```

## Linux

```bash
cd ~/projects/analyzer_scam_bot
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py
```

## macOS

```bash
cd ~/projects/analyzer_scam_bot
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py
```
