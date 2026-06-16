# Git на Windows для одного человека

Эта инструкция описывает простой сценарий работы с Git и GitHub на Windows.

Сценарий такой:

1. Вы один работаете над проектом.
2. Используется только одна ветка: `main`.
3. Вы сохраняете изменения в Git через `commit`.
4. Вы отправляете изменения на GitHub через `push`.
5. Вы забираете изменения с GitHub через `pull`.

---

# 1. Что нужно установить один раз

## 1.1. Установите Git для Windows

Скачайте Git с официального сайта:

```text
https://git-scm.com/download/win
```

Во время установки можно оставлять стандартные настройки.

После установки откройте PowerShell и проверьте Git:

```powershell
git --version
```

Если версия появилась, Git установлен правильно.

## 1.2. Настройте имя и email

Git должен знать, кто делает коммиты.

В PowerShell выполните:

```powershell
git config --global user.name "Ваше имя"
git config --global user.email "your_email@example.com"
```

Проверьте настройки:

```powershell
git config --global --list
```

Email лучше указывать тот же, который используется в GitHub.

---

# 2. Как создать репозиторий на GitHub

1. Откройте сайт GitHub.
2. Нажмите `New repository`.
3. Введите имя репозитория, например `analyzer_scam_bot`.
4. Выберите `Public` или `Private`.
5. Не ставьте галочки `Add a README file`, `.gitignore`, `license`, если проект уже есть на компьютере.
6. Нажмите `Create repository`.

После создания GitHub покажет ссылку на репозиторий.

Для HTTPS она выглядит примерно так:

```text
https://github.com/ВАШ_ЛОГИН/analyzer_scam_bot.git
```

---

# 3. Как создать Git-репозиторий из готовой папки проекта

## 3.1. Откройте PowerShell в папке проекта

Перейдите в папку проекта:

```powershell
cd C:\Users\User\projects\analyzer_scam_bot
```

Проверьте, что вы в нужной папке:

```powershell
dir
```

В списке файлов должны быть файлы проекта, например `main.py`, `README.md`, `requirements.txt`.

## 3.2. Создайте локальный Git-репозиторий

```powershell
git init
```

## 3.3. Назовите основную ветку `main`

```powershell
git branch -M main
```

В этом документе используется только ветка `main`.

## 3.4. Посмотрите состояние проекта

```powershell
git status
```

Git покажет файлы, которые пока не сохранены в истории.

## 3.5. Добавьте файлы в будущий коммит

```powershell
git add .
```

Команда добавляет все файлы текущего проекта.

## 3.6. Сделайте первый коммит

```powershell
git commit -m "first commit"
```

Коммит — это сохраненная точка в истории проекта.

## 3.7. Подключите GitHub-репозиторий

Замените ссылку на свою ссылку из GitHub:

```powershell
git remote add origin https://github.com/ВАШ_ЛОГИН/analyzer_scam_bot.git
```

Проверьте, что ссылка добавилась:

```powershell
git remote -v
```

## 3.8. Отправьте проект на GitHub

```powershell
git push -u origin main
```

При первом `push` GitHub может попросить войти в аккаунт через браузер.

После успешной отправки обновите страницу репозитория на GitHub. Там должны появиться файлы проекта.

---

# 4. Как каждый день сохранять и отправлять изменения

Этот порядок используется каждый раз, когда вы изменили файлы и хотите отправить их на GitHub.

## 4.1. Посмотрите, какие файлы изменились

```powershell
git status
```

## 4.2. Добавьте изменения

Добавить все изменения:

```powershell
git add .
```

Или добавить один конкретный файл:

```powershell
git add main.py
```

## 4.3. Сделайте коммит

```powershell
git commit -m "описание изменений"
```

Примеры нормальных сообщений:

```powershell
git commit -m "add project setup instructions"
git commit -m "fix question validation"
git commit -m "update README"
```

## 4.4. Отправьте изменения на GitHub

```powershell
git push
```

После первого `git push -u origin main` обычно достаточно писать просто `git push`.

---

# 5. Как забрать изменения с GitHub

Если вы работали на другом компьютере или изменяли файлы прямо на GitHub, перед новой работой заберите свежую версию:

```powershell
git pull
```

Лучше делать `pull` перед началом работы:

```powershell
git pull
git status
```

Если Git ответил `Already up to date`, значит локальная папка уже совпадает с GitHub.

---

# 6. Самый частый рабочий порядок

## Начали работу

```powershell
git pull
git status
```

## Изменили файлы

```powershell
git status
git add .
git commit -m "описание изменений"
git push
```

## Проверили историю

```powershell
git log --oneline -5
```

---

# 7. Частые проблемы на Windows

## Git не найден

Если PowerShell пишет, что `git` не является командой, Git не установлен или PowerShell был открыт до установки.

Что сделать:

1. Установите Git с сайта `git-scm.com`.
2. Закройте PowerShell.
3. Откройте PowerShell заново.
4. Проверьте команду:

```powershell
git --version
```

## GitHub просит логин и пароль

GitHub больше не принимает обычный пароль для Git-операций.

Обычно при `git push` открывается окно входа GitHub в браузере. Войдите в аккаунт и разрешите доступ.

Если Git просит пароль прямо в терминале, используйте вход через браузер или настройте Personal Access Token на GitHub.

## Ошибка `remote origin already exists`

Это значит, что ссылка на GitHub уже добавлена.

Посмотрите текущую ссылку:

```powershell
git remote -v
```

Если ссылка неправильная, замените ее:

```powershell
git remote set-url origin https://github.com/ВАШ_ЛОГИН/analyzer_scam_bot.git
```

## Ошибка при `git push`: сначала нужно сделать `pull`

Если на GitHub есть изменения, которых нет на компьютере, выполните:

```powershell
git pull
```

Затем снова отправьте изменения:

```powershell
git push
```

## После `git pull` появился конфликт

Конфликт бывает, когда один и тот же файл изменен и на компьютере, и на GitHub.

Git покажет файл с конфликтом. Откройте его и найдите такие строки:

```text
<<<<<<< HEAD
ваша версия
=======
версия с GitHub
>>>>>>> origin/main
```

Оставьте правильный вариант текста, удалите строки `<<<<<<<`, `=======`, `>>>>>>>`, затем выполните:

```powershell
git add .
git commit -m "resolve conflict"
git push
```

## Случайно добавили лишний файл

Если файл добавлен через `git add`, но коммит еще не сделан, уберите его из будущего коммита:

```powershell
git restore --staged имя_файла
```

Например:

```powershell
git restore --staged .env
```

## Нужно понять, что сейчас происходит

Используйте эти команды:

```powershell
git status
git remote -v
git branch
git log --oneline -5
```

В нормальной ситуации команда `git branch` должна показывать только ветку `main`.

---

# 8. Краткая шпаргалка

## Первый запуск проекта в Git

```powershell
cd C:\Users\User\projects\analyzer_scam_bot
git init
git branch -M main
git add .
git commit -m "first commit"
git remote add origin https://github.com/ВАШ_ЛОГИН/analyzer_scam_bot.git
git push -u origin main
```

## Обычная отправка изменений

```powershell
git status
git add .
git commit -m "описание изменений"
git push
```

## Обычное получение изменений

```powershell
git pull
```
