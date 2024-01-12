import tkinter as tk
from tkinter import filedialog
import json
import os
import requests
from login import FbBot
from mainfb import main_create_posts
from threading import Thread


class Fbmenu():
    def __init__(self, root: tk.Tk):
        print('start window')
        if not os.path.exists('groups.txt'):
            open('groups.txt', 'w')
        counter = {}
        counter['count'] = 0
        with open("counter.json", "w") as f:
            json.dump(counter, f)

        self.selenium_settings = {}
        self.stop_flag = False
        self.activation_code = ''
        self.groups = []
        self.bot = ''
        self.message_text = ''
        self.wait_time = 60
        self.saved_settings = ''
        self.account_fb = '-'
        self.photo_count = 0
        self.file_paths = []
        self.was_send = 0
        self.root = root

        # Label для отображения количества отправленных сообщений
        self.sent_label = tk.Label(root, text=f"Отправил: 0", width=13, height=4, bg='#c5b7b6', 
                                   anchor='sw', padx=23, pady=10, font=('arial',16,'bold'))
        self.sent_label.place(x=20,y=110)

        # Кнопка Старт
        self.start_button = tk.Button(root, text="Старт", width=10, height=2, font=('arial',16,'bold'),
                                      bg='#746b6c', command=self.on_start_click)
        self.start_button.place(x=45,y=130)


        # Label для выбора что отправлять фото текст фото+текст
        self.content_label = tk.Label(root, text=f"Рассылать:", width=13, height=4, bg='#c5b7b6', 
                                      anchor='nw', padx=23, pady=10, font=('arial',16,'bold'))
        self.content_label.place(x=20,y=250)

        # Переменная для хранения выбранного значения
        self.selected_content = tk.StringVar(value="Текст")  

        # Radiobutton для выбора "Фото"
        self.photo_button1 = tk.Radiobutton(root, text="Фото",bg='#c5b7b6', 
                                            variable=self.selected_content, value="Фото")
        self.photo_button1.place(x=50, y=290)

        # Radiobutton для выбора "Текст"
        self.text_button1 = tk.Radiobutton(root, text="Текст",bg='#c5b7b6', 
                                           variable=self.selected_content, value="Текст")
        self.text_button1.place(x=50, y=315)

        # Radiobutton для выбора "Фото+Текст"
        self.photo_text_button = tk.Radiobutton(root, text="Фото+Текст",bg='#c5b7b6', 
                                                variable=self.selected_content, value="Фото+Текст")
        self.photo_text_button.place(x=50, y=340)



        # Label для выбора времени между отправками сообщений
        self.time_label = tk.Label(root, text="""Время задержки между \nотправками сообщений:\n              секунд""", 
                                   width=22, 
                                   height=4, 
                                   bg='#c5b7b6', 
                                   anchor='nw',
                                   justify='left',
                                   padx=10, 
                                   pady=10, 
                                   font=('arial',16,'bold'))
        self.time_label.place(x=236,y=250)

        # Поле ввода времени задержки
        self.delay_entry = tk.Entry(root, width=6, font=('arial', 14))
        self.delay_entry.place(x=260, y=312)
        self.delay_entry.insert(0, self.wait_time)


        # Label для импорта групп
        groups = []
        with open('groups.txt', 'r') as f:
            try:
                groups = list(set(f.readlines())) 
            except:
                pass
        self.groups_count = len(groups)
                
        self.import_label = tk.Label(root, text=f"""Импортировано групп: {self.groups_count}""", 
                                   width=22, 
                                   height=4, 
                                   bg='#c5b7b6', 
                                   anchor='sw',
                                   justify='left',
                                   padx=10, 
                                   pady=10, 
                                   font=('arial',16,'bold'))
        self.import_label.place(x=595,y=110)

        # Кнопка импортировать группы
        self.add_groups_button = tk.Button(root, text="Импорт групп", width=13, height=1, 
                                      font=('arial',16,'bold'),bg='#746b6c', command=self.add_group)
        self.add_groups_button.place(x=645,y=130)



        # Label для добавления фото
        self.photo_label = tk.Label(root, text=f"Загружено: {len(self.file_paths)} шт.", width=25, height=4, bg='#c5b7b6', 
                                    anchor='sw', padx=23, pady=10, font=('arial',16,'bold'))
        self.photo_label.place(x=235,y=110)

        # Кнопка добавить фото
        self.add_photo_button = tk.Button(root, text="Выбрать фото для отправки", width=25, height=1, 
                                          font=('arial',16,'bold'),bg='#746b6c', command=self.add_photo)
        self.add_photo_button.place(x=243,y=130)

        # Кнопка удалить фото
        self.del_photo_button = tk.Button(root, text="Удалить", width=8, height=1, 
                                          font=('arial',16,'bold'),bg='#746b6c', command=self.del_photo)
        self.del_photo_button.place(x=445,y=180)



        # Label для авторизации в акк фб
        self.autorisation_label = tk.Label(root, text=f"Вы авторизованы в аккаунт:\n{self.account_fb}", 
                                           width=27,
                                           height=6, 
                                           bg='#c5b7b6', 
                                           anchor='sw', 
                                           padx=10, 
                                           pady=10, 
                                           font=('arial',16,'bold'))
        self.autorisation_label.place(x=535,y=250)

        # Кнопка авторизация в акк
        self.autorization_button = tk.Button(root, text="Авторизоваться в фейсбук", width=25, height=1, 
                                             font=('arial',16,'bold'),bg='#746b6c', 
                                             command=self.autorisation_fb)
        self.autorization_button.place(x=544,y=265)

        # Кнопка выхода из аккаунта
        self.unautorization_button = tk.Button(root, text="Выйти из аккаунта", width=25, height=1, 
                                               font=('arial',16,'bold'),bg='#746b6c', 
                                               command=self.unautorisation_fb)
        self.unautorization_button.place(x=544,y=310)




        # Label для ввода текста
        self.text_message_label = tk.Label(root, text=f"Текст сообщения:", width=40, height=6, 
                                           bg='#c5b7b6', anchor='nw', padx=10, pady=10, 
                                           font=('arial',16,'bold'))
        self.text_message_label.place(x=20,y=390)


        # Поле ввода текста
        self.text_entry = tk.Text(root , width=47, height=5, font=('arial', 14))
        self.scrollbar = tk.Scrollbar(root, command=self.text_entry.yview)
        self.scrollbar.place(x=495, y=435, height=110)

        self.text_entry.config(yscrollcommand=self.scrollbar.set)
        self.text_entry.place(x=30, y=435)

       
           
        self.root.after(500, lambda: self.cnt_updater())


        self.load_settings()



    
    def load_settings(self):
        try:
            with open("settingsfb.json", "r") as f:
                self.saved_settings = json.load(f)
                try:
                    self.file_paths = self.saved_settings['file_paths']
                except:
                    pass
                try:
                    self.wait_time = self.saved_settings['wait_time']
                except:
                    pass
                try:
                    self.message_text = self.saved_settings['message_text']
                except:
                    pass
                try:
                    self.account_fb = self.saved_settings['account_fb']
                except:
                    pass
        except FileNotFoundError:
            self.saved_settings = {}
        self.photo_label['text'] = f"Загружено: {len(self.file_paths)} шт."
        self.delay_entry.delete(0, tk.END)
        self.delay_entry.insert(0, self.wait_time)
        self.text_entry.insert("1.0", self.message_text)
        self.autorisation_label['text'] = f"Вы авторизованы в аккаунт:\n{self.account_fb}"


    def save_settings(self):
        with open("settingsfb.json", "w") as f:
            json.dump(self.saved_settings, f)
    


    def unautorisation_fb(self):
        try:
            os.remove('cookies.pkl')
        except:
            pass
        self.account_fb = '-'
        self.autorisation_label['text'] = f"Вы авторизованы в аккаунт:\n{self.account_fb}"


    def autorisation_fb(self):
        self.autorisation_window = tk.Toplevel(self.root)
        self.autorisation_window.title("Войди в акк фб и не закрывая окно браузера нажми ок")
        self.autorisation_window.geometry('500x50')
        self.autorisation_window.resizable(False, False)


        # Кнопка подтверждения кода
        self.confirm_button = tk.Button(self.autorisation_window, text="OK",anchor='center', command=self.close_autoris)
        self.confirm_button.pack()
        self.create_bot()



    def create_bot(self):
        self.bot = FbBot()



    def close_autoris(self):
        self.autorisation_window.destroy()
        self.account_fb = self.bot.quit_driver()
        self.autorisation_label['text'] = f"Вы авторизованы в аккаунт:\n{self.account_fb}"
        self.saved_settings['account_fb'] = self.account_fb
        self.save_settings()




    def del_photo(self):
        self.saved_settings['file_paths'] = []
        self.file_paths = []
        self.save_settings()
        self.photo_count = 0
        self.photo_label['text'] = f"Загружено: {self.photo_count} шт."


    def add_photo(self):
        photos = []
        self.file_paths = filedialog.askopenfilenames(title="Выберите фотографии")
        if self.file_paths:
            for file in self.file_paths:
                photos.append(file)
            self.saved_settings['file_paths'] = photos
            self.save_settings()
            
            self.photo_count = len(self.file_paths)
            self.photo_label['text'] = f"Загружено: {self.photo_count} шт."




    def add_group(self):
        self.groups_window = tk.Toplevel(self.root)
        self.groups_window.title("Добавь или удали группы. Каждая с новой строки")
        self.groups_window.geometry('500x510')
        self.groups_window.resizable(False, False)

        # поле для ввода групп
        self.groups_list = tk.Text(self.groups_window, width=45, height=20, font=('arial', 14))
        self.groups_list.pack(pady=15)

        grps = ''
        with open('groups.txt', 'r') as f:
            groups = f.readlines()
        for grp in groups:
            grps += f'{grp}'
        self.groups_list.insert('1.0', grps)

        self.scrollbar = tk.Scrollbar(self.groups_window, command=self.groups_list.yview)
        self.scrollbar.place(x=475, y=15, height=427)

        self.groups_list.config(yscrollcommand=self.scrollbar.set)

        # Кнопка подтверждения списка групп
        self.confirm_button = tk.Button(self.groups_window, text="Подтвердить",height=1, 
                                        command=lambda: self.processing_groups(str(self.groups_list.get("1.0", "end-1c"))))
        self.confirm_button.pack(anchor='s', pady=5)


    def processing_groups(self, text):
        self.groups_window.destroy()
        with open('groups.txt', 'w+') as file:
            file.write(text)
        groups = []
        with open('groups.txt', 'r') as f:
            try:
                groups = list(set(f.readlines())) 
            except:
                pass
        self.groups_count = len(groups)
        self.import_label['text'] = f"""Импортировано групп: {self.groups_count}"""


    def on_start_click(self):
        counter = {}
        counter['count'] = 0
        with open("counter.json", "w") as f:
            json.dump(counter, f)
        self.stop_flag = False
        self.wait_time = self.delay_entry.get()
        self.saved_settings['wait_time'] = self.wait_time
        self.save_settings()
        
        self.message_text = self.text_entry.get('1.0', 'end-1c')
        self.saved_settings['message_text'] = self.message_text
        self.save_settings()

        self.content = self.selected_content.get()

        with open('groups.txt', 'r') as f:
            try:
                self.groups = list(set(f.readlines())) 
            except:
                pass
        self.save_settings()
        self.check_validation()
        if self.start_button['state'] == tk.DISABLED:
            self.stop_activation = tk.Toplevel(self.root)
            self.stop_activation.geometry('400x50')
            self.stop_activation.title("Ваша подписка закончилась")
            self.confirm_button = tk.Button(self.stop_activation, text="Ок",height=1, 
                                        command=lambda: self.stop_activation.destroy())
            self.confirm_button.pack(anchor='s', pady=5)
            return
        if self.account_fb == '-':
            self.add_acc_top = tk.Toplevel(self.root)
            self.add_acc_top.geometry('400x50')
            self.add_acc_top.title("Сначала войдите в аккаунт")
            self.confirm_butt = tk.Button(self.add_acc_top, text="Ок",height=1, 
                                        command=lambda: self.add_acc_top.destroy())
            self.confirm_butt.pack(anchor='s', pady=5)
            return
        elif not self.groups:
            self.add_grp_top = tk.Toplevel(self.root)
            self.add_grp_top.geometry('450x50')
            self.add_grp_top.title("Добавьте группы для рассылки")
            self.confirm_but = tk.Button(self.add_grp_top, text="Ок",height=1, 
                                        command=lambda: self.add_grp_top.destroy())
            self.confirm_but.pack(anchor='s', pady=5)
            return
        if self.selected_content.get() == "Фото":
            if not self.file_paths:
                self.add_img_top = tk.Toplevel(self.root)
                self.add_img_top.geometry('450x50')
                self.add_img_top.title("Сначала добавьте изображения")
                self.confirm_bu = tk.Button(self.add_img_top, text="Ок",height=1, 
                                            command=lambda: self.add_img_top.destroy())
                self.confirm_bu.pack(anchor='s', pady=5)
                return
            self.selenium_settings['flag'] = self.stop_flag
            self.selenium_settings['content'] = 'Фото'
            with open("selenium.json", "w") as f:
                json.dump(self.selenium_settings, f)
            self.process = Thread(target=self.create_posts_thread, args=(self.message_text, self.file_paths, self.wait_time, self.groups))
            self.process.start()

        elif self.selected_content.get() == "Текст":
            if not self.message_text:
                self.add_msg_top = tk.Toplevel(self.root)
                self.add_msg_top.geometry('450x50')
                self.add_msg_top.title("Сначала добавьте текст")
                self.confirm_b = tk.Button(self.add_msg_top, text="Ок",height=1, 
                                            command=lambda: self.add_msg_top.destroy())
                self.confirm_b.pack(anchor='s', pady=5)
                return
            self.selenium_settings['flag'] = self.stop_flag
            self.selenium_settings['content'] = 'Текст'
            with open("selenium.json", "w") as f:
                json.dump(self.selenium_settings, f)
            self.process = Thread(target=self.create_posts_thread, args=(self.message_text, self.file_paths, self.wait_time, self.groups))
            self.process.start()

        elif self.selected_content.get() == "Фото+Текст":
            if not self.message_text or not self.file_paths:
                self.add_ms_top = tk.Toplevel(self.root)
                self.add_ms_top.geometry('450x50')
                self.add_ms_top.title("Сначала добавьте текст и фото")
                self.confirm_ = tk.Button(self.add_msg_top, text="Ок",height=1, 
                                            command=lambda: self.add_ms_top.destroy())
                self.confirm_.pack(anchor='s', pady=5)
                return
            self.selenium_settings['flag'] = self.stop_flag
            self.selenium_settings['content'] = 'Фото+Текст'
            with open("selenium.json", "w") as f:
                json.dump(self.selenium_settings, f)

            self.process = Thread(target=self.create_posts_thread, args=(self.message_text, self.file_paths, self.wait_time, self.groups))
            self.process.start()
            
            
        print('images',self.file_paths,'\n', 'gr', self.groups, '\n', 'content', self.selected_content.get(), '\n', 'time', self.wait_time, '\n', 'acc', self.account_fb, '\n', 'text', self.message_text)
        print('start')
        self.start_button['text'] = "Стоп"
        self.start_button['command'] = self.on_stop_click
        #self.cnt_updater()
        
        #self.was_send += 1
        #self.sent_label['text'] = f"Отправил: {self.was_send}"


    def cnt_updater(self):
        try:
            with open("counter.json", "r") as f:
                self.counte = json.load(f)
            counte = self.counte['count']
        except:
            counte = 0
        self.sent_label['text'] = f"Отправил: {counte}"

        self.root.after(2000, self.cnt_updater)

        

               
    def create_posts_thread(self, *args):
        print('thread', args)
        main_create_posts(*args)


    def on_stop_click(self):
        self.stop_flag = True
        self.selenium_settings['flag'] = self.stop_flag
        with open("selenium.json", "w") as f:
            json.dump(self.selenium_settings, f)
        self.start_button['text'] = "Старт"
        self.start_button['command'] = self.on_start_click





    def check_validation(self):
        hwid = 210953322#self.get_hwid()
        with open("settings.json", "r") as f:
            self.saved_settings = json.load(f)
        self.activation_code = self.saved_settings['activation_code']
        url = f'http://3.80.29.21/check_activation/{self.activation_code}/hwid/{hwid}'
        try:
            responce = requests.get(url)
            self.validation_ok = responce.json()
        except:
            pass
        if self.validation_ok:
            if self.validation_ok['status'] == 'code_not_valid':
                self.start_button['state'] = tk.DISABLED
            elif self.validation_ok['status'] == 'valid':
                pass
            elif self.validation_ok['status'] == "licence_expired":
                self.start_button['state'] = tk.DISABLED
            elif self.validation_ok['status'] == "hwid_not_valid":
                self.start_button['state'] = tk.DISABLED
        else:
            self.start_button['state'] = tk.DISABLED