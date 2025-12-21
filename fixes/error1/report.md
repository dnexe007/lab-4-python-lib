Тип:
* неправильный разбор строĸи или входных данных

Место:
* `main.py`, строка 30

Симптом:
* при начале симуляции вылетает исключение `TypeError: 'str' object cannot be interpreted as an integer`

Как воспроизвести:
* Симуляция `sm 0 100 0`

Отладка:
* Breakpoint:
    1. `main.py`, строка 43 `simulate(start, steps, seed)`
    2. `simulation.py`, строка 69 `for i in range(steps)`
* Информация в отладчике: breakpoint 1 -  переменная `steps`, передаваемая в `simulate(start, steps, seed)` имеет тип `str`, хотя должна приводиться к `int`

Причина:
* `main.py`, строка 30: `steps: int = args[2]` отсутствует приведение к типу `int`

Исправление:
* заменить на `steps: int = int(args[2])`

Проверка:
* данное исключение пропалло, вызывается исключение в другом месте, связанное с другой ошибкой

Доказательства:
* `debugger.png`
* `breakpoint1.png`
* `breakpoint2.png`
* `exception.png`
