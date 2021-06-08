from technical import *
import tkinter
from random import randint, sample

# Ширина карты (в клетках).
# Map width (in cells).
MAP_WIDTH = 20
# Высота карты (в клетках).
# Map height (in cells).
MAP_HEIGHT = 20
# Размер клетка.
# Cell size.
SIZE_CELL = 40


def create_grid(canvas):
    """Рисует сетку.
    Draws a grid."""
    for i in range(MAP_WIDTH):
        canvas.create_line(((i * SIZE_CELL, 0), (i * SIZE_CELL, MAP_HEIGHT * SIZE_CELL)), fill='black')
    for i in range(MAP_HEIGHT):
        canvas.create_line(((0, i * SIZE_CELL), (MAP_WIDTH * SIZE_CELL, i * SIZE_CELL)), fill='black')


class GameGraphics:
    def __init__(self):
        self.button_direction = {
            'Left': '-col',
            'Right': '+col',
            'Up': '-row',
            'Down': '+row'
        }
        # Создаем карту и змейку.
        # Creating a map and a snake.
        self.game = Game(MAP_WIDTH // 2, MAP_HEIGHT // 2, MAP_HEIGHT, MAP_WIDTH)
        self.canvas = tkinter.Canvas(tk, width=MAP_WIDTH * SIZE_CELL, height=MAP_HEIGHT * SIZE_CELL)
        self.canvas.pack()
        # Кнопка "RESTART".
        # The "RESTART" button.
        self.button = tkinter.Button(text='RESTART', padx=f"8", pady=f"4", font="Arial 14",
                                     command=self.reset)
        # Создаем сетку.
        # Creating a grid.
        create_grid(self.canvas)
        # Создаем список с id объектов (self.canvas).
        # Creating a list with the object id (self. canvas).
        self.id_list = tuple(map(lambda x: [None] * MAP_WIDTH, range(MAP_HEIGHT)))
        # Создаем список с координатами.
        # Creating a list with coordinates.
        self.list_coordinate = tuple(
            tuple(((i * SIZE_CELL, j * SIZE_CELL), (((i + 1) * SIZE_CELL), (j + 1) * SIZE_CELL))
                  for i in range(MAP_HEIGHT)) for j in range(MAP_WIDTH))
        # Направление.
        # Direction.
        self.direction = None
        # Очки.
        # Points.
        self.points = 0
        # Флаг для контроля цикла.
        # Flag for cycle control.
        self.flag = True
        # Список еды.
        # Food list.
        self.list_food = [i for i in self.game.list_object if self.game.list_object[i]['type'] != 'no_food']
        # Размещаем стенки.
        # We place the walls.
        for i in range(round((MAP_WIDTH * MAP_HEIGHT) * 0.09)):
            row, col = randint(0, self.game.total_rows - 1), randint(0, self.game.total_cols - 1)
            while not self.game.add_an_item_to_the_map('wall', row, col):
                row, col = randint(0, self.game.total_rows - 1), randint(0, self.game.total_cols - 1)
        # Размещаем еду.
        # Placing food.
        self.foods(round(MAP_WIDTH * MAP_HEIGHT * 0.15))
        # Запускаем цикл.
        # Start the loop.
        self.move()
        # Отображаем игру.
        # Displaying the game.
        self.display_images_of_objects()

    def foods(self, count):
        """Размещает еду по карте {count} раз.
        Places food on the map {count} times."""
        for _ in range(count):
            row, col = randint(0, self.game.total_rows - 1), randint(0, self.game.total_cols - 1)
            item = sample(self.list_food, 1)[0]
            while not self.game.add_an_item_to_the_map(item, row, col):
                row, col = randint(0, self.game.total_rows - 1), randint(0, self.game.total_cols - 1)
        self.display_images_of_objects()

    def keysym_game(self, event):
        """Меняем направление змеи.
        Changing the direction of the snake."""
        item = self.button_direction.get(event.keysym, False)
        if item:
            self.direction = item

    def move(self):
        """"Главный метод, который перемещает змейку по направлению.
        The main method that moves the snake in the direction."""
        # Цикл.
        # Cycle.
        self.canvas.after(350, self.move)
        # Если flag = True, то игра не окончена.
        # If flag = True, the game is not over.
        if self.flag:
            if self.direction is not None:
                # Данные о перемещении змеи (False или (True,  False/integer)).
                # Snake movement data (False or (True, False/integer)).
                move = self.game.moving_the_snake(self.direction)
                # Если проигрыш, то выводим пользователю красный экран.
                # If you lose, then we display a red screen to the user.
                if not move:
                    self.canvas.delete('all')
                    self.canvas.create_rectangle(((0, 0), (MAP_HEIGHT * SIZE_CELL, MAP_WIDTH * SIZE_CELL)),
                                                 fill='red')
                    self.canvas.create_text(MAP_WIDTH * SIZE_CELL * 0.5, MAP_HEIGHT * SIZE_CELL * 0.2,
                                            font='Arial 40',
                                            text='GAME OVER')
                    self.canvas.create_text(MAP_WIDTH * SIZE_CELL * 0.5, MAP_HEIGHT * SIZE_CELL * 0.4,
                                            font='Arial 30',
                                            text=f'Points: {self.points}')
                    # Размещаем кнопку.
                    # Placing the button.
                    self.button.place(relx=0.43, rely=0.6)
                # Если змейка что-то съел.
                # If the snake ate something.
                elif move[1]:
                    self.points += move[1]
                    # Размещаем новую еду.
                    # Posting new food.
                    self.foods(1)
                # Если игра продолжается, то отображаем её.
                # If the game continues, then we display it.
                if move:
                    self.display_images_of_objects()
                else:
                    self.flag = False

    def reset(self):
        """Обнуляет игру.
        Resets the game."""
        self.canvas.destroy()
        self.button.destroy()
        self.__init__()

    def display_images_of_objects(self):
        """Отображает на дисплей объекты по данным списка (self.map).
        Displays objects based on the list data (self. map)."""
        # Удаляем все объекты.
        # Deleting all objects.
        for index_element_row in range(len(self.game.map)):
            for index_element_col in range(len(self.game.map[index_element_row])):
                if self.id_list[index_element_row][index_element_col] is not None:
                    self.canvas.delete(self.id_list[index_element_row][index_element_col])
                    self.id_list[index_element_row][index_element_col] = None
        # Отображаем объекты.
        # Displaying objects.
        for index_element_row in range(len(self.game.map)):
            for index_element_col, element in enumerate(self.game.map[index_element_row]):
                if element is not None:
                    coordinate = self.list_coordinate[index_element_row][index_element_col]
                    objects = {
                        'apple': lambda x: self.canvas.create_oval(coordinate,
                                                                   fill='red'),
                        'head_snake': lambda x: self.canvas.create_oval(coordinate,
                                                                        fill='green'),
                        'snake_body': lambda x: self.canvas.create_oval(coordinate, fill='black',
                                                                        outline='black'),
                        'big_apple': lambda x: self.canvas.create_oval(coordinate, fill='hot pink',
                                                                       outline='black'),
                        'spoiled_apple': lambda x: self.canvas.create_oval(coordinate, fill='DarkOrange4',
                                                                           outline='black'),
                        'big_spoiled_apple': lambda x: self.canvas.create_oval(coordinate, fill='red4',
                                                                               outline='black'),
                        'wall': lambda x: self.canvas.create_rectangle(coordinate, fill='dimgrey',
                                                                       outline='black')
                    }
                    self.id_list[index_element_row][index_element_col] = objects[element](None)


tk = tkinter.Tk()
tk.geometry(f'{MAP_WIDTH * SIZE_CELL}x{MAP_HEIGHT * SIZE_CELL}+0+0')
tk.title('Змейка на Python')
game_graphics = GameGraphics()
tk.bind('<KeyPress>', game_graphics.keysym_game)
tk.mainloop()
