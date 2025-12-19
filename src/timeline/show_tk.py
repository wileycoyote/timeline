from tkinter import Tk, Canvas, Label, W


def create_grid(canvas):
    width = 800
    height = 600

    for line in range(0, width, 20):  # range(start, stop, step)
        canvas.create_line(
            [(line, 0), (line, height)],
            fill='black',
            tags='grid_line_w')

    for line in range(0, height, 20):
        canvas.create_line(
            [(0, line), (width, line)],
            fill='black',
            tags='grid_line_h')

    l1 = Label(canvas, text="Height")
    l1.grid(row=0, column=0, sticky=W, pady=2)


def run_app():
    window = Tk()
    window.title('Time Line')
    canvas = Canvas(window, background='white', width=800, height=600)
    create_grid(canvas)
    canvas.grid(row=0, column=0)
    window.mainloop()
