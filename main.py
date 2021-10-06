import shutil
from datetime import date
import os
import re
from time import sleep
import time
from PySimpleGUI import PySimpleGUI as sg

today = date.today()
srcdir = r"C:\Users\meier\Documents"
destdir = r"E:"
folder = "THALES"
filename = f"BACKUP {today}"
erase = True
pych = True

def MakeBackup(srcdir = srcdir, destdir = destdir, filename = filename, erase = erase, pych = pych):
  t0= time.time()
  sg.Print("\n Iniciando...")

  if pych == True:
    shutil.make_archive(r"{}\{}\PycharmProjects".format(srcdir,folder), 'zip', r"C:\Users\meier", "PycharmProjects")

    sg.Print('\n Criado Backup da pasta do PyCharm')

  shutil.make_archive(r"{}\{}".format(srcdir, filename), 'zip', srcdir, folder)

  sg.Print("\n Criado Backup principal")

  if os.path.exists(r"{}\THALES\PycharmProjects.zip".format(srcdir)):
    os.remove(r"{}\THALES\PycharmProjects.zip".format(srcdir))
    sleep(0.7)
    sg.Print("\n Removida cópia da pasta do PyCharm")
  else:
    sg.Print("")
    sg.Print(" Pasta do PyCharm não foi movida",text_color='red')
    sleep(0.7)

  try:
    shutil.move(r"{}\{}.zip".format(srcdir, filename), r"{}\{}.zip".format(destdir, filename))

    sg.Print('\n Backup movido para o HD externo')
    sleep(0.7)

    if erase == True:
      pattern = re.compile(r"BACKUP*")

      for item in os.listdir(destdir):
        if pattern.search(item) != None:
          file_date = item.replace('BACKUP ', '').split('.')[0]
          if file_date != f"{today}":
            os.remove(r"{}\{}".format(destdir, item))

      sg.Print('\n Backup antigo apagado!')
      sleep(0.7)
  except FileNotFoundError:
    sg.Print("")
    sg.Print(" HD NÃO CONECTADO!",text_color='white',background_color='red')
    sleep(0.7)

  t1 = time.time() - t0
  sg.Print(f"\n Feito! Tempo total: {t1:02} seg")
  sleep(5)

#GUI SETUP
sg.theme("Reddit")


layout = [
  [sg.Text(f"PYTHON AUTO BACKUP - {today}",font=("Lato",14,'bold'))],
  [sg.Text(f"\n")],
  [sg.Text("Backup from: ",size=(13,1)),sg.Input(key='srcdir',default_text=srcdir)],
  [sg.Text("Folder name: ",size=(13,1)),sg.Input(key='folder',default_text=folder)],
  [sg.Text("Backup to: ",size=(13,1)),sg.Input(key='destdir',default_text=destdir)],
  [sg.Text("Include PyCharm: ",size=(13,1)),sg.Checkbox(text = None,key='pych', default=True)],
  [sg.Text("Erase Old: ",size=(13,1)),sg.Checkbox(text = None,key='erase', default=True)],
  [sg.Text(f"The file will be saved as {filename}",font=("Arial",11,'italic'))],
  [sg.Text(f"")],
  [sg.Submit(button_text="Iniciar")]
]

window = sg.Window('#TAL AUTO BACKUP - v 0.8',layout)

while True:
    event, values = window.read()
    srcdir = values['srcdir']
    destdir = values['destdir']
    folder = values['folder']
    erase = values['erase']
    pych = values['pych']
    if event == 'Iniciar':
      MakeBackup()
      window.close()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break

window.close()
