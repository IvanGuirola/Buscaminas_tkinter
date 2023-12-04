# unit.py
import random
from tkinter import Button, Label, messagebox
import config
import time

turn_count = 0
start_time = 0


class Cell:
    all = []
    cell_count = config.CELL_COUNT = config.GRID_SIZE * 7
    cell_count_label_object = None
    game_over = False

    def __init__(self, x, y, show_mine_func=None, is_mine=False):
        self.is_mine = is_mine
        self.is_opened = False
        self.is_mine_candidate = False
        self.cell_btn_object = None
        self.x = x
        self.y = y
        self.show_mine_func = show_mine_func
        Cell.all.append(self)

    def create_btn_object(self, location):
        btn = Button(location, width=12, height=4)
        btn.bind('<Button-1>', self.left_click_actions)
        btn.bind('<Button-3>', self.right_click_actions)
        self.cell_btn_object = btn

    @staticmethod
    def create_cell_count_label(location):
        lbl = Label(location, bg='#5D6D7E', fg='white', text=f"Casillas Restantes:{Cell.cell_count}\nTurno: 0",
                    font=("", 30))
        Cell.cell_count_label_object = lbl

    def left_click_actions(self, event):
        if Cell.game_over or self.is_mine_candidate:
            return

        global turn_count, start_time
        if turn_count == 0:
            start_time = time.time()

        if self.is_mine:
            self.show_mine()
        else:
            if self.surrounded_cells_mines_length() == 0:
                for cell_obj in self.surrounded_cells():
                    cell_obj.show_cell()
            self.show_cell()
            if Cell.cell_count == config.MINES_COUNT:
                elapsed_time = time.time() - start_time
                messagebox.showinfo('Felicidades',
                                    f'Has ganado en {turn_count} turnos!\nTiempo transcurrido:'
                                    f' {elapsed_time:.2f} segundos')
                Cell.game_over = True

        self.cell_btn_object.unbind('<Button-1>')
        self.cell_btn_object.unbind('<Button-3>')

        update_turn_count()

    def right_click_actions(self, event):
        if Cell.game_over:
            return

        if not self.is_mine_candidate:
            self.cell_btn_object.configure(
                bg='orange'
            )
            self.is_mine_candidate = True
        else:
            self.cell_btn_object.configure(
                bg='SystemButtonFace'
            )
            self.is_mine_candidate = False

        update_turn_count()

    def surrounded_cells(self):
        cells = [
            self.get_cell_by_axis(self.x - 1, self.y - 1),
            self.get_cell_by_axis(self.x - 1, self.y),
            self.get_cell_by_axis(self.x - 1, self.y + 1),
            self.get_cell_by_axis(self.x, self.y - 1),
            self.get_cell_by_axis(self.x + 1, self.y - 1),
            self.get_cell_by_axis(self.x + 1, self.y),
            self.get_cell_by_axis(self.x + 1, self.y + 1),
            self.get_cell_by_axis(self.x, self.y + 1)
        ]

        cells = [cell for cell in cells if cell is not None]
        return cells

    def surrounded_cells_mines_length(self):
        counter = 0
        for cell in self.surrounded_cells():
            if cell.is_mine:
                counter += 1

        return counter

    def show_cell(self):
        if not self.is_opened:
            Cell.cell_count -= 1
            self.cell_btn_object.configure(text=self.surrounded_cells_mines_length())
            if Cell.cell_count_label_object:
                Cell.cell_count_label_object.configure(
                    text=f"Casillas Restantes:{Cell.cell_count}\nTurno: {turn_count}"
                )
            self.cell_btn_object.configure(
                bg='SystemButtonFace'
            )

        self.is_opened = True

    def show_mine(self):
        global start_time
        if Cell.game_over:
            return

        elapsed_time = time.time() - start_time

        for cell in Cell.all:
            if cell.is_mine:
                cell.cell_btn_object.configure(bg='red')

        Cell.game_over = True

        if self.is_mine:
            messagebox.showinfo('Game Over',
                                f'Has pulsado en una mina\nTurnos: {turn_count}\nTiempo transcurrido:'
                                f' {elapsed_time:.2f} segundos')

    @staticmethod
    def randomize_mines():
        picked_cells = random.sample(Cell.all, config.MINES_COUNT)
        for picked_cell in picked_cells:
            picked_cell.is_mine = True

    @staticmethod
    def get_cell_by_axis(x, y):
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell

    def __repr__(self):
        return f"Cell({self.x}, {self.y})"

    @staticmethod
    def reset_game(center_frame, top_frame, game_over):
        global turn_count, start_time
        turn_count = 0
        start_time = 0
        Cell.all = []
        config.CELL_COUNT = config.GRID_SIZE * 7
        Cell.cell_count = config.CELL_COUNT
        Cell.game_over = False

        if Cell.cell_count_label_object:
            Cell.cell_count_label_object.place_forget()

        for widget in center_frame.winfo_children():
            if isinstance(widget, Button):
                widget.destroy()

        for x in range(config.GRID_SIZE):
            for y in range(7):
                c = Cell(x, y, game_over)
                c.create_btn_object(center_frame)
                c.cell_btn_object.grid(column=y, row=x)

        if Cell.cell_count_label_object is None:
            Cell.create_cell_count_label(top_frame)
        else:
            Cell.cell_count_label_object.configure(text=f"Casillas Restantes:{Cell.cell_count}\nTurno: {turn_count}")
            Cell.cell_count_label_object.place(anchor="center", relx=.5, rely=.6)

        Cell.randomize_mines()


def update_turn_count():
    global turn_count
    turn_count += 1
    Cell.cell_count_label_object.configure(
        text=f"Casillas Restantes:{Cell.cell_count}\nTurno: {turn_count}"
    )
