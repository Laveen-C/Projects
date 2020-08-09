import random
import tkinter as tk

n = 1000000
inside = 0

window = tk.Tk()
canvas = tk.Canvas(window, width = 900, height = 900)
canvas.pack()
T = tk.Text(window, height=2, width=30)
T.pack()
canvas.create_oval(0, 0, 900, 900)

for i in range(n):
    x = random.uniform(0, 2)
    y = random.uniform(0, 2)

    if (x - 1)**2 + (y-1)**2 <= 1:
        inside += 1
        canvas.create_oval(x*450 - 2, y*450 - 2, x*450 + 2, y*450 + 2, outline = "green", fill = "green")
    else:
        canvas.create_oval(x*450 - 2, y*450 - 2, x*450 + 2, y*450 + 2, outline = "blue", fill = "blue")

pi = 4 * inside / n

T.insert(tk.END, pi)


window.mainloop()
