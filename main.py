from multiprocessing import Process
from threading import Thread
import server
import gui

if __name__ == '__main__':
    Gui = gui.gui()

    # p_gui = Process(target=Gui.gui_main(), args=('bob',))
    # p_server = Process(target=server.run_flask(), args=('bob',))
    p_gui = Thread(target=Gui.gui_main())
    p_server = Thread(target=server.run_flask())

    p_server.start()
    p_gui.start()
    p_server.join()
    p_gui.join()