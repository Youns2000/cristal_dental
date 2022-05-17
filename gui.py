import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import mss
import mss.tools
import time
import os
import server
from threading import Thread

class gui():
    def __init__(self):
        self.curr_img = "./pics.png"

        self.root = tk.Tk()
        self.refresh_icon = tk.PhotoImage(file="./refresh.png")
        self.root.title('Polaris-Implants')
        self.root.minsize(500, 200)
        window_width = 1100
        window_height = 500
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.root.attributes('-topmost', 1)
        self.root.wm_attributes('-transparentcolor','grey')
        self.root.update_idletasks()
        self.init_mss()
        # root.iconbitmap('./logo.ico')
        # root.attributes('-alpha',0.5)

        self.shot_area_cnv = tk.Canvas(self.root, background="grey")
        self.shot_area_cnv.pack(fill=tk.X, side=tk.TOP)
        self.buttons_cnv = tk.Canvas(self.root)
        self.buttons_cnv.pack(fill=tk.X, side=tk.BOTTOM)

        self.root.update()

        # print(self.buttons_cnv.winfo_width())
        self.shot_button = ttk.Button(self.buttons_cnv,  width=(self.buttons_cnv.winfo_width()//2), text ="Take a shot", command =self.shot)
        self.shot_button.pack(side=tk.LEFT, expand=True)
        
        self.retake_button = tk.Button(self.buttons_cnv, image=self.refresh_icon, width=int(self.buttons_cnv.winfo_height()//2), text ="Retake a shot", command = self.refresh_cnv)
        self.retake_button.pack(side=tk.RIGHT, expand=True)

    def init_mss(self):
        with mss.mss() as sct:
            sct.shot(mon=-1, output=self.curr_img)
        if os.path.exists(self.curr_img):
            os.remove(self.curr_img)

    def shot(self, e = None):
        with mss.mss() as sct:
            monitor = {
                "top": self.root.winfo_y() + 35,
                "left": self.root.winfo_x() + 11,
                "width": self.root.winfo_width(), 
                "height": int(self.root.winfo_height()*0.9)
            }
            sct_img = sct.grab(monitor)
            # mss.tools.to_png(sct_img.rgb, sct_img.size, output=CURR_IMG)
            img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
            image = ImageTk.PhotoImage(img)

            img.save(self.curr_img)

            self.shot_area_cnv.create_image(0,0, anchor = tk.NW, image=image)
            self.shot_area_cnv.image = image
            self.shot_area_cnv.pack()

            # newwindow = tk.Tk()
            # newwindow.mainloop()
            

    
    def manage_size(self, event):
        self.shot_area_cnv.config(height=int(self.root.winfo_height()*0.9))
        self.buttons_cnv.config(width=int(self.root.winfo_height()*0.1))

    def refresh_cnv(self):
        self.shot_area_cnv.delete('all')
        # pass

    def on_closing(self):
        if os.path.exists(self.curr_img):
            os.remove(self.curr_img)
        self.root.destroy()

    def gui_main(self):
        # server.run_flask()
        # Thread(target=server.run_flask(), daemon=True).start()
        self.shot_area_cnv.bind("<Configure>", self.manage_size)
        self.root.bind('<KeyPress>', self.shot)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()