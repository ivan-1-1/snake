import tkinter
from json import loads
from network import Client
from threading import Timer


class Player:
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title("snake")
        self.root.geometry("1920x1080")
        self.login_entry = tkinter.Entry(self.root, text="Login")
        self.server_entry = tkinter.Entry(self.root, text="Server")
        self.connect_btn = tkinter.Button(self.root, text="Connect to server", command=self.start)
        self.connect_btn.pack()
        self.login_entry.pack()
        self.server_entry.pack()
        self.canvas = None
        self.scale = 100
        self.root.bind('<Up>', self.up)
        self.root.bind('<Down>', self.down)
        self.root.bind('<Left>', self.left)
        self.root.bind('<Right>', self.right)
        self.root.mainloop()

    def start(self):
        self.server = None
        self.nc = None
        self.nc = Client()
        self.timer = Timer(0.01, self.game_update)
        self.timer.start()
        self.connect_btn["state"] = "disabled"
        print(1)

    def up(self, event):
        self.send('u')

    def down(self, event):
        self.send('d')

    def left(self, event):
        self.send('l')

    def right(self, event):
        self.send('r')

    def send(self, msg):
        self.nc.send(msg)

    def recv(self):
        return self.nc.recv()

    def game_update(self):
        while True:
            print("waiting level for painting")
            self.paint(loads(self.recv()))

    def paint(self, level):
        scale = self.scale
        apple = level["apple"]
        snake = level["snake"]
        walls = level["walls"]
        size = level["size"]
        score = level["score"]

        if not self.canvas:
            self.canvas = tkinter.Canvas(self.root, width=size[0] * scale, height=size[1] * scale, bg='light green')
            self.canvas.pack()

        self.canvas.delete("all")
        self.canvas.create_oval(apple[0] * scale, apple[1] * scale, apple[0] * scale + scale, apple[1] * scale + scale,
                      fill='red', outline='green', width=3, activedash=(5, 4))
        head, *tail = snake
        self.canvas.create_rectangle(head[0] * scale, head[1] * scale, head[0] * scale + scale, head[1] * scale + scale,
                           fill='black', outline='brown', width=3)
        for link in tail:
            self.canvas.create_rectangle(link[0] * scale, link[1] * scale, link[0] * scale + scale, link[1] * scale + scale,
                               fill='yellow', outline='brown', width=3, activedash=(5, 4))
        for wall in walls:
            self.canvas.create_rectangle(wall[0] * scale, wall[1] * scale, wall[0] * scale + scale, wall[1] * scale + scale,
                               fill='black', outline='green', width=5, activedash=(5, 4))
        self.canvas.create_text(size[0] * scale - 50, 50, text=score, font="Verdana 40", fill="white")


if __name__ == "__main__":
    player = Player()
