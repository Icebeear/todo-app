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

cur.execute('SELECT * FROM tasks')
tasks = cur.fetchall()


class ToDo():
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("To Do")

        self.x = 200 
        self.y = 60

        self.image = tk.PhotoImage(file="background.png")
        self.canvas = tk.Canvas(highlightthickness=0)
        self.canvas.config(width=400, height=845, bg="#373737")
      
        self.canvas.create_text(200, 20, font=("Arial", 15), text=time, fill="gray")
        self.canvas.grid(column=1, row=1)

        self.entry = ctk.CTkEntry(self.window, width=350, height=30, font=("Arial", 25))
        self.entry.place(x=25, y=750)
        
        self.add_btn = ctk.CTkButton(self.window, text="Add Task", command=self.get_task, font=("Arial", 25, "bold"))
        self.add_btn.configure(width=300)
        self.add_btn.place(x=50, y=800)

        self.del_btns = []
        self.load_db()

    def load_db(self):
        if tasks: 
            for task in tasks:
                self.canvas.create_text(self.x, self.y, font=("Arial", 20, "bold"), text=task[1], fill="white", tags=str(task[0]))
                self.canvas.create_line(0, self.y + 20, 400, self.y + 20, fill="white", width=1, tags=str(task[0]))

                self.del_btn = ctk.CTkButton(self.window, text="❌", command=lambda id=task[0]: self.del_task(id))
                self.del_btn.configure(width=10)
                self.del_btn.place(x=360, y=self.y - 15)
                self.del_btns.append(self.del_btn)
                self.y += 40
        else: 
            self.id = 1 


    def get_task(self):
        self.task = self.entry.get().lower()
        if len(self.task) <= 20 and self.task:
            self.task = f"{self.task[0].upper()}{self.task[1:]}"
            cur.execute("INSERT INTO tasks (task) VALUES (%s)", (self.task,))
            conn.commit()
            

            self.canvas.create_text(self.x, self.y, font=("Arial", 20, "bold"), text=self.task, fill="white", tags=self.id)
            self.canvas.create_line(0, self.y + 20, 400, self.y + 20, fill="white", width=1, tags=self.id)

            self.del_btn = ctk.CTkButton(self.window, text="❌", command=lambda id=self.id: self.del_task(id))
            self.del_btn.configure(width=10)
            self.del_btn.place(x=360, y=self.y - 15)

            self.del_btns.append(self.del_btn)

            self.id += 1 
            self.y += 40
            
        self.entry.delete(0, "end")


    def del_task(self, id):
        cur.execute("DELETE FROM tasks WHERE id = %s", (id,))
        conn.commit()
    
        
        # text_obj = self.canvas.find_withtag(str(id + 1))
        # line_obg = self.canvas.find_withtag(str(id + 2))
        # self.canvas.delete(text_obj)
        # self.canvas.delete(line_obg)
        
        # self.canvas.delete("all")
        # self.canvas.create_text(200, 20, font=("Arial", 15), text=time, fill="gray")
        # self.load_db()




if __name__ == "__main__":
    app = ToDo()
    app.window.mainloop()

'''
sry but gui bugs in ctk, bb
graveyard app
'''