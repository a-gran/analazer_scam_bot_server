# Полезные расширения для VS Code

Эта инструкция помогает установить расширения VS Code, которые пригодятся для работы с Python-проектом, Markdown-файлами и Git Bash.

---

# 1. Как открыть список расширений

1. Откройте VS Code.
2. Нажмите на значок `Extensions` слева.
3. Или нажмите горячие клавиши:

```text
Ctrl + Shift + X
```

4. В строке поиска введите название расширения.
5. Нажмите `Install`.

---

# 2. Python

Расширение `Python` нужно для нормальной работы с файлами `.py`.

Оно помогает:

1. Подсвечивать Python-код.
2. Показывать ошибки в коде.
3. Запускать Python-файлы.
4. Выбирать виртуальное окружение `.venv`.
5. Удобнее работать с подсказками по коду.

Что искать в VS Code:

```text
Python
```

Обычно нужное расширение называется `Python` и выпущено Microsoft.

После установки можно выбрать Python из виртуального окружения:

1. Нажмите `Ctrl + Shift + P`.
2. Введите `Python: Select Interpreter`.
3. Выберите интерпретатор из папки `.venv`.

---

# 3. Code Runner

Расширение `Code Runner` позволяет быстро запускать небольшие файлы и фрагменты кода.

Что искать в VS Code:

```text
Code Runner
```

Когда расширение установлено, в правом верхнем углу редактора появляется кнопка запуска.

Важно: для проекта лучше запускать основной файл через терминал:

```powershell
python main.py
```

`Code Runner` удобен для быстрых проверок, но не всегда правильно использует виртуальное окружение `.venv`.

---

# 4. Markdown Preview Enhanced

Расширение `Markdown Preview Enhanced` помогает удобно смотреть, как будет выглядеть Markdown-файл.

Что искать в VS Code:

```text
Markdown Preview Enhanced
```

Оно полезно для файлов инструкций, например:

```text
README.md
venv_setup.md
team_git_guide.md
vscode_extensions.md
```

После установки можно открыть расширенный предпросмотр Markdown через командную палитру:

```text
Ctrl + Shift + P
```

Затем найдите команду:

```text
Markdown Preview Enhanced: Open Preview
```

Также в VS Code есть встроенный предпросмотр Markdown.

Чтобы открыть обычный предпросмотр текущего `.md` файла, нажмите:

```text
Ctrl + Shift + V
```

---

# 5. Git Bash

Git Bash обычно устанавливается вместе с `Git for Windows`.

Это не всегда отдельное расширение VS Code. Чаще всего нужно просто выбрать Git Bash как терминал внутри VS Code.

## Как выбрать Git Bash в VS Code

1. Откройте VS Code.
2. Нажмите `Ctrl + Shift + P`.
3. Введите:

```text
Terminal: Select Default Profile
```

4. Выберите `Git Bash`.
5. Откройте новый терминал через:

```text
Ctrl + Shift + `
```

Если `Git Bash` не появился в списке, установите Git для Windows:

```text
https://git-scm.com/download/win
```

После установки перезапустите VS Code.

---

# 6. Quick Print

Расширение `Quick Print` удобно, если нужно быстро распечатать файл из VS Code.

Что искать в VS Code:

```text
Quick Print
```

После установки обычно можно открыть командную палитру:

```text
Ctrl + Shift + P
```

Затем найти команду печати по слову:

```text
Print
```

Если `Quick Print` не подходит или не находится, можно искать похожие расширения по словам:

```text
Print
```

---

# 7. Краткая шпаргалка

Откройте расширения:

```text
Ctrl + Shift + X
```

Установите:

```text
Python
Code Runner
Markdown Preview Enhanced
Quick Print
```

Для Git Bash:

```text
Ctrl + Shift + P
Terminal: Select Default Profile
Git Bash
```

После установки расширений лучше перезапустить VS Code.
