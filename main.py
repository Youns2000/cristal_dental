from tkinter import *
from PIL import Image, ImageTk
import mss
import mss.tools
import os

CURR_IMG = "./pics.png"

#######################
###  WINDOW CONFIG  ###
#######################
root = Tk()
root.title('Polaris-Implants')
window_width = 1100
window_height = 500
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
root.attributes('-topmost', 1)
# root.iconbitmap('./logo.ico')
# root.attributes('-alpha',0.5)
root.wm_attributes('-transparentcolor','grey')

#######################
#####  CALLBACKS  #####
#######################

def paint(event):
    # get x1, y1, x2, y2 co-ordinates
    x1, y1 = (event.x-3), (event.y-3)
    x2, y2 = (event.x+3), (event.y+3)
    color = "black"
    # display the mouse movement inside canvas
    wn.create_oval(x1, y1, x2, y2, fill=color, outline=color)

def shot(e):
    if e.keysym != "Return":
        return
    
    with mss.mss() as sct:
        monitor = {
            "top": root.winfo_y() + 35,
            "left": root.winfo_x() + 11, 
            "width": root.winfo_width(), 
            "height": root.winfo_height()
        }
        sct_img = sct.grab(monitor)
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=CURR_IMG)
        # if os.path.exists(CURR_IMG):
        #     print("yeah")
        image = ImageTk.PhotoImage(Image.open(CURR_IMG))
        # img = wn.create_image(250, 120, anchor=NW, image=image)
        img_label = Label(image=image)
        img_label.grid(row=0, column=0, columnspan=3)


        
        # filename = sct.shot(mon=1, output="pics.bmp")
    # root.attributes('-alpha',1)
    # image = ImageTk.PhotoImage(Image.open('pics.bmp'))
    # img = wn.create_image(250, 120, anchor=NW, image=image)
    # wn.pack()





wn=Canvas(root, bg='grey')
# wn.pack()
# image = ImageTk.PhotoImage(Image.open(CURR_IMG))
# img_label = Label(image=image)
# img_label.grid(row=0, column=0, columnspan=3)
wn.pack(fill=BOTH, expand=True)
# wn.bind('<B1-Motion>', paint)
root.bind('<KeyPress>', shot)




def on_closing():
    if os.path.exists(CURR_IMG):
        os.remove(CURR_IMG)
    root.destroy()
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()