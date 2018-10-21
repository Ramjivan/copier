#!/usr/bin/env python3

import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter.ttk import *
from tkinter import *
import sys , pyudev ,threading
from subprocess import *
import shlex ,os ,math, pyfastcopy ,shutil ,time
from functools import partial
import tkinter.font as tkfont


def dusb():
    temp = getoutput("df -B1 | grep -vE '^Filesystem|tmpfs|cdrom' | awk '{ print $6 }'|tail -n +3")
    global mpoint
    mpoint = [""]
    mpoint = temp.split()
    temp = getoutput("df -B1 | grep -vE '^Filesystem|tmpfs|cdrom' | awk '{ print $2 }'|tail -n +3")
    global size
    size = [""]
    size = temp.split()
    temp = getoutput("df -B1 | grep -vE '^Filesystem|tmpfs|cdrom' | awk '{ print $3 }'|tail -n +3")
    global use
    use = [""]
    use = temp.split() 
    temp = getoutput("df -B1 | grep -vE '^Filesystem|tmpfs|cdrom' | awk '{ print $4 }'|tail -n +3")
    global avail
    avail = [""]
    avail = temp.split()
    temp = getoutput("df -B1 | grep -vE '^Filesystem|tmpfs|cdrom' | awk '{ print $1 }'|tail -n +3")
    global sysloc
    sysloc = [""]
    sysloc = temp.split()
    print(sysloc)
    temp = getoutput("df -B1 | grep -vE '^Filesystem|tmpfs|cdrom' | awk '{ print $5 }'|tail -n +3")
    global uper
    uper = [""]
    uper = temp.split()

class USBDetector():
    
    ''' Monitor udev for detection of usb '''
    def __init__(self):
        ''' Initiate the object '''
        thread = threading.Thread(target=self._work)
        copyspeed_t = threading.Thread(target=self._cs)
        thread.daemon = True
        copyspeed_t.daemon = True
        copyspeed_t.start()
        thread.start()
        
    '''Monitor main usb bus by dstat on shell '''
    def _cs(self):
        while True:
            cmd = "dstat -d 001 1"
            p=getoutput(cmd)
            po=p.split('\n')[-1]
            writ=po.split(' ')[-1]
            read=po.split(' ')[1]
            T_read.config(text = read)
            T_writ.config(text = writ)

    ''' Runs the actual loop to detect the events '''
    def _work(self):
        self.context = pyudev.Context()
        self.monitor = pyudev.Monitor.from_netlink(self.context)
        self.monitor.filter_by(subsystem='usb')
        self.monitor.start()
        for device in iter(self.monitor.poll, None):
            
            if device.action == 'add':
                # insertion of usb
                time.sleep(2)
                ulist()
            else:
                # removal of usb
                ulist()
USBDetector()

