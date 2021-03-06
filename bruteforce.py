# Auteurs: Benjamin BEYERLE - Philippe DA SILVA OLIVEIRA - Karthike EZHILARASAN - Alexandre KOSTAS
# Classe: SRC1 - 3E
# Projet - ClicMed

import settings


def main_frame(root_frame, username, group):
    settings.login.clear_window(root_frame)
    root_frame.configure(background='#3c3f41')

    root_frame.title('Bruteforcer')
    root_frame.geometry('290x290')
    root_frame.maxsize(290, 190)
    root_frame.minsize(290, 190)

    cnx = settings.mysql.connect(host=settings.HOST, user=settings.MYSQL_USER, password=settings.MYSQL_USER_PWD,
                                 database=settings.MYSQL_DB)
    cursor = cnx.cursor(buffered=True)
    cursor.execute("SELECT DISTINCT Username FROM Users")
    username_list = list(cursor.fetchall())
    cursor.close()

    filter1_choice = settings.tk.StringVar()
    filter2_choice = settings.tk.StringVar()
    filter1_choice.set(username_list[0])
    filter2_choice.set('4')

    password_length = ['1', '2', '3', '4', '5', '6', '7', '8']

    filter1 = settings.tk.Label(root_frame, text='Select user : ', font=("Arial", 10), fg='white', bg='#3c3f41')
    filter1.grid(row=0, column=0, pady=2, sticky="e")

    dropdown1 = settings.tk.OptionMenu(root_frame, filter1_choice, *username_list)
    dropdown1.grid(row=0, column=1, pady=2, sticky="w")
    dropdown1.config(borderwidth=0)

    filter2 = settings.tk.Label(root_frame, text="Length :", font=("Arial", 8), fg='white', bg='#3c3f41')
    filter2.grid(row=0, column=1, pady=2, sticky="e")

    dropdown2 = settings.tk.OptionMenu(root_frame, filter2_choice, *password_length)
    dropdown2.grid(row=0, column=2, sticky="w", ipady=2)
    dropdown2.config(borderwidth=0)

    filtr_btn = settings.tk.Button(root_frame, text="Attack!",
                                   command=lambda: bruteforcer(filter1_choice.get()[2:-3],
                                                               int(filter2_choice.get()), progress_bar,
                                                               label2, label3))
    filtr_btn.grid(row=3, column=1, pady=2, sticky="w")

    progress_bar = settings.ttk.Progressbar(root_frame, orient='horizontal', length=165)
    progress_bar.grid(row=1, column=1, sticky='w', pady=2)

    label1 = settings.tk.Label(root_frame, text='Try n° : ', font=("Arial", 10), fg='white', bg='#3c3f41')
    label1.grid(row=2, column=0, pady=2, sticky="e")

    label2 = settings.tk.Label(root_frame, text='0', font=("Arial", 10), fg='black', bg='white')
    label2.grid(row=2, column=1, pady=2, sticky="w")

    label3 = settings.tk.Entry(root_frame, text='0', font=("Arial", 10), fg='black', bg='white', width=10)

    return_btn = settings.tk.Button(root_frame, text='Return',
                                    command=lambda: settings.menu.main_frame(root_frame, username, group))
    return_btn.grid(row=3, column=1, sticky="se", padx=35, pady=2)

    exit_btn = settings.tk.Button(root_frame, text='Exit', command=root_frame.destroy)
    exit_btn.grid(row=3, column=1, sticky="se", pady=2)


def bruteforcer(username_target, length, progress_bar, nb_try, found):

    password_try = 0
    available_char = settings.string.ascii_letters + settings.string.digits
    cnx = settings.mysql.connect(host=settings.HOST, user=settings.MYSQL_USER, password=settings.MYSQL_USER_PWD,
                                 database=settings.MYSQL_DB)
    cursor = cnx.cursor(buffered=True)
    cursor.execute("SELECT PasswordHash FROM Users WHERE Username = %s", (username_target, ))
    cursed = cursor.fetchone()
    hashed_user_password = str(cursed[0])
    cursor.close()
    cnx.close()
    password_to_attempt = settings.itertools.product(available_char, repeat=length)

    progress_bar.config(maximum=(64**length), mode='determinate', value=password_try)

    for attempt in password_to_attempt:
        password_try += 1
        progress_bar['value'] = password_try
        nb_try.config(text=password_try)
        nb_try.update()
        progress_bar.update()
        attempt = ''.join(attempt)
        hashed_attempt = settings.login.password_hash(attempt)
        if hashed_attempt == hashed_user_password:
            found.delete(0, settings.tk.END)
            found.insert(0, attempt)
            found.grid(row=2, column=1, pady=2, sticky="e")
            break
