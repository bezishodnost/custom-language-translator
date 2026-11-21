from tkinter import *
from tkinter import messagebox
import webbrowser
import json
import os

lang_folder = 'languages'
if not os.path.exists(lang_folder):
    os.makedirs(lang_folder)

summ = 0
active_lang = ''
lang_dict = {}
letter_rows = []
sign_rows = []

win = Tk()
win.title('translator')
win.geometry('700x700')

frame = Frame(win, padx=0, pady=0)
frame.pack(fill=BOTH, expand=True)


def space_press(e):
    e.widget.delete(0, END)
    e.widget.insert(0, 'Space')
    return 'break'


def get_all_langs():
    if not os.path.exists(lang_folder):
        return []
    res = []
    for f in os.listdir(lang_folder):
        if f.endswith('.json'):
            res.append(f[:-5])
    return res


def open_saved_lang(name):
    global lang_dict, active_lang
    p = os.path.join(lang_folder, name + '.json')
    if os.path.exists(p):
        f = open(p, 'r', encoding='utf-8')
        lang_dict = json.load(f)
        f.close()
        active_lang = name
        print('loaded:', active_lang, len(lang_dict))
        trans_screen()


def remove_lang(name):
    ans = messagebox.askyesno('Delete language', f'Are you sure you want to delete "{name}"?')
    if ans == True:
        p = os.path.join(lang_folder, f'{name}.json')
        if os.path.exists(p):
            os.remove(p)
            print('deleted', name)
        welcome_screen()


def creator_win():
    top = Toplevel(win)
    top.title('Creator')
    top.geometry('360x200')
    top.resizable(False, False)
    top.grab_set()

    Label(top, text='Creator: bezishodnost', font=('Arial', 14, 'bold')).pack(pady=(22, 10))
    lnk = Label(top, text='https://github.com', fg='#0066CC', font=('Arial', 12, 'underline'), cursor='hand2')
    lnk.pack(pady=5)
    lnk.bind('<Button-1>', lambda e: webbrowser.open('https://github.com'))
    Label(top, text='Good luck!', font=('Arial', 13, 'italic'), fg='#555555').pack(pady=(18, 10))


creator_but = Button(win, text='Creator', font=('Arial', 11), fg='#666666', command=creator_win)
creator_but.place(relx=0.98, rely=0.98, anchor='se')


def welcome_screen():
    for w in frame.winfo_children():
        w.destroy()
    letter_rows.clear()
    sign_rows.clear()
    win.unbind_all('<MouseWheel>')

    ver_title = Label(frame, text='v.1.0', fg="#9F9F9F", font=('Arial', 20))
    ver_title.place(relx=0.65, rely=0.05)

    w_title = Label(frame, text='Welcome!', fg='black', font=('Arial', 30))
    w_title.place(relx=0.5, rely=0.08, anchor='center')

    how_many_title = Label(frame, text='How many letters in your language?', fg='black', font=('Arial', 18))
    how_many_title.place(relx=0.5, rely=0.18, anchor='center')

    err_lbl = Label(frame, text='', fg="#9F9F9F", font=('Arial', 13))

    how_many_box = Entry(frame, font=('Arial', 18), justify='center')
    how_many_box.place(relx=0.5, rely=0.29, anchor='center')

    def check_welcome():
        global summ
        t = how_many_box.get().strip()
        if t.isdigit() and int(t) > 0:
            summ = int(t)
            print('ok summ =', summ)
            alpha_screen()
        elif not t:
            err_lbl.config(text="*You didn't enter anything*")
            err_lbl.place(relx=0.5, rely=0.235, anchor='center')
        else:
            err_lbl.config(text='*Enter digits only (>0)*')
            err_lbl.place(relx=0.5, rely=0.235, anchor='center')

    next_but = Button(frame, text='Create new', fg='black', font=('Arial', 13), command=check_welcome)
    next_but.place(relx=0.5, rely=0.355, anchor='center')

    Label(frame, text='Choose language:', fg='black', font=('Arial', 18)).place(relx=0.5, rely=0.46, anchor='center')

    box_langs = Frame(frame)
    box_langs.place(relx=0.5, rely=0.72, anchor='center', width=400, height=300)

    saved = get_all_langs()
    if len(saved) == 0:
        Label(box_langs, text='*No saved languages yet*', fg='#9F9F9F', font=('Arial', 14)).pack(pady=30)
    else:
        cnv = Canvas(box_langs, highlightthickness=0)
        sb = Scrollbar(box_langs, orient='vertical', command=cnv.yview)
        scr_fr = Frame(cnv)

        scr_fr.bind('<Configure>', lambda e: cnv.configure(scrollregion=cnv.bbox('all')))
        cnv.create_window((0, 0), window=scr_fr, anchor='nw')
        cnv.configure(yscrollcommand=sb.set)

        cnv.pack(side=LEFT, fill=BOTH, expand=True)
        sb.pack(side=RIGHT, fill=Y)
        win.bind_all('<MouseWheel>', lambda e: cnv.yview_scroll(int(-1 * (e.delta / 120)), 'units'))

        for l in saved:
            r = Frame(scr_fr)
            r.pack(fill=X, pady=4, padx=10)
            Button(r, text=l, font=('Arial', 14), width=22, command=lambda x=l: open_saved_lang(x)).pack(side=LEFT, padx=5)
            Button(r, text='X', font=('Arial', 12, 'bold'), fg='#990000', width=3, command=lambda x=l: remove_lang(x)).pack(side=LEFT, padx=5)
