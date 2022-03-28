from dataclasses import dataclass, asdict
from typing import Dict, Union, Type, ClassVar


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE: ClassVar[str] = ('Тип тренировки: {training_type}; '
                              'Длительность: {duration:.3f} ч.; '
                              'Дистанция: {distance:.3f} км; '
                              'Ср. скорость: {speed:.3f} км/ч; '
                              'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        """Формирует внешний вид сообщения."""
        return self.MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""

    # расстояние, которое спорстмен преодолевает за один шаг
    LEN_STEP: float = 0.65
    # константа для перевода значений из метров в километры
    M_IN_KM: float = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий.
        Для каждого вида тренировок подсчет калорий свой в своих методах
        поэтому здесь заглушка."""
        raise NotImplementedError(
            'Для каждого вида тренировок свой метод подсчета калорий.')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    # Коэффициенты для расчета калорий при Running
    CALORIE_RATIO_1: float = 18
    CALORIE_RATIO_2: float = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий для тренировки бег."""
        return ((self.CALORIE_RATIO_1 * self.get_mean_speed()
                - self.CALORIE_RATIO_2) * self.weight
                / self.M_IN_KM * (self.duration * 60))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    # Коэффициенты для расчета калорий при SportWalking
    WALK_RATIO_1: float = 0.035
    WALK_RATIO_2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Количество затраченных калорий при спортивной ходьбе."""
        return ((self.WALK_RATIO_1 * self.weight
                + (self.get_mean_speed() ** 2 // self.height)
                * self.WALK_RATIO_2) * (self.duration * 60))


class Swimming(Training):
    """Тренировка: плавание."""

    # расстояние, которое спорстмен преодолевает за один гребок.
    LEN_STEP: float = 1.38
    # константа для перевода значений из метров в километры
    M_IN_KM: float = 1000
    # Коэффициенты для расчета калорий при Swimming
    SWIM_RATIO_1: float = 1.1
    SWIM_RATIO_2: float = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения при плавании."""
        swim_length = self.length_pool * self.count_pool
        return swim_length / self.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        """Количество затраченных калорий при плавании."""
        return ((self.get_mean_speed() + self.SWIM_RATIO_1)
                * self.SWIM_RATIO_2 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    SWIM: str = 'SWM'
    RUN: str = 'RUN'
    SWALK: str = 'WLK'
    workout: Dict[str, Union[Type[Swimming],
                             Type[Running],
                             Type[SportsWalking]]] = {SWIM: Swimming,
                                                      RUN: Running,
                                                      SWALK: SportsWalking}
    try:
        training = workout[workout_type](*data) 
    except KeyError:
        print(f'You entered workout_type {workout_type}, '
              f'but waiting {workout.keys()}')
    return training


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
