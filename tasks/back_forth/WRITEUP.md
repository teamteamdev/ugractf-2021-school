# Безопасный чат: Write-up

Запустив приложение, видим в терминале следующие сообщения:

```
Creating secure connection
Party 1 started, using secure channel
Party 2 started, using secure channel
```
На этом всё взаимодействие с пользователем заканчивается, но программа висит.

Дизассемблировав приложение, мы увидим большое количество системных вызовов начиная с `main`. Среди них как минимум `fork()`, `read()` и `write()`, что намекает, что внутри приложения происходит больше, чем наблюдается снаружи — как минимум, что оно создаёт дочерний процесс.

Для исследования приложений, активно взаимодействующих с системой, в Linux есть утилита `strace`, которая выводит на экран все системные вызовы, выполняемые программой. Похожая утилита для Windows называется [Process Monitor](https://docs.microsoft.com/en-us/sysinternals/downloads/procmon). Подробнее про этот тип утилит для исследования можно почитать [в нашем курсе](https://course.ugractf.ru/reverse/normal.html). Автор крайне рекомендует начинать исследование неизвестных взаимодействующих с системой приложений именно с неё, а не с изучения кода.

Запустим утилиту, сразу же наблюдаем флаг:

```
$ strace ./secure_chat
...
write(4, "ugra_obscure_unix_security_b871c"..., 70) = 70
write(4, "\n", 1)                       = 1
read(4, "\320\272\321\200\321\203\321\202\320\276 \321\201\320\277\320\260\321\201\320\270\320\261\320\276. \320\277\320\276\320"..., 1024) = 45
write(4, "\320\274\320\276\320\266\320\265\320\274 \320\277\320\276\320\262\321\202\320\276\321\200\320\270\321\202\321\214.", 30) = 30
write(4, "\n", 1)                       = 1
clock_nanosleep(CLOCK_REALTIME, 0, {tv_sec=3, tv_nsec=0},
```

Чтобы получить флаг полностью, воспользуемся ключом `-s`, который убирает ограничение на длину выводимых строк.

Известный автору альтернативный, более сложный путь решения заключался в классическом для задач на реверс использовании отладчика. Нужно было найти функцию `get_flag` (для этого были заботливо оставлены отладочные символы) и поискать её вызовы (воспользовавшись, например, функцией «Show X-Refs» в Cutter). Затем поставить точку останова сразу после её вызова, и прочитать из памяти по указателю в RAX заветный флаг.

Флаг: **ugra_obscure_unix_security_b871c3fd68ad058c8e534b3ae9e7defcaa641121f5a**
