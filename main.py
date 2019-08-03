#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import messagebox
from functools import partial
import dropbox
from dateutil import tz
from datetime import datetime
from os import listdir


def search_dbx(entry):
    global li
    li.clear()
    files = dbx.files_list_folder('')
    entries = files.entries
    for file in entries:
        global inp
        name = file.name
        # print(name)
        if name.find(inp, 0, len(name) - 4) != -1:
            li.append(name)
    # print(name)
    global length
    length = len(li)
    if length == 0 or (entry.index("end") == 0):
        root.deiconify()
        root2.iconify()
        messagebox.showinfo(title='提醒', message='查無此車牌')
        pic1()
    else:
        for i in range(length):
            with open(li[i], "wb") as f:
                metadata, res = dbx.files_download(path="/" + li[i])
                f.write(res.content)
                f.close()


def db_remove():
	global flate
	global global_timestamp
	if (flate):
		name = (li[1].split('.')[0]) + ".jpg"
		dbx.files_delete(path="/pictures_jpg/" + name)
		dbx.files_delete(path="/" + li[1])
		with open(work_path + "License_plate_record.txt", "a+") as f:
			f.write(li[1].split('.')[0]+"\t\t"+global_timestamp+"\t\t\t"+
			datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S"))
			f.write('\n\n')
	else:
		name = (li[0].split('.')[0]) + ".jpg"
		dbx.files_delete(path="/pictures_jpg/" + name)
		dbx.files_delete(path="/" + li[0])
		with open(work_path + "License_plate_record.txt", "a+") as f:
			f.write(li[0].split('.')[0]+"\t\t"+global_timestamp +"\t\t\t"+
			datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S"))
			f.write('\n\n')


def db_upload():
	for files in listdir(work_path):
		if ".txt" in files:
			txt = files
			with open(work_path + files, 'rb') as f:
				dbx.files_upload(f.read(), "/" + txt,
								 mode=dropbox.files.WriteMode("overwrite"))


def get_input(entry, argu):
    entry.insert(END, argu)


def backspace(entry):
    input_len = len(entry.get())
    entry.delete(input_len - 1)


def enter(entry):
    global inp
    inp = str(entry.get())
    root.quit()
    root2.deiconify()
    root.iconify()
    root3.iconify()
    search_dbx(entry)
    t2s()
    pic2()


def enter2():
	global time_list
	db_remove()
	db_upload()
	time_list.clear()
	root.deiconify()
	root2.iconify()
	root3.iconify()
	pic1()


def button1_flate():
    global flate
    global idx2
    flate = False
    root3.deiconify()
    root2.iconify()
    idx2 = 10000
    pic3()


def button2_flate():
    global flate
    global idx
    flate = True
    root3.deiconify()
    root2.iconify()
    idx = 10000
    pic3()
	
	
def return_pic1():
	root.deiconify()
	root2.iconify()
	pic1()


def t2s():
	from_zone = tz.gettz('UTC')
	to_zone = tz.gettz('CST')
	files = dbx.files_list_folder('/pictures_jpg')
	entries = files.entries
	global time_list
	global global_timestamp
	for file in entries:
		name = file.name
		name = name.split('.')[0]
		time_list.append(name)
		utc_timestamp = file.client_modified
		utc_timestamp = utc_timestamp.replace(tzinfo=from_zone)
		local_timestamp = utc_timestamp.astimezone(to_zone)
		global_timestamp = datetime.strftime(local_timestamp, "%Y-%m-%d %H:%M:%S")
		local_timestamp = datetime.strftime(local_timestamp, "%d:%H:%M:%S")
		d, h, m, s = local_timestamp.strip().split(":")
		local_timestamp_res = int(d) * 86400 + int(h) * 3600 + int(m) * 60 + int(s)
		time_list.append(local_timestamp_res)
	now_time = datetime.strftime(datetime.now(), "%d:%H:%M:%S")
	nd, nh, nm, ns = now_time.strip().split(":")
	now_time_res = int(nd) * 86400 + int(nh) * 3600 + int(nm) * 60 + int(ns)
	time_list.append(now_time_res)


def s2t(arg):
    global time_list
    m, s = divmod(time_list[-1] - time_list[arg], 60)
    h, m = divmod(m, 60)
    res = ("%02d:%02d:%02d" % (h, m, s))
    res = res.split(':')
    res = res[0] + "小時" + "\t  " + res[1] + "分" + "\t  " + res[2] + "秒"
    return res


def pic1():
    entry = Entry(root, justify="right", font="Helvetica 26 bold")
    entry.grid(row=0, column=0, columnspan=4, sticky=N + W + S + E, padx=20, pady=20)

    button_bg = '#D5E0EE'

    myButton = partial(Button, root, bg=button_bg, padx=8, pady=8, width=7, height=6)

    button7 = myButton(text='7', command=lambda: get_input(entry, '7'))
    button7.grid(row=1, column=0)

    button8 = myButton(text='8', command=lambda: get_input(entry, '8'))
    button8.grid(row=1, column=1)

    button9 = myButton(text='9', command=lambda: get_input(entry, '9'))
    button9.grid(row=1, column=2)

    button4 = myButton(text='4', command=lambda: get_input(entry, '4'))
    button4.grid(row=3, column=0)

    button5 = myButton(text='5', command=lambda: get_input(entry, '5'))
    button5.grid(row=3, column=1)

    button6 = myButton(text='6', command=lambda: get_input(entry, '6'))
    button6.grid(row=3, column=2, pady=40, padx=40)

    button1 = myButton(text='1', command=lambda: get_input(entry, '1'))
    button1.grid(row=5, column=0)

    button2 = myButton(text='2', command=lambda: get_input(entry, '2'))
    button2.grid(row=5, column=1)

    button3 = myButton(text='3', command=lambda: get_input(entry, '3'))
    button3.grid(row=5, column=2, pady=40, padx=40)

    button0 = myButton(text='0', command=lambda: get_input(entry, '0'))
    button0.grid(row=7, column=0, pady=40, padx=40)

    button15 = myButton(text='退格', bg=button_bg,
                        command=lambda: backspace(entry))
    button15.grid(row=7, column=6)

    button17 = myButton(text='確定', bg=button_bg,
                        command=lambda: enter(entry))
    button17.grid(row=7, column=7, pady=40, padx=40)

    root.mainloop()


def pic2():
	Txt = Text(root2, height=2, width=30, font="Helvetica 20 bold")
	Txt.grid(row=0, column=0, padx=30, pady=30)
	Txt.insert(END, "請點選圖片")
	Txt.config(state='disabled')

	global length
	global button2
	global idx
	global idx2
	# print(length)
	if length == 1:
		temp = PhotoImage(file=li[0])
		name = li[0].split('.')[0]
		if name in time_list:
			idx = time_list.index(name)
		button1 = Button(root2, image=temp, bg='#FF8800',
						 command=lambda: button1_flate())
		button3 = Button(root2,text="返回",height=10, width=20,fg="#ff0000",
						command=lambda: return_pic1())
		button1.grid(row=5, column=10, padx=50, pady=50)
		button3.grid(row=8, column=50, padx=50, pady=50)
		# print(name)
		# print(time_list)
		# print(idx)
		button2.grid_forget()

	elif length == 2:
		temp = PhotoImage(file=li[0])
		temp2 = PhotoImage(file=li[1])
		name = li[0].split('.')[0]
		name2 = li[1].split('.')[0]
		if name in time_list:
			idx = time_list.index(name)
		if name2 in time_list:
			idx2 = time_list.index(name2)
		button1 = Button(root2, image=temp, bg='#FF8800',
						 command=lambda: button1_flate())
		button2 = Button(root2, image=temp2, bg='#6FEF00',
						 command=lambda: button2_flate())
		button3 = Button(root2,text="返回",height=10, width=20,fg="#ff0000",
							command=lambda: return_pic1())
		button1.grid(row=5, column=10, padx=50, pady=50)
		button2.grid(row=5, column=30, padx=50, pady=50)
		button3.grid(row=8, column=50, padx=50, pady=50)
		
	root2.mainloop()


def pic3():
	global flate
	global idx
	global idx2
	if (flate):
		temp = PhotoImage(file=li[1])
		button = Button(root3, image=temp, bg='#6FEF00')
		button.grid(row=10, column=50, padx=50, pady=50)
	else:
		temp = PhotoImage(file=li[0])
		button = Button(root3, image=temp, bg='#FF8800')
		button.grid(row=10, column=50, padx=50, pady=50)

	Txt = Text(root3, height=2, width=30, font="Helvetica 20 bold", foreground="#DB7093")
	Txt.grid(row=50, column=50, padx=30, pady=30)
	if idx < idx2 and idx2 == 10000:
		Txt.insert(END, s2t(idx + 1))
	elif idx > idx2 and idx == 10000:
		Txt.insert(END, s2t(idx2 + 1))
	button88 = Button(root3, text='確定', height=10, width=20,fg="#0015ff",
						command=lambda: enter2())
	button88.grid(row=100, column=100)
	button3 = Button(root3,text="返回",height=10, width=20,fg="#ff0000",
							command=lambda: return_pic1())
	button3.grid(row=100, column=50)

	root3.mainloop()


if __name__ == '__main__':
	dbx = dropbox.Dropbox('8v5hwjJC9gAAAAAAAAAAjUBwI0c6uuV1voodtcgSpGbiYnAR9XsZovlZOXsZ4uB_')
	work_path = "C:\\PICS\\"
	inp = ""
	li = []
	length = 0
	flate = False
	time_list = []
	global_timestamp = ""
	idx = 10000
	idx2 = 10000
	root = Tk()
	root.attributes("-fullscreen", True)
	root2 = Toplevel()
	root2.attributes("-fullscreen", True)
	root3 = Toplevel()
	root3.attributes("-fullscreen", True)
	button2 = Button(root2)
	pic1()
