# juego.py
import time
from tkinter import *
from tkinter import messagebox

import config
import new
from unit import Cell

start_time = 0


def new_game():
    global start_time
    start_time = time.time()
    Cell.reset_game(center_frame, top_frame, game_over)


def game_over():
    for cell in Cell.all:
        cell.cell_btn_object['state'] = 'disabled'

    end_time = time.time()
    elapsed_time = end_time - start_time

    messagebox.showinfo('Game Over',
                        f'Has perdido en {turn_count} turnos.\nTiempo transcurrido: '
                        f'{elapsed_time:.2f} segundos')


def ejecutar_juego():
    root = Tk()
    root.configure(bg="grey")
    root.geometry(f'{config.WIDTH}x{config.HEIGHT}')
    root.title("Cercamines")
    root.resizable(False, False)

    global top_frame, center_frame, turn_count
    top_frame = Frame(root, bg='#5D6D7E', width=config.WIDTH, height=new.height_prct(25))
    top_frame.place(x=0, y=0)

    game_title = Label(top_frame, bg='#5D6D7E', fg='white', text='Cercamines', font=('', 48))
    game_title.place(anchor="center", relx=.5, rely=.2)

    center_frame = Frame(root, bg='black', width=new.width_prct(75), height=new.height_prct(75))
    center_frame.place(x=new.width_prct(30), y=new.height_prct(30))

    reset_button = Button(top_frame, text="Reiniciar", command=new_game)
    reset_button.place(x=new.width_prct(80), y=new.height_prct(15))

    exit_button = Button(top_frame, text="Salir", command=root.destroy)
    exit_button.place(x=new.width_prct(85), y=new.height_prct(15))

    turn_count = 1

    for x in range(config.GRID_SIZE):
        for y in range(7):
            c = Cell(x, y, game_over)
            c.create_btn_object(center_frame)
            c.cell_btn_object.grid(column=y, row=x)

    Cell.create_cell_count_label(top_frame)
    Cell.cell_count_label_object.place(anchor="center", relx=.5, rely=.6)

    Cell.randomize_mines()

    root.mainloop()


if __name__ == "__main__":
    ejecutar_juego()