def alpha_screen():
    for w in frame.winfo_children():
        w.destroy()
    letter_rows.clear()
    sign_rows.clear()
    win.unbind_all('<MouseWheel>')

    Label(frame, text='Create your alphabet', font=('Arial', 22)).pack(pady=10)

    cont = Frame(frame)
    cont.pack(fill=BOTH, expand=True, padx=90)

    cnv = Canvas(cont)
    sb = Scrollbar(cont, orient='vertical', command=cnv.yview)
    scr_fr = Frame(cnv)

    scr_fr.bind('<Configure>', lambda e: cnv.configure(scrollregion=cnv.bbox('all')))
    cnv.create_window((0, 0), window=scr_fr, anchor='nw')
    cnv.configure(yscrollcommand=sb.set)

    cnv.pack(side=LEFT, fill=BOTH, expand=True)
    sb.pack(side=RIGHT, fill=Y)
    win.bind_all('<MouseWheel>', lambda e: cnv.yview_scroll(int(-1 * (e.delta / 120)), 'units'))

    Label(scr_fr, text='№', font=('Arial', 14, 'bold')).grid(row=0, column=0, padx=10, pady=5)
    Label(scr_fr, text='Letter', font=('Arial', 14, 'bold')).grid(row=0, column=1, padx=20, pady=5)
    Label(scr_fr, text='Cipher', font=('Arial', 14, 'bold')).grid(row=0, column=2, padx=20, pady=5)

    def add_row():
        n = len(letter_rows) + 1
        num_l = Label(scr_fr, text=str(n) + '.', font=('Arial', 14), fg='#666666')
        num_l.grid(row=n, column=0, padx=10, pady=4)

        p1 = Entry(scr_fr, font=('Arial', 16), width=10, justify='center')
        p1.grid(row=n, column=1, padx=20, pady=4)
        p1.bind('<space>', space_press)

        p2 = Entry(scr_fr, font=('Arial', 16), width=10, justify='center')
        p2.grid(row=n, column=2, padx=20, pady=4)
        p2.bind('<space>', space_press)

        letter_rows.append((num_l, p1, p2))

    def del_row():
        global summ
        if len(letter_rows) > 1:
            summ -= 1
            a, b, c = letter_rows.pop()
            a.destroy()
            b.destroy()
            c.destroy()

    def plus_click():
        global summ
        summ += 1
        add_row()

    for i in range(summ):
        add_row()

    signs = [' ', ',', '.', '?', '!']
    for idx, ch in enumerate(signs):
        p1 = Entry(scr_fr, font=('Arial', 16), width=10, justify='center')
        if ch == ' ':
            p1.insert(0, 'Space')
        else:
            p1.insert(0, ch)
        p1.config(state='disabled')
        p1.grid(row=1000 + idx, column=1, padx=20, pady=4)

        p2 = Entry(scr_fr, font=('Arial', 16), width=10, justify='center')
        p2.grid(row=1000 + idx, column=2, padx=20, pady=4)
        p2.bind('<space>', space_press)

        sign_rows.append((ch, p2))

    name_fr = Frame(frame)
    name_fr.pack(pady=(8, 2))
    Label(name_fr, text='Language name:', font=('Arial', 14)).pack(side=LEFT, padx=5)
    name_box = Entry(name_fr, font=('Arial', 14), width=18, justify='center')
    name_box.pack(side=LEFT, padx=5)

    err_lbl = Label(frame, text='', fg='#9F9F9F', font=('Arial', 13))
    err_lbl.pack(pady=2)

    def save_all():
        global lang_dict, active_lang
        lname = name_box.get().strip()
        if lname == '':
            err_lbl.config(text='*Enter language name*')
            return

        bad = '<>:"/\\|?*'
        for c in lname:
            if c in bad:
                err_lbl.config(text='*Invalid characters in name*')
                return

        tmp = {}
        for _, p1, p2 in letter_rows:
            k = p1.get()
            v = p2.get()
            if k == '' or v == '':
                err_lbl.config(text='*Fill in all fields*')
                return
            if k == 'Space':
                k = ' '
            if v == 'Space':
                v = ' '
            tmp[k] = v

        for ch, p2 in sign_rows:
            v = p2.get()
            if v == '':
                err_lbl.config(text='*Fill in all fields*')
                return
            if v == 'Space':
                v = ' '
            tmp[ch] = v

        lang_dict = tmp
        active_lang = lname

        if not os.path.exists(lang_folder):
            os.makedirs(lang_folder)

        fp = os.path.join(lang_folder, lname + '.json')
        with open(fp, 'w', encoding='utf-8') as f:
            json.dump(lang_dict, f, ensure_ascii=False, indent=4)

        print('saved!', active_lang, lang_dict)
        trans_screen()

    bot = Frame(frame)
    bot.pack(pady=10)

    Button(bot, text='Back', font=('Arial', 14), command=welcome_screen).pack(side=LEFT, padx=10)
    Button(bot, text='-', font=('Arial', 14, 'bold'), width=3, command=del_row).pack(side=LEFT, padx=5)
    Button(bot, text='+', font=('Arial', 14, 'bold'), width=3, command=plus_click).pack(side=LEFT, padx=5)
    Button(bot, text='Save', font=('Arial', 14), command=save_all).pack(side=LEFT, padx=10)


