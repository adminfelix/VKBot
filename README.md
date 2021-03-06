## VKBot 

Данное приложение является ботом для социальной сети [ВКонтакте](https://vk.com) и предназначено для ответа на сообщения (на данном этапе)

Приложение написано на языке python версии 2.7 с использованием фреймворка [Kivy](https://kivy.org).
Предполагается использование на OC android, но работа возможна и на других платформах.

<img height="600" src="https://github.com/Fogapod/VKBot/blob/master/data/images/screenshots/main_screen.png" 
align="center"/>

## Использованы библиотеки:
* [vk_api](https://github.com/python273/vk_api)
* [kivy-toaster](https://github.com/knappador/kivy-toaster)

***

## Руководство к использованию

> Руководство написано для версии [0.1.0](https://github.com/Fogapod/VKBot/releases/tag/v0.1.0) и может не соответствовать функционалу других версий

### Начало работы
После запуска приложения нажимаем на кнопку включения бота. Если всё работает нормально, появится окно, предлагающее авторизироваться. Без авторизации бот не может начать работать. 
> Приложение имеет открытый исходный код. Сохранность данных авторизации гарантирована.

После запуска и активации можно ознакомиться с разделом `help`. Для этого нужно выполнить команду `/help`  
> `/` является одним из стандартных обращений к боту. Оно может быть любым, я использую его здесь для удобства

### Пользовательские команды
Бот поддерживает создание и использование своих команд. Их можно добавлять двумя способами. Через интерфейс и сообщения.

> Для работы пользовательских команд необхоимо включить их поддержку через настройки приложения.
Регистр команды не учитывается.

##### Интерфейс
<img height="300" src="https://github.com/Fogapod/VKBot/blob/master/data/images/screenshots/command_edit_popup.png"/>

Для работы с пользовательскими командами в интерефейсе необходимо перейти на экран их настройки из главного экрана приложения. Изначально никаких команд нет. Это можно исправить, добавив несколько.
Каждая команда содержит 5 опций, переключаемых кнопками ниже поля `ответ`

> Каждая из опций может находиться в двух (0, 2) или трёх (0, 1, 2) состояниях. 0 - красный цевт, 1 - синий, 2 - зелёный.

| Иконка | Описание | Красный (0) | Синий (1) | Зелёный (2) |
|--------|----------|-------------|-----------|-------------|
| <img height="25" src="https://github.com/Fogapod/VKBot/blob/master/data/images/screenshots/button_use_regex_option.png"/> | Использовать regex | Нет | - | Да |
| <img height="25" src="https://github.com/Fogapod/VKBot/blob/master/data/images/screenshots/button_force_unmark_option.png"/> | Помечать сообщение | Да | - | Нет |
| <img height="25" src="https://github.com/Fogapod/VKBot/blob/master/data/images/screenshots/button_force_forward_option.png"/> | Пересылать сообщение | Стандартно | Никогда | Всегда |
| <img height="25" src="https://github.com/Fogapod/VKBot/blob/master/data/images/screenshots/button_appeal_only_option.png"/> | Условие ответа | Всегда | Без обращения | При обращении (`Бот, команда`) |
| <img height="25" src="https://github.com/Fogapod/VKBot/blob/master/data/images/screenshots/button_disable_option.png"/> | Отключить команду | Нет | - | Да |

##### Сообщения
<img height="300" src="https://github.com/Fogapod/VKBot/blob/master/data/images/screenshots/learn-forgot_commands.png"/>

Пользовательские команды можно настраивать через сообщения. 
Для добавления команды или ответа для существующей команды используется команда `/learn команда::Ответ::опции`

> Опции представляют из себя последовательность из 5 цифр. Каждая из них соответствует опции из интерфейса и принимает соответствующие значения (0, 2) или (0, 1, 2). Стандартное значение опций - `00000`

Удаление всей команды производится командой `/forgot команда`. Удаление ответа производится через `/forgot команда::Ответ`

### OpenWeatherMap
Для работы команды `погода` необходимо зарегистрироваться на сайте https://openweathermap.org ([скриншот](https://github.com/Fogapod/VKBot/blob/master/data/images/screenshots/openweathermap_instruction_1.png))
После этого нужно перейти в раздел [ключей api](https://home.openweathermap.org/api_keys) и скопировать ваш ключ ([скриншот](https://github.com/Fogapod/VKBot/blob/master/data/images/screenshots/openweathermap_instruction_2.png))  

Далее используйте команду `/погода ваш_ключ`. Готово.
> От момента создания аккаунта до начала работы ключа может пройти от 10 до 60 минут. Если бот ругается на неправильность ключа, немного подождите и попробуйте ещё раз.

> Для сброса ключа используется команда `/погода -`

### Вложения
Пользовательские команды поддерживают вложения. Для их отправки в ответе необходимо указать `{attach=https://vk.com/photo12345_6789}` или `{attach=photo12345_6789}` 
Указывать подобным образом можно только на свои вложения из вк. Так же можно указать ссылку на альбом. В этом случае будет выбрана случайная фотография из альбома. Поддерживаются до 10 вложений для одного сообщения.

### Ссылки на команды
Пользовательские команды могут вызывать другие команды. Для этого в ответе нужно указать `self=привет` (будет использован ответ и опции команды `_привет`)

### События беседы
Для того, чтобы бот ответил на событие беседы (изменено название, пользователь вышел, ... ), нужно создать команду `event=...`.

Список возможных событий:
* `event=photo updated` обновлена обложка беседы
* `event=photo removed` удалена обложка беседы
* `event=chat created` создана новая беседа
* `event=title updated` обновлено название беседы (доступен ключ `{event_text}`)
* `event=user joined` пользователь приглашён/вернулся (доступны ключи `{event_user_id}`и `{event_user_name}`)
* `event=user kicked` пользователь удалён/вышел (доступны ключи `{event_user_id}`и `{event_user_name}`)

### Ключи ответов
В ответе для команды можно указать ключ, заключённый в фигурные скобки `{}`. Бот вставит на это место соответстующий текст.

Список доступных на данный момент ключей (будет пополняться):
* `{version}`: текущая версия бота
* `{author}`: имя и ссылка создателя бота
* `{time}`: текущее время (время определяется в момент отправки сообщения и может быть не актуальным на момент доставки)
* `{appeal}`: одно из обращений к боту (рандомно)
* `{appeals}}` все обращения к боту, разделённые двумя пробеламм
* `{bot_name}` имя бота (указывается в настройках)
* `{my_id}` id аккаунта, на котором запущен бот
* `{my_name}` имя аккаунта, на котором запущен бот
* `{user_id}` id аккаунта, от которого пришло сообщение
* `{user_name}` имя аккаунта, от которого пришло сообщение
* `{random_user_id}` id случайного пользователя из беседы (и диалога)
* `{random_user_name}` имя случайного пользователя из беседы (и диалога)
* `{chat_name}` название беседы
* `{event_text}` текст события
* `{event_user_id}` id пользователя, который вышел/приглашён в беседу
* `{event_user_name}` имя пользователя, который вышел/приглашён в беседу
* `{randomXXX}` случайное число от 0 до XXX
* `{idXXX_name}` имя пользователя (группы или беседы) с id XXX

### Работа со стикерами
Бот поддерживает приём и отправку стикеров. Если вы хотите отправить стикер, используйте ключ `{sticker=XXX}`, где XXX является id стикера. Можно указать несколько ключей со стикерами, тогда будет выбран случайный.
> Бот ничего не отправит, если его у вас нет нужного стикера.

Для того, чтобы бот ответил на стикер, в команде необходимо указать `sticker=XXX:YYY`, где XXX - номер набора, а YYY - id стикера.
Возможно использовать паттерн `^sticker=XXX:\d+$` (включена опция `use_regex`)  
В данном случае бот будет отвечать на любой стикер из данного набора.
> Полезная команда: `^sticker=(?P<gid>\d+):(?P<id>\d+)$` ответ: `Стикер {id} из набора {gid}`  
> С помощью этой команды можно получить id всех нужных вам наборов и стикеров.

### Регулярные выражения (regex)
Язык регулярных выражений - поиск совпадений в тексте по определённым правилам.  
Документация по регулярным выражениям: <https://docs.python.org/2/library/re.html>  
Проверка своих регулярных выражений: <http://pythex.org>  

Бот поддерживает группы регулярного выражения. Для использования части полученного сообщения, в ответе необходимо указать `{имя_группы}`, если используется группа с названием. Так же поддерживаются простые группы, которые доступны через `{}` (не забудьте исключить лишние группы через `(?:)` в регулярном выражении. Количество возвращаемых групп не ограничено.
