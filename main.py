import customtkinter as ctk
import tkinter as tk
import psycopg2
import datetime as dt 

now = dt.datetime.now()

time = now.strftime("%A, %d %B")

ctk.set_appearance_mode("dark") 
ctk.set_default_color_theme("blue")  

conn = psycopg2.connect(
    host="localhost",
    database="todo",
    user="postgres",
    password="12345",
    port=5432
)

cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS tasks (id SERIAL PRIMARY KEY, task TEXT)")

class ToDo():
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("To Do")

        self.x = 200 
        self.y = 60

        self.image = tk.PhotoImage(file="background.png")
        self.canvas = tk.Canvas(highlightthickness=0)
        self.canvas.config(width=400, height=845)
        self.canvas.create_image(200, 422, image=self.image)
        self.canvas.create_text(200, 20, font=("Arial", 15), text=time, fill="gray")
        self.canvas.grid(column=1, row=1)

        self.entry = ctk.CTkEntry(self.window, width=350, height=30, font=("Arial", 25))
        self.entry.place(x=25, y=750)
        
        self.add_btn = ctk.CTkButton(self.window, text="Add Task", command=self.get_task, font=("Arial", 25, "bold"))
        self.add_btn.configure(width=300)
        self.add_btn.place(x=50, y=800)

        # transparent

        # self.canvas2 = tk.Canvas(highlightthickness=0, bg="transparent")
        # self.canvas2.place(x=100,y=10)

        # self.label = ctk.CTkLabel(self.window, text="CTkLabel", fg_color="transparent")
        # self.label.place(x=100,y=10)

        # self.my_frame = ctk.CTkFrame(self.window, fg_color="", text="dklsjhaljdh")
        # self.my_frame.place(x=100,y=10)
        # self.label.configure(background="transparent")

   

    def get_task(self):
        self.task = self.entry.get().lower()
        if self.task:
            cur.execute("INSERT INTO tasks (task) VALUES (%s)", (self.task,))
            conn.commit()
            self.entry.delete(0, "end")
            self.canvas.create_text(self.x, self.y, font=("Arial", 20, "bold"), text=f"{self.task[0].upper()}{self.task[1:]}", fill="white")
            self.checkbox = ctk.CTkCheckBox(self.window, text="", width=1)
            self.checkbox.place(x=self.x + len(self.task) * 10, y=self.y - 10)
            self.y += 30







if __name__ == "__main__":
    app = ToDo()
    app.window.mainloop()