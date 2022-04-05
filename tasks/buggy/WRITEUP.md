# Альфа-версия: Write-up

Запускаем приложение. Наблюдаем вопрос «Показать флаг? (y/n)». Однако, быстрое изучение показывает, что получить флаг не так-то просто:

```
$ ./get_flag
Показать флаг? (y/n)y

Не положено
$ ./get_flag
Показать флаг? (y/n)n

Ну тогда до свидания
$ ./get_flag
Показать флаг? (y/n)x

Это вообще что такое
```

Для начала изучим код приложения. В этом райтапе мы будем использовать Cutter. Подробнее о Cutter, и вообще о реверс-инжиниринге, можно почитать [в нашем курсе](https://course.ugractf.ru/reverse/nightmare.html). Открыв приложение для изучения, быстро находим в нём функцию `get_flag`. Открыв её, видим следующее:

![Вид функции `get_flag`](writeup/get_flag.png)
 
Весьма странный ассемблерный код! Если же открыть шестнадцатеричный редактор:

![`get_flag` в шестнадцатеричном редакторе](writeup/get_flag_hex.png)

Машинный код функции отсутствует, вместо него область функции заполнена нулевыми байтами (два нулевых байта как раз соответствуют машинному коду инструкции `mox ax, al`).

Попробуем исследовать приложение с другого конца: откроем функцию `main`. Здесь сравнительно короткая функция, которая состоит в основном из вызовов в стандартную библиотеку Си и в библиотеку [zlib](https://zlib.net/), широко используемую для сжатия данных. Завершается код вызовом уже встроенной функции `decide_if_show_flag`. Судя по отсутствию работы с вводом-выводом в `main` и названию встроенной функции можно предположить, что именно она отвечает за вывод запроса на экран. Однако, если перейти к этой функции, перед нами встанет уже знакомая картина: функция замещена нулевыми байтами.

Несмотря на это, приложение каким-то образом всё же работает. Давайте запустим его в отладчике, и изучим его поведение подробнее. Поставим точку останова на вызове `decide_if_show_flag` и запустим приложение в Cutter. Дойдём до созданной точки, и сделаем шаг (горячая клавиша F7). Видим настоящий код функции:

![Код `decide_if_show_flag`](writeup/decide_if_show_flag.png)

Такое возможно только, если приложение модифицирует само себя. Откроем снова функцию `main`. Перезапустим программу, поставив точку останова на начало функции. Пройдём по функции, используя внешний шаг (клавишу F8) и следя за состоянием функции `decide_if_show_flag`. Функция заполняется кодом после вызова `fcn.004003b8`, который при изучении оказывается вызовом `memcpy` (переходим на функцию двойным кликом и затем переходим по адресу функции двойным кликом на параметр `jmp` `qword [reloc.ifunc_4234d0]`). Таким образом делаем вывод, что функция распаковывает где-то сохранённый бинарный код с помощью `zlib` и копирует содержимое прямо в свой исполняемый сегмент, на который затем и переходит. Это — простейшая форма упаковки исполняемых файлов, техники, широко применявшийся во времена медленного интернета, и до сих пор используемой для сокрытия кода вирусов от обнаружения. Наиболее известный в мире упаковщик приложений с открытым исходным кодом — [UPX](https://upx.github.io/).

Однако, нам вовсе не обязательно самостоятельно распаковывать приложение, чтобы разбирать его дальше. Давайте продолжим изучать код программы прямо из отладчика. Процесс будет затруднён тем, что Cutter не мог анализировать упакованный код. Это можно исправить, просто вызвав анализ ещё раз после распаковки, прямо во время работы программы (File → Analyze Program).

Смотрим на функцию `decide_if_show_flag`. Судя по её коду, `get_flag` в ней вообще не вызывается: в этом можно убедиться, используя функцию Cutter «Show X-Refs». Поверхностное изучение содержимого функций `still_no_flag`, `no_flag` и `really_no_flag` показывает, что они просто возвращают строковую константу. Видимо, разработчики оставили `get_flag` в приложении по ошибке, и в тестовой версии её вовсе не должно было быть. Как можно вызвать эту функцию?

Мы видим, что `get_flag` объявлена без параметров (`get_flag ()`). Попробуем вызвать `get_flag` самостоятельно, и затем изучить результат. Запомним адрес функции, то есть адрес первой инструкции после метки `get_flag ()`: `0x00484f97`. Далее остановимся в программе на вызове `call decide_if_show_flag`, чтобы бинарный код уже был распакован. Меняем значение в регистре RIP (на панели регистров справа) на найденный адрес. Мы оказались на начале функции `get_flag`. Используем шаг до выхода (горячая клавиша Ctrl+F8), попадаем на инструкцию `ret` в конце функции. Теперь осталось посмотреть результат. По соглашениям о вызовах для платформы x86_64 результат выполнения функции всегда хранится в регистре RAX. Скорее всего, в нём хранится указатель; для изучения его содержимого откроем контекстное меню для RAX из панели «Registers» и используем «Show in → Hexdump», где сразу видим флаг.

Альтернативно, можно также заменить вызов любой из трёх функций (`still_no_flag`, `no_flag` или `really_no_flag`) на `get_flag` и получить флаг на экран. Для этого находим соответствующую инструкцию `call` и воспользуемся функцией редактирования (Edit → Instruction). В появившемся окне заменим адрес функции на адрес `get_flag` и применим изменения. Чтобы взаимодействовать с программой, запущенной в отладчике Cutter, откроем консоль (Windows → Console). В ней откроем консоль самой программы, выбрав в перечисляемом поле внизу «Debugee Input». Продолжаем выполнение программы, вводим нужную опцию (например, `n`, если вы заменили `no_flag`) и опять же получаем флаг.

Флаг: **ugra_smaller_is_better_6ed9864ba0122e8bdb4175e5d1925389c6136288d**
