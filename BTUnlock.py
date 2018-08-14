from tkinter import *           #import the layout information from tkinter
import os
from tkinter import ttk
import tkinter

def checkBluetooth():
     while True:
          os.system("rm -R rssilog.txt")
          os.system("""rs=`system_profiler SPBluetoothDataType | grep -E "Connected.*Yes" `\necho $rs>> /Users/Edon/Desktop/rssilog.txt;""")
          file = open("rssilog.txt","r")
          connected = str(file.read(20)[17:])
          if len(connected) == 0:
               print("please connect a device")
          else:
               os.system("rm -R rssilog.txt")
               os.system("rs=`system_profiler SPBluetoothDataType | grep Bluetooth.Power`\necho $rs>> /Users/Edon/Desktop/rssilog.txt;")
               file = open("rssilog.txt","r")
               bluetooth = str(file.read(20)[17:])
               
               if bluetooth == "Off":
                    BT.set("OFF")
                    root.update()
               else:
                    BT.set("ON")
                    root.update()


def calculateDistance(rssi):
     txPower = -54

     if rssi == 0:
          return (-1.0)

     ratio = rssi*(1.0/txPower)

     if ratio < 1.0:
          return ratio**10

     else:
          distance1 = (0.89976)*(ratio**7.7095) + 0.111
          return distance1


def checkRange(*args):
     status = False
     passwordstr = str(password.get())
     distance = int(dist.get())
     try:
          while True:
               os.system("rm -R rssilog.txt")
               root.update()
               if status == False:
                    os.system("rs=`system_profiler SPBluetoothDataType | grep RSSI`\necho $rs>> /Users/Edon/Desktop/rssilog.txt;")

                    file = open("rssilog.txt","r")
                    rssi = int(file.read(9)[6:])

                    if calculateDistance(rssi) > distance:

                         status = True
                         os.system("""osascript -e 'tell application "finder" to sleep'""")

                    else:
                         print(calculateDistance(rssi))

                         status = False


               elif status == True:
                    os.system("rs=`system_profiler SPBluetoothDataType | grep RSSI`\necho $rs>> /Users/Edon/Desktop/rssilog.txt;")

                    file = open("rssilog.txt","r")
                    rssi = int(file.read(9)[6:])

                    if calculateDistance(rssi) < distance:
                         status = False
                         os.system("""osascript -e 'tell application "system events" to key code 123'\nosascript -e 'tell application "system events" to keystroke """+'"'+passwordstr+'"'+"""'\nosascript -e 'tell application "system events" to keystroke return'""")
                         os.system("""caffeinate  -u -t 6""")

                    else:
                         status = True

     except ValueError:
          print("Please insert values or turn BT on")
 

root = Tk()
root.title("Bluetooth Unlock")
root.resizable(0,0)
mainframe = ttk.Frame(root, padding = "6 6 6 6")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)


BT = StringVar()
password = StringVar()
dist = IntVar()

password_entry = ttk.Entry(mainframe, width = 15, textvariable = password, show = "*")
password_entry.grid(column = 2, row = 1, sticky = (W, E))
dist_entry = ttk.Entry(mainframe, width = 15, textvariable = dist)
dist_entry.grid(column = 2, row = 2, sticky = (W, E))

ttk.Label(mainframe, textvariable = BT).grid(column = 4, row = 1, sticky = W)

ttk.Label(mainframe, text = "Bluetooth status:").grid(column = 3, row = 1, sticky = W)

ttk.Button(mainframe, text = "Activate BT Unlock", command = checkRange).grid(column = 3, row = 2, sticky = W)

ttk.Label(mainframe, text="Password").grid(column=1, row=1, sticky=E)
ttk.Label(mainframe, text="Distance").grid(column=1, row=2, sticky=E)
ttk.Label(mainframe, text="Device").grid(column=1, row=3, sticky=E)

var1 = StringVar(root)
for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)


password_entry.focus()
checkBluetooth()
root.mainloop()

















