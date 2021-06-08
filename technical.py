class Game:
    def __init__(self, row_spawn, col_spawn, rows, cols,):
        self.map = list(map(lambda x: [None] * cols, range(rows)))
        self.total_rows, self.total_cols = rows, cols
        self.snake_body = [[None, (row_spawn, col_spawn)]]
        self.map[row_spawn][col_spawn] = 'head_snake'
        self.list_object = {
            'apple': {
                'type': 'food',
                'price': 1,
                'player': False
            },
            'big_apple': {
                'type': 'food',
                'price': 2,
                'player': False
            },
            'spoiled_apple': {
                'type': 'food',
                'price': -1,
                'player': False
            },
            'big_spoiled_apple': {
                'type': 'food',
                'price': -2,
                'player': False
            },
            'snake_body': {
                'type': 'no_food',
                'player': True
            },
            'head_snake': {
                'type': 'no_food',
                'player': True
            },
            'wall': {
                'type': 'no_food',
                'player': False
            },
            None: {
                'type': 'void',
                'player': False
            }
        }

    def moving_the_snake(self, direction):
        """Перемещает змейку и возвращает True, если ход корректен.
        Moves the snake and returns True if the move is correct."""
        price_food = False
        checking_the_correct_direction = {
            '+col': '-col',
            '-col': '+col',
            '+row': '-row',
            '-row': '+row'
        }
        # Проверка на обратное направление.
        # Check for reverse direction.
        if checking_the_correct_direction[direction] == self.snake_body[0][0]:
            direction = checking_the_correct_direction[direction]
        # Изменяем направление взгляда головы.
        # Change the direction of the head's gaze.
        self.snake_body[0][0] = direction
        # Изменяем направление взгляда всего тела, кроме головы.
        # Change the direction of view of the entire body, except for the head.
        for index_element in range(len(self.snake_body)):
            if index_element != 0:
                self.snake_body[index_element][0] = check_for_items_nearby(self.snake_body, index_element)
        # Перемещаем каждый элемент по направлению взгляда элемента.
        # Move each element in the direction of the element's view.
        for index_element, (direction, (row, col)) in enumerate(self.snake_body):
            # Снимаем значок с карты.
            # Remove the icon from the map.
            self.map[row][col] = None
            new_coordinate_element = {
                '-col': (row, col - 1),
                '+col': (row, col + 1),
                '-row': (row - 1, col),
                '+row': (row + 1, col)
            }
            # Новые координаты по направлению взгляда элемента.
            # New coordinates in the view direction of the element.
            row, col = new_coordinate_element[direction]
            # Изменяем координаты старого элемента.
            # Changing the coordinates of the old element.
            coordinate_element_old = self.snake_body[index_element - 1][1]
            # Если элемент наступает на другой, то выходим из цикла.
            # If an element steps on another one, we exit the loop.
            if index_element != 0 and (row, col) == coordinate_element_old:
                break
            # Заходим, если это голова змеи.
            # Go in if it's a snake's head.
            if index_element == 0:
                # Проверка на выход из границ.
                # Check for getting out of bounds.
                if not (0 <= row < self.total_rows and 0 <= col < self.total_cols):
                    return False
                item = self.map[row][col]
                # Проверка на корректный ход (item должен быть едой).
                # Check for the correct move (item must be food).
                if self.list_object[item]['type'] == 'no_food':
                    return False
                # По направлению будет еда, то нужно увеличить или уменьшить змейку.
                # In the direction of the food, you need to increase or decrease the snake.
                if self.list_object[item]['type'] == 'food':
                    # цена еды.
                    # the price of food.
                    price_food = self.list_object[item]['price']
                    if price_food > 0:
                        # Увеличиваем змейку.
                        # Increase the snake.
                        for _ in range(price_food):
                            self.snake_body.append(self.snake_body[-1].copy())
                    else:
                        # Уменьшаем змейку.
                        # Reduce the snake.
                        for _ in range(-price_food):
                            row_, col_ = self.snake_body[-1][1]
                            self.map[row_][col_] = None
                            del self.snake_body[-1]
                            # Если змеи нет, то проигрыш.
                            # If there is no snake, then you lose.
                            if not self.snake_body:
                                return False
            # Изменяем координаты элемента.
            # Changing the coordinates of the element.
            self.snake_body[index_element][1] = (row, col)
        # Заполняем список новыми данными.
        # Fill the list with new data.
        for index_element, element in enumerate(self.snake_body):
            row, col = element[1]
            self.map[row][col] = 'head_snake' if (index_element == 0 or
                                                  self.map[row][col] == 'head_snake') else 'snake_body'
        return True, price_food

    def add_an_item_to_the_map(self, name, spawn_row, spawn_col):
        """Добавляет на карту объект.
        Adds an object to the map."""
        item = self.list_object.get(name, False)
        if item and not item['player'] and self.map[spawn_row][spawn_col] is None:
            self.map[spawn_row][spawn_col] = name
            return True
        return False

    def get_list_object(self):
        """Получить список объектов.
        Get a list of objects."""
        return self.list_object


def check_for_items_nearby(snake_body, index_element):
    """Проверяет, что нет ли соседних элементов.
    Checks whether there are no neighboring elements."""
    # Распаковка.
    # Unpack.
    direction_the_original, (row_the_original, col_the_original) = snake_body[index_element]
    # Список направлений, по которым может стоять объект.
    # List of directions in which the object can stand.
    while_list_direction = {
        '-col': ('+row', '-row'),
        '+col': ('+row', '-row'),
        '-row': ('+col', '-col'),
        '+row': ('+col', '-col')
    }
    # Перебираем "белые" направления.
    # Going through the "white" directions.
    for direction in while_list_direction[direction_the_original]:
        new_coordinate_element = {
            '-col': (row_the_original, col_the_original - 1),
            '+col': (row_the_original, col_the_original + 1),
            '-row': (row_the_original - 1, col_the_original),
            '+row': (row_the_original + 1, col_the_original)
        }
        row, col = new_coordinate_element[direction]
        if snake_body[index_element - 1][1] == (row, col):
            return direction
    return direction_the_original