def trans_screen():
    for w in frame.winfo_children():
        w.destroy()
    win.unbind_all('<MouseWheel>')

    mode_var = StringVar(value='encrypt')

    Label(frame, text=f'Language: {active_lang}', font=('Arial', 22, 'bold')).pack(pady=(15, 10))

    m_bar = Frame(frame)
    m_bar.pack(pady=5)

    in_lbl = Label(frame, text='Normal text:', font=('Arial', 14))
    in_lbl.pack(pady=(10, 3))

    in_box = Text(frame, font=('Arial', 15), width=52, height=7, wrap=WORD)
    in_box.pack(pady=3)

    out_lbl = Label(frame, text='Cipher text:', font=('Arial', 14))
    out_lbl.pack(pady=(10, 3))

    out_box = Text(frame, font=('Arial', 15), width=52, height=7, wrap=WORD, state='disabled', bg='#F5F5F5')
    out_box.pack(pady=3)

    def do_translate(e=None):
        txt = in_box.get('1.0', 'end-1c')
        res = []

        if mode_var.get() == 'encrypt':
            for ch in txt:
                if ch in lang_dict:
                    res.append(lang_dict[ch])
                elif ch.lower() in lang_dict:
                    res.append(lang_dict[ch.lower()])
                else:
                    res.append(ch)
            done = ''.join(res)
        else:
            rev = {}
            for k, v in lang_dict.items():
                rev[v] = k
            keys_sorted = sorted(rev.keys(), key=len, reverse=True)
            i = 0
            while i < len(txt):
                ok = False
                for tok in keys_sorted:
                    if tok != '' and txt.startswith(tok, i):
                        res.append(rev[tok])
                        i += len(tok)
                        ok = True
                        break
                if ok == False:
                    res.append(txt[i])
                    i += 1
            done = ''.join(res)

        out_box.config(state='normal')
        out_box.delete('1.0', END)
        out_box.insert('1.0', done)
        out_box.config(state='disabled')

    def change_mode(m):
        mode_var.set(m)
        print('mode:', m)
        if m == 'encrypt':
            enc_but.config(relief=SUNKEN, bg='#D9E8F5')
            dec_but.config(relief=RAISED, bg='SystemButtonFace')
            in_lbl.config(text='Normal text:')
            out_lbl.config(text='Cipher text:')
        else:
            dec_but.config(relief=SUNKEN, bg='#D9E8F5')
            enc_but.config(relief=RAISED, bg='SystemButtonFace')
            in_lbl.config(text='Cipher text:')
            out_lbl.config(text='Normal text:')
        do_translate()

    enc_but = Button(m_bar, text='Encrypt (Text → Cipher)', font=('Arial', 13), relief=SUNKEN, bg='#D9E8F5', command=lambda: change_mode('encrypt'))
    enc_but.pack(side=LEFT, padx=8)

    dec_but = Button(m_bar, text='Decrypt (Cipher → Text)', font=('Arial', 13), command=lambda: change_mode('decrypt'))
    dec_but.pack(side=LEFT, padx=8)

    in_box.bind('<KeyRelease>', do_translate)

    st_lbl = Label(frame, text='', fg='#4CAF50', font=('Arial', 12))
    st_lbl.pack(pady=(4, 0))

    def copy_res():
            win.clipboard_append()
            st_lbl.config(text='Copied to clipboard!')
            win.after(1500, lambda: st_lbl.config(text=''))

    bot = Frame(frame)
    bot.pack(pady=12)

    Button(bot, text='Main Menu', font=('Arial', 14), command=welcome_screen).pack(side=LEFT, padx=12)
    Button(bot, text='Copy Result', font=('Arial', 14), command=copy_res).pack(side=LEFT, padx=12)


welcome_screen()
win.mainloop()