def ulist():
    
    dusb()
    
    global drivesFrame
    try: 
        drivesFrame
    except NameError:
        print("No drivesFrame")
    else:   
        drivesFrame.destroy()
    
    drivesFrame = Frame(master=canvas)
    
    drivesFrame.pack(side=LEFT, fill='x')
    canvas.create_window((0,0), window=drivesFrame, anchor='n',width=240)
    
    i = 0

    global dynamic_status
    dynamic_status = []
    
    while (i < len(mpoint)):
        
          tup1 = "USB "+str(i)
          print (tup1)
          vars()[tup1] = tk.LabelFrame(drivesFrame, width=240, text=tup1,font=("Helvetica", 10))
          vars()[tup1].pack(fill='x', )
          
          tup = "mpoint"+str(i)
          test = Label(vars()[tup1], text="Mount Point -",font=("Helvetica", 8))
          test.grid(row=1, column=1, sticky='e')
          vars()[tup] = Label(vars()[tup1], text=mpoint[i],fg="blue", cursor='xterm', takefocus=1, font=("Helvetica", 8))
          vars()[tup].grid(row=1, column=2)
          vars()[tup].bind('<Button-1>',lambda event, y=mpoint[i]: file_e(y) )
        
          test = Label(vars()[tup1], text="Capacity -",font=("Helvetica", 8))
          test.grid(row=2, column=1, sticky='e')
          tup = "size"+str(i)
          vars()[tup] = Label(vars()[tup1], text=[convert_size(int(size[i]))],font=("Helvetica", 8))
          vars()[tup].grid(row=2, column=2)

          test = Label(vars()[tup1], text="Uses Memory -",font=("Helvetica", 8))
          test.grid(row=3, column=1, sticky='e')
          tup = "use"+str(i)
          vars()[tup] = Label(vars()[tup1], text=[convert_size(int(use[i]))],font=("Helvetica", 8))
          vars()[tup].grid(row=3, column=2)

          test = Label(vars()[tup1], text="Available -",font=("Helvetica", 8))
          test.grid(row=4, column=1, sticky='e')
          tup = "avail"+str(i)
          vars()[tup] = Label(vars()[tup1], text=[convert_size(int(avail[i]))],font=("Helvetica", 8))
          vars()[tup].grid(row=4, column=2)
      
          tup = "uper"+str(i)
          vars()[tup] = ttk.Progressbar(vars()[tup1],orient=tk.HORIZONTAL, mode='determinate')
          vars()[tup]["maximum"] = 100
          vars()[tup].grid(row=5, column=2)
          tamp = uper[i].rstrip('%')
          vars()[tup]["value"] = tamp

        #  tup = "slusb"+str(i)
        #  tup2 = "SUSB"+str(i)
        #  vars()[tup2]= tk.IntVar(value=1)
        #  vars()[tup] = tk.Checkbutton(vars()[tup1], variable=vars()[tup2], text="slect ", width=10)
        #  vars()[tup].grid(row=2, column=3,) 
           
             
          status = Label(vars()[tup1], text="wating",font=("Helvetica", 8))
          dynamic_status.append(status)
          status.grid(row=6, column=1, columnspan=3)

          tup = "format"+str(i)
          vars()[tup]= tk.Button(vars()[tup1],command=lambda a=sysloc[i],b=mpoint[i]:fmat(a, b), text= "FORMAT",font=("Helvetica", 5))
          vars()[tup].grid(row=3, column=3,)
      
          i= i + 1

    global copysource

    if 1==len(mpoint):
                copysource.grid(row=7, column=2)
    else:
        print("try deleteing")
        copysource.grid_remove()



#---------------------------------------------------------------------------------------------------------------------------------------------------------------def run_command(command):

class USBcopier():
    
    def __init__(self):
        
        list_copy=[""]
        list_speed=[""]
        g = 0
        global seleccion
        seleccion = filelist.curselection()

        temp_size=list(size)
        temp_names=list(names)
        temp_avail=list(avail)
        temp_tfsize=tfsize
        global timercount
        timercount=int(0)
        pp=int(len(mpoint))
        time_thread=threading.Thread(target=partial (self._timer,pp))
        time_thread.start()
        
        while (g < len(mpoint)):
            dynamic_status[g].config(text = "copy = 0%" )
            dynamic_status[g].bind('<Button-1>',lambda event, y=mpoint[g]: file_e )
            dynamic_status[g].update()
            
            copythread = threading.Thread(target=partial (self._extra,g,temp_size,temp_names,temp_avail,temp_tfsize))
            copythread.start()
            g = g + 1

        
    def _timer(self,pp):
        start=time.time()
        global timercount
        while True:
            curenttime=time.time()
            time.sleep(1)
            
            t=time.strftime("%H:%M:%S",time.gmtime(curenttime-start))
            Timert.config(text=t)
                         
            if timercount==pp :
                break

            
    def _extra(self,g,temp_size,temp_names,temp_avail,temp_tfsize):
        
        t = 0
        
        if temp_tfsize<=int(temp_avail[g]):
            print(temp_size)
            print(temp_names)        
            for i in seleccion:
                    print(list(temp_size))
                    t = t + int(temp_size[i])
                    d = mpoint[g]
                    n = temp_names[i]
                    src=str(sor+'/'+n)
                    dst=str(d+'/'+n)
                   
                    try:
                        shutil.copytree(src, dst)
                            
                    except FileExistsError:
                        dynamic_status[g].config(text ="all redy have")
                        dynamic_status[g].update()
                        continue
                    except NotADirectoryError:
                        aaa=str(getoutput("[ -f '"+dst+"' ] || printf '1'"))
                        print("[ -f '"+dst+"' ] || printf '1'")
                        if aaa == '1':
                            print ("i all copy")
                            shutil.copy(src, dst)
                        else:
                            print ("i all ready")
                            dynamic_status[g].config(text ="all redy have")
                            dynamic_status[g].update()
                            continue
                        
                    status= t/temp_tfsize*100
                    si=int(status)
                    dynamic_status[g].config(text = "copy = "+str(si)+"%")
                    dynamic_status[g].update()
                    print("status: ", si)
                
        else:
            dynamic_status[g].config(text = "not enough space make copy")
            dynamic_status[g].update()
        global timercount
        timercount=timercount + 1
        


 
