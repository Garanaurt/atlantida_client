import tkinter as tk
from tkinter import PhotoImage
import json
from main_menu_fb import Fbmenu
import subprocess
import requests

class MyApp:
    def __init__(self, root: tk.Tk):
        self.validation_ok = {}
        self.activation_code = ''
        self.end_day = '-'
        self.autorization_status = 'Нет авторизации, для авторизации нажмите шестеренку'
        self.root = root
        self.root.title("Poster")
        self.root['bg'] = "#6279bb"
        self.root.geometry('900x580')
        self.root.resizable(width=False, height=False)
        self.font = ('ubuntu', 11)
        self.root.option_add("*Font", self.font)

        # Иконки
        self.settings_image = PhotoImage(file='icons/settings.png')
        self.fb_image = PhotoImage(file='icons/fb.png')

        # Авторизация статус
        self.autorization_status_label = tk.Label(root, text=self.autorization_status, bg='#c5b7b6', 
                                                  width=51, anchor='w')
        self.autorization_status_label.place(x=1,y=2)

        # Конец подписки
        self.date_label = tk.Label(root, text=f"Подписка закончится: {self.end_day}", bg='#c5b7b6', 
                                   width=51, anchor='w')
        self.date_label.place(x=450,y=2)

        # Кнопка настроек
        self.settings_button = tk.Button(root, image=self.settings_image, height=59, 
                                         command=self.open_settings) 
        self.settings_button.place(x=1, y=26)

        # Кнопка Facebook
        self.fb_button = tk.Button(root, image=self.fb_image, height=59, command=self.pass_btn)
        self.fb_button.place(x=75, y=26)

        # Кнопка пустая
        self.fb_button = tk.Button(root, width=300, height=3, command=self.pass_btn, bg='#c5b7b6', 
                                   state=tk.DISABLED)
        self.fb_button.place(x=244, y=26)
        self.load_settings()
        print(self.saved_settings)

        

    def load_settings(self):
        try:
            with open("settings.json", "r") as f:
                self.saved_settings = json.load(f)
            self.activation_code = self.saved_settings['activation_code']
            self.end_day = self.saved_settings['end_day']
            if self.activation_code:
                self.check_validation()
        except FileNotFoundError:
            self.saved_settings = {}



    def get_hwid(self):
        try:
            result = subprocess.check_output(['wmic', 'csproduct', 'get', 'uuid']).decode('utf-8')
            hwid = result.split('\n')[1].strip()
            return hwid
        except Exception:
            return None



    def check_validation(self):
        hwid = self.get_hwid()
        url = f'http://3.80.29.21/check_activation/{self.activation_code}/hwid/{hwid}'
        try:
            responce = requests.get(url)
            self.validation_ok = responce.json()
        except:
            pass
        if self.validation_ok:
            if self.validation_ok['status'] == 'code_not_valid':
                self.autorization_status = 'Ваш код активации не верный'
                self.autorization_status_label['text'] = self.autorization_status
                self.end_day = '-'
                self.date_label['text'] = f"Подписка закончится: {self.end_day}"
            elif self.validation_ok['status'] == 'valid':
                self.autorization_status = 'Лицензия активна'
                self.autorization_status_label['text'] = self.autorization_status
                self.end_day = self.validation_ok['end']
                self.date_label['text'] = f"Подписка закончится: {self.end_day}"
                Fbmenu(self.root)
            elif self.validation_ok['status'] == "licence_expired":
                self.autorization_status = 'Лицензия окончена, свяжитесь с админом'
                self.autorization_status_label['text'] = self.autorization_status
                self.end_day = "-"
                self.date_label['text'] = f"Подписка закончится: {self.end_day}"
            elif self.validation_ok['status'] == "hwid_not_valid":
                self.autorization_status = 'Лицензия активирована на другом устройстве'
                self.autorization_status_label['text'] = self.autorization_status
                self.end_day = "-"
                self.date_label['text'] = f"Подписка закончится: {self.end_day}"
            else:
                self.autorization_status = 'Лицензия активирована'
                self.autorization_status_label['text'] = self.autorization_status
                self.end_day = self.validation_ok['end']
                self.date_label['text'] = f"Подписка закончится: {self.end_day}"
                Fbmenu(self.root)
        else:
            self.autorization_status = 'Не могу связаться с сервером'
            self.autorization_status_label['text'] = self.autorization_status
            self.end_day = '-'
            self.date_label['text'] = f"Подписка закончится: {self.end_day}"
        


    def save_settings(self):
        with open("settings.json", "w") as f:
            json.dump(self.saved_settings, f)
    

    # Открыть настройки
    def show_context_menu(self, event):
        self.context_menu.post(event.x_root, event.y_root)

    def paste_from_clipboard(self):
        clipboard_text = self.settings_window.clipboard_get()
        self.activation_code.insert(tk.INSERT, clipboard_text)
    

    # Открыть настройки
    def open_settings(self):
        self.settings_window = tk.Toplevel(self.root)
        self.settings_window.title("Введи код активации и нажми подтвердить")
        self.settings_window.geometry('450x100')
        self.settings_window.resizable(False, False)

        # поле для ввода кода
        self.activation_code = tk.Entry(self.settings_window, width=50)
        self.activation_code.pack(pady=10)


        self.context_menu = tk.Menu(self.activation_code, tearoff=0)
        self.context_menu.add_command(label="Вставить", command=self.paste_from_clipboard)
        self.activation_code.bind("<Button-3>", self.show_context_menu)

        # Кнопка подтверждения кода
        self.confirm_button = tk.Button(self.settings_window, text="Подтвердить", command=lambda: self.process_code(str(self.activation_code.get())))
        self.confirm_button.pack()


    # сохранение кода и проверка валидности
    def process_code(self, code):
        self.settings_window.destroy()
        self.activation_code = code
        self.check_validation()      
        self.saved_settings["activation_code"] = code
        self.saved_settings["end_day"] = self.end_day
        self.save_settings()



    def pass_btn(self):
        pass



if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()