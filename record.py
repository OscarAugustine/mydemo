#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *
from os import mkdir, path
import dropbox

dbx = dropbox.Dropbox('8v5hwjJC9gAAAAAAAAAAjUBwI0c6uuV1voodtcgSpGbiYnAR9XsZovlZOXsZ4uB_')
root = Tk()
root.geometry("1024x768")
root.resizable(False, False)
f = ""
idx = '1.0'
if not path.isdir("C:\\PICS"):
    mkdir("C:\\PICS")
create = open("C:/PICS/License_plate_record.txt", "w")
create.close()

fram = Frame(root)
Label(fram, text='文字尋找:').pack(side=LEFT)
edit = Entry(fram)
edit.pack(side=LEFT, fill=BOTH, expand=1)
edit.focus_set()
butt = Button(fram, text='找下一個')
butt.pack(side=RIGHT)
fram.pack(side=TOP)
scrollbar = Scrollbar()
scrollbar.pack(side=RIGHT,fill=Y)


def find():
	global idx 
	text.tag_remove('found', '1.0', END)
	s = edit.get()
	if s:
		# 從頭開始
		# nocase=True不區分大小寫
		idx = text.search(s, idx, nocase=True, stopindex=END)
		if not idx:
			idx ='1.0'
			text.see(idx)
			idx = text.search(s, idx, nocase=True, stopindex=END)
			if idx:
				lastidx = '%s+%dc' % (idx, len(s))
				text.see(idx)
				text.tag_add('found', idx, lastidx)
				idx = lastidx
				#print(idx)
				text.tag_config('found', foreground='red')
			else:
				idx ='1.0'
				text.see(idx)
		else:
			lastidx = '%s+%dc' % (idx, len(s))
			text.see(idx)
			text.tag_add('found', idx, lastidx)
			idx = lastidx
			#print(idx)
			text.tag_config('found', foreground='red')
		

butt.config(command=find)


def txt_download_db():
    files = dbx.files_list_folder('')
    entries = files.entries
    for file in entries:
        name = file.name
        if name.find("License_plate_record", 0, len(name) - 4) != -1:
            with open("C:\\PICS\\" + name, "wb") as f:
                name = "License_plate_record.txt"
                metadata, res = dbx.files_download(path="/" + name)
                f.write(res.content)


def read_file():
    txt_download_db()
    f = open("C:/PICS/License_plate_record.txt", "r").read()
    text.config(state='normal')
    text.delete('1.0', END)
    text.insert(END, "車牌號碼\t\t進場時間\t\t\t離場時間\n\n" + "".join(f))
    text.config(state='disabled')
    root.after(10000, read_file)


text = Text(root, font="Helvetica 18 bold",yscrollcommand=scrollbar.set)
text.pack(fill='y')
scrollbar.config(command=text.yview)
root.after(0, read_file)
root.mainloop()