from unit import BaseUnit

class BaseSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Arena(metaclass=BaseSingleton):
    STAMINA_PER_ROUND = 1
    player = None
    enemy = None
    game_is_running = False
    battle_result = "Битва не окончена"

    def start_game(self, player: BaseUnit, enemy: BaseUnit):
        # TODO НАЧАЛО ИГРЫ -> None
        # TODO присваиваем экземпляру класса аттрибуты "игрок" и "противник"
        # TODO а также выставляем True для свойства "началась ли игра"

        self.player = player
        self.enemy = enemy
        self.game_is_running = True

    def _check_players_hp(self):
        # TODO ПРОВЕРКА ЗДОРОВЬЯ ИГРОКА И ВРАГА
        # TODO проверка здоровья игрока и врага и возвращение результата строкой:
        # TODO может быть три результата:
        # TODO Игрок проиграл битву, Игрок выиграл битву, Ничья и сохраняем его в аттрибуте (self.battle_result)
        # TODO если Здоровья игроков в порядке то ничего не происходит

        if self.player.hp <= 0 and self.enemy.hp <= 0:
            self.battle_result = "В этой битве ничья!"
            return self._end_game()
        elif self.enemy.hp <= 0:
            self.battle_result = "В этой битве вы победили!"
            return self._end_game()
        elif self.player.hp <= 0:
            self.battle_result = "В этой битве вы проиграли!"
            return self._end_game()

    def _stamina_regeneration(self):
        # TODO регенерация здоровья и стамины для игрока и врага за ход

        self.player.add_stamina(self.STAMINA_PER_ROUND)
        self.enemy.add_stamina(self.STAMINA_PER_ROUND)


    def next_turn(self):
        # TODO СЛЕДУЮЩИЙ ХОД -> return result | return self.enemy.hit(self.player)
        # TODO срабатывает когда игрок пропускает ход или когда игрок наносит удар.
        # TODO создаем поле result и проверяем что вернется в результате функции self._check_players_hp
        # TODO если result -> возвращаем его
        # TODO если же результата пока нет и после завершения хода игра продолжается,
        # TODO тогда запускаем процесс регенерации стамины и здоровья для игроков (self._stamina_regeneration)
        # TODO и вызываем функцию self.enemy.hit(self.player) - ответный удар врага

        result = self._check_players_hp()
        if result:
            return result
        self._stamina_regeneration()
        self.enemy.hit(self.player)
        return self.enemy.hit(self.player)


    def _end_game(self):
        # TODO КНОПКА ЗАВЕРШЕНИЕ ИГРЫ - > return result: str
        # TODO очищаем синглтон - self._instances = {}
        # TODO останавливаем игру (game_is_running)
        # TODO возвращаем результат

        self._instances = {}
        self.game_is_running = False
        return self.battle_result

    def player_hit(self):
        # TODO КНОПКА УДАР ИГРОКА -> return result: str
        # TODO получаем результат от функции self.player.hit
        # TODO запускаем следующий ход
        # TODO возвращаем результат удара строкой

        result = self.player.hit(self.enemy)
        self.next_turn()
        return result

    def player_use_skill(self):
        # TODO КНОПКА ИГРОК ИСПОЛЬЗУЕТ УМЕНИЕ
        # TODO получаем результат от функции self.use_skill
        # TODO включаем следующий ход
        # TODO возвращаем результат удара строкой

        result = self.player.use_skill(self.enemy)
        self.next_turn()
        return result
