import os.path
import datetime
import subprocess
import tkinter as tk
import cv2
from PIL import Image, ImageTk


import util

class App:
    def __init__(self):
        self.main_window = tk.Tk()# Aqui estamos creando la ventana de inicio
        self.main_window.geometry("1200x520+350+100") #aqui damos las medidas y la posicion de la ventana en la pantalla
        # Aqui creamos los botones, asi como las posiciones de los mismos
        self.login_button_main_window = util.get_button(self.main_window, 'Login','green',self.login, fg='blue')
        self.login_button_main_window.place(x=750, y=300)

        self.register_new_user_button_main_window = util.get_button(self.main_window, 'Register New User', 'gray',
                                                                    self.register_new_user, fg='Black')
        self.register_new_user_button_main_window.place(x=750, y=400)
        #Aqui se crea la ventana donde aparecera la imagen capturada por nuestra webcam
        self.webcam_label = util.get_image_label(self.main_window)
        self.webcam_label.place(x=10, y=0, width=700, height=500)

        self.add_webcam(self.webcam_label)
        #Aqui se crea el directorio qeu nos servida de base de imagenes para entrenar
        self.db_dir = './db'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

        self.log_path = './log.txt' # con esta linea + la libreria de datetime podemos crear estampas de tiempo de registro

    def add_webcam(self, label):
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)

        self._label = label
        self.process_webcam()

    def process_webcam(self):
        ret, frame = self.cap.read()

        self.most_recent_capture_arr = frame

        img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)

        self.most_recent_capture_pil = Image.fromarray(img_)

        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        self._label.imgtk = imgtk
        self._label.configure(image=imgtk)

        self._label.after(20, self.process_webcam)

    def login(self):
        unknown_img_path = './.tmp.jpg'

        cv2.imwrite(unknown_img_path, self.most_recent_capture_arr)

        output = str(subprocess.check_output(['face_recognition', self.db_dir, unknown_img_path]))
        name = output.split(',')[1][:-3]

        if name in ['unknown_person', 'no_persons_found']:
            util.msg_box('Ups...','Error, Usuario desconocido o no encontrado \n Intentelo nuevamente o Registre un nuevo usuario')
        else:
            util.msg_box('Welcome Back!!', 'Welcome, {}'.format(name))
            with open(self.log_path, 'a') as f:
                f.write('{},{}\n'.format(name, datetime.datetime.now()))
                f.close()
        os.remove(unknown_img_path)

    def register_new_user(self):
        self.register_new_user_window = tk.Toplevel(self.main_window)
        self.register_new_user_window.geometry("1200x520+370+120")

        self.accept_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Accept', 'green', self.accept_register_new_user, fg='blue')
        self.accept_button_register_new_user_window.place(x=750, y=300)

        self.try_again_register_new_user_window = util.get_button(self.register_new_user_window, 'Try Again', 'green', self.try_again_register_new_user, fg='Red')
        self.try_again_register_new_user_window.place(x=750, y=400)

        self.capture_label = util.get_image_label(self.register_new_user_window)
        self.capture_label.place(x=10, y=0, width=700, height=500)

        self.add_img_to_label(self.capture_label)

        self.entry_text_register_new_user = util.get_entry_text(self.register_new_user_window)
        self.entry_text_register_new_user.place(x=750, y=150)

        self.text_label_register_new_user = util.get_text_label(self.register_new_user_window, "Digite el nombre del usuario")
        self.text_label_register_new_user.place(x=750, y=90)


    def try_again_register_new_user(self):
        self.register_new_user_window.destroy()

    def add_img_to_label(self, label):
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)

        self.register_new_user_capture = self.most_recent_capture_arr.copy()

    def start(self):
        self.main_window.mainloop()

    def accept_register_new_user(self):
        name = self.entry_text_register_new_user.get(1.0, "end-1c")

        cv2.imwrite(os.path.join(self.db_dir, '{}.jpg'.format(name)), self.register_new_user_capture)

        util.msg_box('Registrado!', 'Usuario registrado con exito!')
        self.register_new_user_window.destroy()




if __name__ == "__main__":
    app = App()
    app.start()