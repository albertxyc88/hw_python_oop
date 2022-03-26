from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Формирует внешний вид сообщения."""
        message = (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration:.3f} ч.; '
            f'Дистанция: {self.distance:.3f} км; '
            f'Ср. скорость: {self.speed:.3f} км/ч; '
            f'Потрачено ккал: {self.calories:.3f}.'
            )
        return message


class Training:
    """Базовый класс тренировки."""
    # расстояние, которое спорстмен преодолевает за один шаг
    LEN_STEP: float = 0.65
    # константа для перевода значений из метров в километры
    M_IN_KM: int = 1000
    # Коэффициенты для расчета калорий при Running
    calorie_ratio_1 = 18
    calorie_ratio_2 = 20
    # Коэффициенты для расчета калорий при SportWalking
    walk_ratio_1 = 0.035
    walk_ratio_2 = 0.029
    # Коэффициенты для расчета калорий при Swimming
    swim_ratio_1 = 1.1
    swim_ratio_2 = 2

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
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        distance = Training.get_distance(self)
        middle_speed = distance / self.duration
        return middle_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий.
        Для каждого вида тренировок подсчет калорий свой в своих методах
        поэтому здесь заглушка pass."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий для тренировки бег."""
        run_calories = ((self.calorie_ratio_1 * Training.get_mean_speed(self) -
                        self.calorie_ratio_2) * self.weight /
                        self.M_IN_KM * (self.duration * 60))
        return run_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
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
        walk_calories = ((self.walk_ratio_1 * self.weight +
                         (Training.get_mean_speed(self) ** 2 // self.height) *
                         self.walk_ratio_2) * (self.duration * 60))
        return walk_calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    M_IN_KM: int = 1000

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
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения при плавании."""
        middle_speed = self.length_pool * self.count_pool
        middle_speed = middle_speed / self.M_IN_KM / self.duration
        return middle_speed

    def get_spent_calories(self) -> float:
        """Количество затраченных калорий при плавании."""
        swim_calories = Swimming.get_mean_speed(self) + self.swim_ratio_1
        swim_calories = swim_calories * self.swim_ratio_2 * self.weight
        return swim_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    return workout[workout_type](*data)


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
