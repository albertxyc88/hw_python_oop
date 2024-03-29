# Модуль фитнес - трекера 
## Описание
Модуль рассчитывает и отображает результаты тренировок по плаванию, бегу, спортивной ходьбе. 
Модуль написан с использованием базового класса и классами наследниками. В классах, описывающих любой из видов тренировки, применяются одни и те же свойства и методы, поэтому происходит наследование от базового класса Training, далее каждый класс уже дополняет или расширяет базовый класс.

Выполняет следующие функции:
- принимает от блока датчиков информацию о прошедшей тренировке,
- определяет вид тренировки,
- рассчитывает результаты тренировки,
- выводит информационное сообщение о результатах тренировки.

Последовательность данных в принимаемых пакетах:

Плавание
Код тренировки: 'SWM'.
Элементы списка: количество гребков, время в часах, вес пользователя, длина бассейна, сколько раз пользователь переплыл бассейн.

Бег
Код тренировки: 'RUN'.
Элементы списка: количество шагов, время тренировки в часах, вес пользователя.

Спортивная ходьба
Код тренировки: 'WLK'.
Элементы списка: количество шагов, время тренировки в часах, вес пользователя, рост пользователя.

## Технологии
Python 3.7

## Имитация получения данных в модуль для проверки работоспособности

В модуле __main__ имитирована работа датчиков и передает в программу подготовленные тестовые данные. 

```
if __name__ == '__main__':
    packages = [        
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
```