def convert_size(size_bytes):
   if size_bytes == 0:
       return "0  Bytes"
    
   size_name = ("By", "KB", "MB", "GB", "TB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])



def on_configure(event):

    canvas.configure(scrollregion=canvas.bbox('all'))


def sloc():
    global sor
    try: 
        os.chdir(sor)
    except NameError:
        print("source not selected")
        sor="/home/pi/Source"
    except TypeError:
        print("TypeError")
        sor="/home/pi/Source"
    except FileNotFoundError:
        print("FileNotFoundError")
        sor="/home/pi/Source"
    else:   
        os.chdir(sor)
        sor = filedialog.askdirectory()
    
    entryText.set(sor)
    os.chdir(sor)

    global dsize
    global names
    global size
    fname=[""]
    dname=[""]
    fsize=[""]
    dsize=[""]
    temp = getoutput("stat -c '%F %n' * | grep 'regular file' | cut -d' ' -f 3-")
    fname = list(temp.split("\n"))
    temp = getoutput("stat -c '%F %n' * | grep 'directory' | cut -d' ' -f 2-")
    dname = list(temp.split("\n"))
    temp = getoutput("stat -c '%F %s' * | grep 'regular file' | cut -d' ' -f 3-")
    fsize = list(temp.split("\n"))
    temp = getoutput("du -s *// | awk '{ print $1 }'")
    dsize = list(temp.split("\n"))
    size=[""]
    names=[""]
    size = dsize+fsize
    names = dname+fname
    flist.set(names)
    for i in range(len(dname)):
        filelist.itemconfig(i, {'fg': 'blue'})

def select(evt):
    global tfsize
    tfsize = int()
    selecsion = filelist.curselection()
    for i in selecsion:
        entrada = size[i]
        tfsize = tfsize + int(entrada)
            
    B = convert_size(tfsize)
    label4.config(text = B, width = "15")


def D_selector():
    A = lsl.get()
    if A == 1 :
        filelist.selection_set(0,tk.END)
        filelist.update()
        listsle.config(text="deselect all")
        select('ListboxSelect')
 
    else :
        filelist.selection_clear(0,tk.END)
        filelist.update()
        listsle.config(text="select all")
        select('ListboxSelect')

def file_e(string):
    os.chdir(string)
    print(string)
    getoutput('pcmanfm')
    os.chdir(sor)

def type_format(mn,b,a,d):
    getoutput("sudo umount "+a)
    
    if d=="ext4":
        getoutput("yes | sudo mkfs."+d+" "+a+" -n Santvani ")

    elif d=="ntfs":
        
        getoutput("sudo mkfs."+d+" "+a+" -f -v -I -n Santvani")
    else:
        getoutput("sudo mkfs."+d+" "+a+" -n Santvani")
        
    #getoutput("sudo e2label "+a+" /Santvani")
    getoutput("udisksctl mount --block-device "+a)
    #getoutput("sudo e2label "+a+" /Santvani")

    ulist()
    
    mn.destroy()
    
def fmat(a, b):
    mn = Toplevel(bg="gray")
    mn.wm_attributes('-type', 'splash')
    mn.lift(aboveThis=root)
    
    button = Button(mn, text="vFat32", command= lambda d="vfat": type_format(mn,b,a,d) ,width=20)
    button.pack()
    button = Button(mn, text="NTFS", command= lambda d="ntfs":type_format(mn,b,a,d),width=20)
    button.pack()
    button = Button(mn, text="ext4", command= lambda d="ext4": type_format(mn,b,a,d),width=20)
    button.pack()
    button = Button(mn, text="Nothing", command =mn.destroy,width=20)
    button.pack()


    
        
    
    
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
global root
root = tk.Tk()
root.title("USB Copier Utility")
ww=str(root.winfo_screenwidth())
hh=str(root.winfo_screenheight()-20)
root.geometry(ww+"x"+hh+"+0+0")
root.wm_attributes('-type', 'splash')
root.focus_set()  # <-- move focus to this widget

Frame2 = Frame(root,bg="black",height=20)
Frame2.pack(side=BOTTOM,fill='x')

textr=Label(Frame2,text="USB BUS READ :",bg="black",fg="white").grid(row=1, column=1)
T_read=Label(Frame2,bg="black",fg="white",width=6)
T_read.grid(row=1, column=2)
textw=Label(Frame2,text=" WRITE :",bg="black",fg="white").grid(row=1, column=3)
T_writ=Label(Frame2,bg="black",fg="white",width=6)
T_writ.grid(row=1, column=4)

Timert=Label(Frame2,text="00:00:00",bg="black",fg="white",width=8)
Timert.grid(row=1,column=6,sticky=E)
texttco=Label(Frame2,text="Timer",bg="black",fg="white").grid(row=1,column=5)

canvas = tk.Canvas(root, width=240)
canvas.pack(side=LEFT, fill='y')

scrollbar = tk.Scrollbar(root, command=canvas.yview)
scrollbar.pack(side=LEFT, fill='y')

canvas.configure(yscrollcommand = scrollbar.set)

canvas.bind('<Configure>', on_configure)
global a


Frame1 = Frame(root)
Frame1.pack(side=LEFT,fill='y')

def copySOR():
    os.chdir(mpoint[0])
    Ssize=[""]
    Sname=[""]
    temp = getoutput("stat -c '%F %n' * | grep 'regular file' | cut -d' ' -f 3-")
    Sname = list(temp.split("\n"))
    temp = getoutput("stat -c '%F %n' * | grep 'directory' | cut -d' ' -f 2-")
    Sname +=list(temp.split("\n"))
    temp = getoutput("stat -c '%F %s' * | grep 'regular file' | cut -d' ' -f 3-")
    Ssize = list(temp.split("\n"))
    temp = getoutput("du -s *// | awk '{ print $1 }'")
    Ssize+=list(temp.split("\n"))
    print(Sname,Ssize)
    print(len(Ssize))
    to=0
    t=0
    for t in range(len(Ssize)):
        to=to+int(Ssize[t])
        print(to)

    t=0
    for i in range(len(Ssize)):
        print("======="+str(t))
        t = t + int(Ssize[i])
        d = "/home/pi/Source"
        n = Sname[i]
        src=str(mpoint[0]+'/'+n)
        dst=str(d+'/'+n)       
        try:
            shutil.copytree(src, dst)
                            
        except FileExistsError:
            print("alrady")
            continue
        except NotADirectoryError:
            aaa=str(getoutput("[ -f '"+dst+"' ] || printf '1'"))
            print("[ -f '"+dst+"' ] || printf '1'")
            if aaa == '1':
                print ("i all copy")
                shutil.copy(src, dst)
            else:
                print("alrady")
                continue
        status= t/to*100
        status=int(status)
        lablee.configure(text="copy = "+str(status)+"%")
        lablee.update
        temp_prog["value"]=status
        temp_prog.update
        t=t+1
            

def cleanSor():
    getoutput("sudo rm -rf '/home/pi/Source'")
    getoutput("mkdir '/home/pi/Source'")
    temp_prog["value"]=100
    lablee.configure(text="source DIR clear")
    lablee.update
    temp_prog.update
    
    

def CopySOR_b():
    top = Toplevel(bg="gray")
    top.wm_attributes('-type', 'splash')
    top.attributes('-topmost', 'true')
    top.grab_set()
    global lablee
    lablee=Label(top,text="Chose opretion")
    lablee.pack()
    global temp_prog
    temp_prog = ttk.Progressbar(top,orient=tk.HORIZONTAL, length=190, mode='determinate')
    temp_prog["maximum"] = 100
    temp_prog.pack()
    button = Button(top, text="Copy Source", command=copySOR,width=20)
    button.pack()
    button = Button(top, text="Clean Source",command=cleanSor,width=20)
    button.pack()
    button = Button(top, text="Nothing", command=top.destroy,width=20)
    button.pack()
    

copysource = tk.Button(Frame1,command=CopySOR_b, text="Sorce copy",font=("Helvetica", 8))
ulist()

label2 = Label(Frame1, text ="source",font=("Helvetica", 8,"bold")).grid(row=1, column=1, sticky=W)

entryText = tk.StringVar()
scrloc = Entry(Frame1, width=21, textvariable=entryText)
scrloc.grid(row=2, column=1,columnspan=2, sticky=tk.E+tk.W)

flist = tk.StringVar()
filelist = tk.Listbox(Frame1, selectmode=tk.MULTIPLE, listvariable=flist ,font=("Helvetica", 8),width=31)
filelist.grid(row=3, column=1, columnspan=2,sticky=W)

slb = tk.Button(Frame1, command=sloc, text="O O O",font=("Helvetica", 3,"bold"))
slb.grid(row=2, column=3,sticky=W)
filelist.bind('<<ListboxSelect>>', select)

sloc()

slist = Scrollbar(Frame1, orient="vertical",width=15)
slist.grid(row=3, column=3, sticky=W+N+S )
slist.config(command=filelist.yview)
filelist.config(yscrollcommand=slist.set)

label3 = Label(Frame1, text ="Selected Size",font=("Helvetica", 8))
label3.grid(row=5, column=1, sticky=W, columnspan=2)

label4 = Label(Frame1, text="0 Bytes",font=("Helvetica", 8))
label4.grid(row=5, column=2, sticky=W)

lsl = IntVar()
listsle = Checkbutton(Frame1, variable=lsl, command=D_selector, text="slect all",font=("Helvetica", 8), width=10)
listsle.grid(row=4, column=1,sticky=W)

makecopy = tk.Button(Frame1, text="MakeCopies", command=lambda:USBcopier(),font=("Helvetica", 8))
makecopy.grid(row=6, column=2)

def shutdown():
    getoutput(" sudo sleep 3s; shutdown -h now")
        
def close():
    top = Toplevel(bg="gray")
    top.wm_attributes('-type', 'splash')
    top.attributes('-topmost', 'true')
    top.grab_set()
    
    msg = Message(top, text="What you want's")
    msg.pack()
    button = Button(top, text="Close Program", command=root.destroy,width=20)
    button.pack()
    button = Button(top, text="Shutedown system", command = shutdown,width=20)
    button.pack()
    button = Button(top, text="Nothing", command=top.destroy,width=20)
    button.pack()
    
    
    
close = Button (Frame1, text = "Close", command = close,font=("Helvetica", 8))
close.grid(row=1, column=2)

root.mainloop()
