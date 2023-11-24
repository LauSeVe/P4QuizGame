import tkinter as tk
from tkinter import ttk


class MyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi-Page GUI")

        self.notebook = ttk.Notebook(root)


        # Create pages
        self.page = ttk.Frame(self.notebook)

        self.notebook.add(self.page, text="Enrollment")

        self.notebook.pack(expand=True, fill="both")

        # Page
        self.wellcomeLabel = tk.Label(self.enrollment_page, text="Welcome to P4QuizGame, there are 4 levels")
        self.wellcomeLabel.pack(pady=10)

        self.lvlButton0 = tk.Button(self.page, text="lvl1", command=self.lvlButton(0))
        self.lvlButton0.pack(pady=10)
        
        self.lvlButton1 = tk.Button(self.page, text="lvl2", command=self.lvlButton(1))
        self.lvlButton1.pack(pady=10)
        
        self.lvlButton2 = tk.Button(self.page, text="lvl3", command=self.lvlButton(2))
        self.lvlButton2.pack(pady=10)
        
        self.lvlButton3 = tk.Button(self.page, text="lvl4", command=self.lvlButton(3))
        self.lvlButton3.pack(pady=10)

    
    def lvlButton(self,id):
        self.lvlButton.config(state=tk.DISABLED)

        self.wellcomeLabel.config(text="Prueba" + id)




if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()
