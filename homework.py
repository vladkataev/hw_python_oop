class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65  # расстояние, которое спортсмен преодолевает за один шаг в метрах
    M_IN_KM: int = 1000     # константа для перевода значений из метров в километры
    H_IN_M: int = 60        # константа для перевода значений из часов в минуты

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        self.action = action        # количество совершённых действий (число шагов при ходьбе и беге либо гребков — при плавании)
        self.duration = duration    # длительность тренировки в часах
        self.weight = weight        # вес спортсмена в килограммах

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        message = InfoMessage(self.__class__.__name__,
                              self.duration,
                              self.get_distance(),
                              self.get_mean_speed(),
                              self.get_spent_calories()
                              )
        return message


class Running(Training):
    """Тренировка: бег."""
    COEFF_CALORIE_1: int = 18   # константа для расчета калорий при беге
    COEFF_CALORIE_2: int = 20   # константа 2 для расчета калорий при беге

    def get_spent_calories(self) -> float:
        self.duration_min = self.duration * self.H_IN_M
        return ((self.COEFF_CALORIE_1 * self.get_mean_speed()
                - self.COEFF_CALORIE_2)
                * self.weight / self.M_IN_KM * self.duration_min)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_CALORIE_1: float = 0.035  # константа для расчета калорий при хотьбе
    COEFF_CALORIE_2: float = 0.029  # константа 2 для расчета калорий при хотьбе

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height    # рост пользователя в сантиметрах

    def get_spent_calories(self) -> float:
        self.duration_min = self.duration * self.H_IN_M
        return ((self.COEFF_CALORIE_1 * self.weight
                + (self.get_mean_speed()**2 // self.height)
                * self.COEFF_CALORIE_2 * self.weight) * self.duration_min)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38          # расстояние, преодолеваемое за один гребок при плавании в метрах
    COEFF_CALORIE_1: float = 1.1    # константа для расчета калорий при плавании
    COEFF_CALORIE_2: int = 2        # константа 2 для расчета калорий при плавании

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool  # длинна бассейна в метрах
        self.count_pool = count_pool    # сколько раз пользователь переплыл бассейн

    def get_mean_speed(self) -> float:
        return (self.length_pool
                * self.count_pool / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed()
                + self.COEFF_CALORIE_1) * self.COEFF_CALORIE_2 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_type_dict = {'SWM': Swimming,
                         'RUN': Running,
                         'WLK': SportsWalking}

    if workout_type in workout_type_dict.keys():
        return workout_type_dict[workout_type](*data)
    raise ValueError('Несуществующий тип тренировки')


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
