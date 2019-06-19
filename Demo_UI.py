import sys
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from tkinter import filedialog
from tkinter import messagebox
import  PIL
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk
import CNN as cnn

try:
    import ttk

    py3 = False
except ImportError:
    import tkinter.ttk as ttk

    py3 = True


def vp_start_gui(Form_Number):
    global val, w, root, top1, Dis, Desc, Tre
    root = tk.Tk()
    top1 = Toplevel1(root, Form_Number)
    root.mainloop()

w = None



class call_back_end:
    def Create_Model(FilePath,modelname):
        trainpath = FilePath + "/train"
        validpath = FilePath + "/valid"
        try:
            x =cnn.DataSetFunctions.new_Train(trainpath, validpath,modelname)
        except:
            if(top1.Entry1.get() == ''):
                messagebox.showerror("Error", " write model name ")
            elif (top1.Entry1_10.get() == ''):
                messagebox.showerror("Error", "select file path")
            else:
                messagebox.showerror("Error", "Make Sure that you select the correct folder")

        print('aacc ',x)
    def Test_Model(FolderPath, ModelName, Type,flag):
        if(flag == 1):
            try:
                Data = cnn.DataSetFunctions.read_folder(FolderPath)
            except:
                messagebox.showerror("Error", "Error in test Make sure that you select the correct folder")
            MetaDataFile = 'MetaData/'+Type + ".txt"

            MetaData = cnn.Get_Features.LoadMetaData(MetaDataFile)
            Diseases = cnn.DataSetFunctions.CheckFoledOfImages(Data, ModelName, MetaData)
            Dis=Diseases[0][0]
            ratio=str(Diseases[0][1]*100)+'%'
            Desc=Diseases[1][0]
            Tre=Diseases[1][1]
            mes=messagebox.showinfo("Disease",Dis+' Disease ,the ratio of disease is '+ratio)
            print(Dis)
        else:
            try:
                Data=cnn.DataSetFunctions.single_image(FolderPath,ModelName)
            except:

                messagebox.showerror("Error", "Error In Read Image Please make sure the you select the correct image")
            Dis=Data[0]
            Desc=Data[1][0]
            Tre=Data[1][1]
            print(Data[0])
            print(Data[1])
            mes = messagebox.showinfo("Disease",'The leaf has '+ Dis + ' Disease ')

        return Dis,Desc,Tre
    def Update_In_Track(FolderPath ,TrackID):
        cnn.Tracking.Update_Tracking(TrackID,FolderPath)
    def CreateNewTrack(TrackName ,PlantType):
        cnn.Tracking.Create_New_Track(TrackName,PlantType)
    def ShowGraph(TrackID):
        cnn.Tracking.create_graph(TrackID)
class Home_Form_Setting:
    def creat_browse_button():
        str1 = None
        if Toplevel1.flag == 1:
            fplder = filedialog.askdirectory()
            str1 = fplder
        elif (Toplevel1.flag == 0):
            filetype = (('Portable Network Graphics', '*.png'), ("All files", "*.*"))
            filename = askopenfilename(initialdir="C:/Users", filetypes=filetype, title="fdf")
            str1 = filename
        top1.update_Entry(str1, Toplevel1.Level)

    def changeflag():
        if (Toplevel1.flag == 0):
            Toplevel1.flag = 1
        elif (Toplevel1.flag == 1):
            Toplevel1.flag = 0


class Toplevel1:
    flag = 0
    Level = None
    Dis= ''
    Desc=''
    Tre=''

    def __init__(self, top=None, Number=None):
        Toplevel1.Level = Number
        if Number == 0:
            Toplevel1.flag = 0
            _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
            _fgcolor = '#000000'  # X11 color: 'black'
            _compcolor = '#d9d9d9'  # X11 color: 'gray85'
            _ana1color = '#d9d9d9'  # X11 color: 'gray85'
            _ana2color = '#ececec'  # Closest X11 color: 'gray92'
            self.style = ttk.Style()
            if sys.platform == "win32":
                self.style.theme_use('winnative')
            self.style.configure('.', background=_bgcolor)
            self.style.configure('.', foreground=_fgcolor)
            self.style.configure('.', font="TkDefaultFont")
            self.style.map('.', background=
            [('selected', _compcolor), ('active', _ana2color)])

            top.geometry("737x450+269+167")
            top.title("Home")
            top.configure(background="#ffffff")
            top.configure(highlightbackground="#f0f0f0f0f0f0")
            top.configure(highlightcolor="#646464646464")

            self.menubar = tk.Menu(top, font="TkMenuFont", bg='#ffffff', fg='#ffffff')
            top.configure(menu=self.menubar)

            self.Button1 = tk.Button(top)
            self.Button1.place(relx=0.841, rely=0.356, height=34, width=107)
            self.Button1.configure(activebackground="#ececec")
            self.Button1.configure(activeforeground="#000000")
            self.Button1.configure(background="#d9d9d9")
            self.Button1.configure(command=Home_Form_Setting.creat_browse_button)
            self.Button1.configure(disabledforeground="#a3a3a3")
            self.Button1.configure(foreground="#000000")
            self.Button1.configure(highlightbackground="#d9d9d9")
            self.Button1.configure(highlightcolor="black")
            self.Button1.configure(pady="0")
            self.Button1.configure(text='''Browse''')
            self.Button1.configure(width=107)

            self.Text1 = tk.Entry(top)
            self.Text1.place(relx=0.461, rely=0.356, relheight=0.053, relwidth=0.358)

            self.Text1.configure(background="white")
            self.Text1.configure(font="TkTextFont")
            self.Text1.configure(foreground="black")
            self.Text1.configure(highlightbackground="#d9d9d9")
            self.Text1.configure(highlightcolor="black")
            self.Text1.configure(insertbackground="black")
            self.Text1.configure(selectbackground="#c4c4c4")
            self.Text1.configure(selectforeground="black")
            self.Text1.configure(width=264)
            # self.Text1.configure(wrap="word")

            self.Test = tk.Button(top,command = Toplevel1.start_Test)

            self.Test.place(relx=0.57, rely=0.622, height=44, width=127)
            self.Test.configure(activebackground="#ececec")
            self.Test.configure(activeforeground="#000000")
            self.Test.configure(background="#fff5fe")
            self.Test.configure(borderwidth=".5")
            self.Test.configure(disabledforeground="#a3a3a3")
            self.Test.configure(font="-family {Segoe UI} -size 12")
            self.Test.configure(foreground="#000000")
            self.Test.configure(highlightbackground="#d9d9d9")
            self.Test.configure(highlightcolor="black")
            self.Test.configure(pady="0")
            self.Test.configure(text='''Start Test''')
            self.Test.configure(width=127)

            self.Label1 = tk.Label(top)
            self.Label1.place(relx=0.299, rely=0.356, height=21, width=101)
            self.Label1.configure(background="#ffffff")
            self.Label1.configure(disabledforeground="#a3a3a3")
            self.Label1.configure(foreground="#000000")
            self.Label1.configure(text='''Choose file/folder''')

            self.Checkbutton1 = tk.Checkbutton(top)
            self.Checkbutton1.place(relx=0.733, rely=0.267, relheight=0.056
                                    , relwidth=0.083)
            self.Checkbutton1.configure(activebackground="#ececec")
            self.Checkbutton1.configure(activeforeground="#000000")
            self.Checkbutton1.configure(background="#ffffff")
            self.Checkbutton1.configure(command=Home_Form_Setting.changeflag)
            self.Checkbutton1.configure(disabledforeground="#a3a3a3")
            self.Checkbutton1.configure(foreground="#000000")
            self.Checkbutton1.configure(highlightbackground="#d9d9d9")
            self.Checkbutton1.configure(highlightcolor="black")
            self.Checkbutton1.configure(justify='left')
            self.Checkbutton1.configure(text='''Folder''')
            #        self.Checkbutton1.configure(variable=Home_support.che48)

            self.TSeparator1 = ttk.Separator(top)
            self.TSeparator1.place(relx=0.237, rely=0.0, relheight=1.0)
            self.TSeparator1.configure(orient="vertical")

            self.HomeBtn = ttk.Button(top, command=Move_Between_Formms.Go_To_Home_Form)
            self.HomeBtn.place(relx=0.0, rely=0.044, height=85, width=176)
            self.HomeBtn.configure(takefocus="")
            self.HomeBtn.configure(text='''Home''')
            self.HomeBtn.configure(width=176)

            self.Statisticsbtn = ttk.Button(top, command=Move_Between_Formms.Go_To_Statistics_Form)
            self.Statisticsbtn.place(relx=0.0, rely=0.233, height=85, width=176)
            self.Statisticsbtn.configure(takefocus="")
            self.Statisticsbtn.configure(text='''Statistics''')

            self.Monitiringbtn = ttk.Button(top, command=Move_Between_Formms.Go_To_Monitiring_Form)
            self.Monitiringbtn.place(relx=0.0, rely=0.422, height=85, width=176)
            self.Monitiringbtn.configure(takefocus="")
            self.Monitiringbtn.configure(text='''Monitiring''')

            self.Model_Btn = ttk.Button(top, command=Move_Between_Formms.Go_To_CreateModel_Form)
            self.Model_Btn.place(relx=0.0, rely=0.611, height=85, width=176)
            self.Model_Btn.configure(takefocus="")
            self.Model_Btn.configure(text='''Create Model''')

            self.Helpbtn = ttk.Button(top, command=Move_Between_Formms.Go_To_Help_Form)
            self.Helpbtn.place(relx=0.0, rely=0.811, height=85, width=176)
            self.Helpbtn.configure(takefocus="")
            self.Helpbtn.configure(text='''Help''')
            Toplevel1.formLevel = top
        elif Number == 3:
            Toplevel1.flag = 1
            _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
            _fgcolor = '#000000'  # X11 color: 'black'
            _compcolor = '#d9d9d9'  # X11 color: 'gray85'
            _ana1color = '#d9d9d9'  # X11 color: 'gray85'
            _ana2color = '#ececec'  # Closest X11 color: 'gray92'
            self.style = ttk.Style()
            if sys.platform == "win32":
                self.style.theme_use('winnative')
            self.style.configure('.', background=_bgcolor)
            self.style.configure('.', foreground=_fgcolor)
            self.style.configure('.', font="TkDefaultFont")
            self.style.map('.', background=
            [('selected', _compcolor), ('active', _ana2color)])

            top.geometry("737x450+269+167")
            top.title("Create Model")
            top.configure(background="#ffffff")
            top.configure(highlightbackground="#f0f0f0f0f0f0")
            top.configure(highlightcolor="#646464646464")

            self.menubar = tk.Menu(top, font="TkMenuFont", bg='#ffffff', fg='#ffffff')
            top.configure(menu=self.menubar)

            self.Button1 = tk.Button(top, command=Home_Form_Setting.creat_browse_button)
            self.Button1.place(relx=0.841, rely=0.356, height=34, width=107)
            self.Button1.configure(activebackground="#ececec")
            self.Button1.configure(activeforeground="#000000")
            self.Button1.configure(background="#d9d9d9")
            self.Button1.configure(disabledforeground="#a3a3a3")
            self.Button1.configure(foreground="#000000")
            self.Button1.configure(highlightbackground="#d9d9d9")
            self.Button1.configure(highlightcolor="black")
            self.Button1.configure(pady="0")
            self.Button1.configure(takefocus="0")
            self.Button1.configure(text='''Browse''')

            self.Label1 = tk.Label(top)
            self.Label1.place(relx=0.299, rely=0.367, height=21, width=101)
            self.Label1.configure(activebackground="#f9f9f9")
            self.Label1.configure(activeforeground="black")
            self.Label1.configure(background="#ffffff")
            self.Label1.configure(disabledforeground="#a3a3a3")
            self.Label1.configure(foreground="#000000")
            self.Label1.configure(highlightbackground="#d9d9d9")
            self.Label1.configure(highlightcolor="black")
            self.Label1.configure(text='''Choose Folder''')

            self.Create = tk.Button(top,command = Toplevel1.start_generate_model)
            self.Create.place(relx=0.543, rely=0.733, height=44, width=127)
            self.Create.configure(activebackground="#ececec")
            self.Create.configure(activeforeground="#000000")
            self.Create.configure(background="#fff5fe")
            self.Create.configure(borderwidth=".5")
            self.Create.configure(disabledforeground="#a3a3a3")
            self.Create.configure(font="-family {Segoe UI} -size 12")
            self.Create.configure(foreground="#000000")
            self.Create.configure(highlightbackground="#d9d9d9")
            self.Create.configure(highlightcolor="black")
            self.Create.configure(pady="0")
            self.Create.configure(takefocus="0")
            self.Create.configure(text='''Create''')
            self.Label1_9 = tk.Label(top)
            self.Label1_9.place(relx=0.299, rely=0.256, height=21, width=101)
            self.Label1_9.configure(activebackground="#f9f9f9")
            self.Label1_9.configure(activeforeground="black")
            self.Label1_9.configure(background="#ffffff")
            self.Label1_9.configure(disabledforeground="#a3a3a3")
            self.Label1_9.configure(foreground="#000000")
            self.Label1_9.configure(highlightbackground="#d9d9d9")
            self.Label1_9.configure(highlightcolor="black")
            self.Label1_9.configure(text='''Model Name''')

            self.Entry1 = tk.Entry(top)
            self.Entry1.place(relx=0.461, rely=0.267, height=20, relwidth=0.358)
            self.Entry1.configure(background="white")
            self.Entry1.configure(disabledforeground="#a3a3a3")
            self.Entry1.configure(font="TkFixedFont")
            self.Entry1.configure(foreground="#000000")
            self.Entry1.configure(insertbackground="black")
            self.Entry1.configure(takefocus="0")
            self.Entry1.configure(width=264)


            self.Entry1_10 = tk.Entry(top)
            self.Entry1_10.place(relx=0.461, rely=0.367, height=20, relwidth=0.358)
            self.Entry1_10.configure(background="white")
            self.Entry1_10.configure(disabledforeground="#a3a3a3")
            self.Entry1_10.configure(font="TkFixedFont")
            self.Entry1_10.configure(foreground="#000000")
            self.Entry1_10.configure(highlightbackground="#d9d9d9")
            self.Entry1_10.configure(highlightcolor="black")
            self.Entry1_10.configure(insertbackground="black")
            self.Entry1_10.configure(selectbackground="#c4c4c4")
            self.Entry1_10.configure(selectforeground="black")
            self.Entry1_10.configure(takefocus="0")

            self.TSeparator1 = ttk.Separator(top)
            self.TSeparator1.place(relx=0.237, rely=0.0, relheight=1.0)
            self.TSeparator1.configure(orient="vertical")
            self.TSeparator1.configure(takefocus="0")
            self.HomeBtn = ttk.Button(top, command=Move_Between_Formms.Go_To_Home_Form)
            self.HomeBtn.place(relx=0.0, rely=0.044, height=85, width=176)
            self.HomeBtn.configure(takefocus="")
            self.HomeBtn.configure(text='''Home''')
            self.HomeBtn.configure(width=176)

            self.Statisticsbtn = ttk.Button(top, command=Move_Between_Formms.Go_To_Statistics_Form)
            self.Statisticsbtn.place(relx=0.0, rely=0.233, height=85, width=176)
            self.Statisticsbtn.configure(takefocus="")
            self.Statisticsbtn.configure(text='''Statistics''')

            self.Monitiringbtn = ttk.Button(top, command=Move_Between_Formms.Go_To_Monitiring_Form)
            self.Monitiringbtn.place(relx=0.0, rely=0.422, height=85, width=176)
            self.Monitiringbtn.configure(takefocus="")
            self.Monitiringbtn.configure(text='''Monitiring''')

            self.Model_Btn = ttk.Button(top, command=Move_Between_Formms.Go_To_CreateModel_Form)
            self.Model_Btn.place(relx=0.0, rely=0.611, height=85, width=176)
            self.Model_Btn.configure(takefocus="")
            self.Model_Btn.configure(text='''Create Model''')

            self.Helpbtn = ttk.Button(top, command=Move_Between_Formms.Go_To_Help_Form)
            self.Helpbtn.place(relx=0.0, rely=0.811, height=85, width=176)
            self.Helpbtn.configure(takefocus="")
            self.Helpbtn.configure(text='''Help''')
            Toplevel1.formLevel = top
        elif Number == 6:
            _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
            _fgcolor = '#000000'  # X11 color: 'black'
            _compcolor = '#d9d9d9'  # X11 color: 'gray85'
            _ana1color = '#d9d9d9'  # X11 color: 'gray85'
            _ana2color = '#ececec'  # Closest X11 color: 'gray92'
            self.style = ttk.Style()
            if sys.platform == "win32":
                self.style.theme_use('winnative')
            self.style.configure('.', background=_bgcolor)
            self.style.configure('.', foreground=_fgcolor)
            self.style.configure('.', font="TkDefaultFont")
            self.style.map('.', background=
            [('selected', _compcolor), ('active', _ana2color)])

            top.geometry("737x450+269+167")
            top.title("Report")
            top.configure(background="#ffffff")
            top.configure(highlightbackground="#f0f0f0f0f0f0")
            top.configure(highlightcolor="#646464646464")

            self.menubar = tk.Menu(top, font="TkMenuFont", bg='#ffffff', fg='#ffffff')
            top.configure(menu=self.menubar)

            self.HomeBtn = ttk.Button(top, command=Move_Between_Formms.Go_To_Home_Form)
            self.HomeBtn.place(relx=0.0, rely=0.044, height=85, width=176)
            self.HomeBtn.configure(takefocus="")
            self.HomeBtn.configure(text='''Home''')
            self.HomeBtn.configure(width=176)

            self.Statisticsbtn = ttk.Button(top, command=Move_Between_Formms.Go_To_Statistics_Form)
            self.Statisticsbtn.place(relx=0.0, rely=0.233, height=85, width=176)
            self.Statisticsbtn.configure(takefocus="")
            self.Statisticsbtn.configure(text='''Statistics''')

            self.Monitiringbtn = ttk.Button(top, command=Move_Between_Formms.Go_To_Monitiring_Form)
            self.Monitiringbtn.place(relx=0.0, rely=0.422, height=85, width=176)
            self.Monitiringbtn.configure(takefocus="")
            self.Monitiringbtn.configure(text='''Monitiring''')

            self.Model_Btn = ttk.Button(top, command=Move_Between_Formms.Go_To_CreateModel_Form)
            self.Model_Btn.place(relx=0.0, rely=0.611, height=85, width=176)
            self.Model_Btn.configure(takefocus="")
            self.Model_Btn.configure(text='''Create Model''')

            self.Helpbtn = ttk.Button(top, command=Move_Between_Formms.Go_To_Help_Form)
            self.Helpbtn.place(relx=0.0, rely=0.811, height=85, width=176)
            self.Helpbtn.configure(takefocus="")
            self.Helpbtn.configure(text='''Help''')
            Toplevel1.formLevel = top

            labelfont = ('times', 19, 'bold')
            self.Label1 = tk.Label(top)
            self.Label1.place(relx=0.4, rely=0.05, height=30, width=300)
            self.Label1.configure(background="#ffffff")
            self.Label1.configure(disabledforeground="#a3a3a3")
            self.Label1.configure(foreground="red")
            self.Label1.configure(font=labelfont)
            self.Label1.configure(text=top1.Dis+' Disease')

            self.Label2 = tk.Label(top)
            self.Label2.place(relx=0.25, rely=0.13, height=21, width=120)
            self.Label2.configure(background="#ffffff")
            self.Label2.configure(disabledforeground="#a3a3a3")
            self.Label2.configure(foreground="black")
            self.Label2.configure(font=('times', 15, 'bold'))
            self.Label2.configure(text='''Description''')

            self.Label2 = tk.Label(top)
            self.Label2.place(relx=0.25, rely=0.45, height=21, width=120)
            self.Label2.configure(background="#ffffff")
            self.Label2.configure(disabledforeground="#a3a3a3")
            self.Label2.configure(foreground="black")
            self.Label2.configure(font=('times', 15, 'bold'))
            self.Label2.configure(text='''Treatment''')

            self.Label3 = tk.Label(top)
            self.Label3.place(relx=0.25, rely=0.2, height=109, width=450)
            self.Label3.configure(background="#ffffff")
            self.Label3.configure(disabledforeground="#a3a3a3")
            self.Label3.configure(foreground="black")
            self.Label3.configure(font=('times', 10))
            self.Label3.configure(text=top1.Desc)

            self.Label3 = tk.Label(top)
            self.Label3.place(relx=0.25, rely=0.52, height=200, width=450)
            self.Label3.configure(background="#ffffff")
            self.Label3.configure(disabledforeground="#a3a3a3")
            self.Label3.configure(foreground="black")
            self.Label3.configure(font=('times', 10))
            self.Label3.configure(text=top1.Tre)
        elif Number == 2:
            _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
            _fgcolor = '#000000'  # X11 color: 'black'
            _compcolor = '#d9d9d9'  # X11 color: 'gray85'
            _ana1color = '#d9d9d9'  # X11 color: 'gray85'
            _ana2color = '#ececec'  # Closest X11 color: 'gray92'
            self.style = ttk.Style()
            if sys.platform == "win32":
                self.style.theme_use('winnative')
            self.style.configure('.', background=_bgcolor)
            self.style.configure('.', foreground=_fgcolor)
            self.style.configure('.', font="TkDefaultFont")
            self.style.map('.', background=
            [('selected', _compcolor), ('active', _ana2color)])

            top.geometry("737x450+269+167")
            top.title("Monitiring")
            top.configure(background="#ffffff")
            top.configure(highlightbackground="#f0f0f0f0f0f0")
            top.configure(highlightcolor="#646464646464")

            self.menubar = tk.Menu(top, font="TkMenuFont", bg='#ffffff', fg='#ffffff')
            top.configure(menu=self.menubar)

            self.HomeBtn = ttk.Button(top, command=Move_Between_Formms.Go_To_Home_Form)
            self.HomeBtn.place(relx=0.0, rely=0.044, height=85, width=176)
            self.HomeBtn.configure(takefocus="")
            self.HomeBtn.configure(text='''Home''')
            self.HomeBtn.configure(width=176)

            self.Statisticsbtn = ttk.Button(top, command=Move_Between_Formms.Go_To_Statistics_Form)
            self.Statisticsbtn.place(relx=0.0, rely=0.233, height=85, width=176)
            self.Statisticsbtn.configure(takefocus="")
            self.Statisticsbtn.configure(text='''Statistics''')

            self.Monitiringbtn = ttk.Button(top, command=Move_Between_Formms.Go_To_Monitiring_Form)
            self.Monitiringbtn.place(relx=0.0, rely=0.422, height=85, width=176)
            self.Monitiringbtn.configure(takefocus="")
            self.Monitiringbtn.configure(text='''Monitiring''')

            self.Model_Btn = ttk.Button(top, command=Move_Between_Formms.Go_To_CreateModel_Form)
            self.Model_Btn.place(relx=0.0, rely=0.611, height=85, width=176)
            self.Model_Btn.configure(takefocus="")
            self.Model_Btn.configure(text='''Create Model''')

            self.Helpbtn = ttk.Button(top, command=Move_Between_Formms.Go_To_Help_Form)
            self.Helpbtn.place(relx=0.0, rely=0.811, height=85, width=176)
            self.Helpbtn.configure(takefocus="")
            self.Helpbtn.configure(text='''Help''')
            Toplevel1.formLevel = top

            self.CreateTrackbtn = tk.Button(top,command=Move_Between_Formms.Go_TO_CreateNewTrack)
            self.CreateTrackbtn.place(relx=0.76, rely=0.689, height=44, width=127)
            self.CreateTrackbtn.configure(activebackground="#ececec")
            self.CreateTrackbtn.configure(activeforeground="#000000")
            self.CreateTrackbtn.configure(background="#fff5fe")
            self.CreateTrackbtn.configure(borderwidth=".5")
            self.CreateTrackbtn.configure(disabledforeground="#a3a3a3")
            self.CreateTrackbtn.configure(font="-family {Segoe UI} -size 12")
            self.CreateTrackbtn.configure(foreground="#000000")
            self.CreateTrackbtn.configure(highlightbackground="#d9d9d9")
            self.CreateTrackbtn.configure(highlightcolor="black")
            self.CreateTrackbtn.configure(pady="0")
            self.CreateTrackbtn.configure(takefocus="0")
            self.CreateTrackbtn.configure(text='''Create''')
            self.UpdateTrack_btn = tk.Button(top , command = Move_Between_Formms.Go_TO_Update_In_Track)
            self.UpdateTrack_btn.place(relx=0.353, rely=0.689, height=44, width=127)
            self.UpdateTrack_btn.configure(activebackground="#ececec")
            self.UpdateTrack_btn.configure(activeforeground="#000000")
            self.UpdateTrack_btn.configure(background="#fff5fe")
            self.UpdateTrack_btn.configure(borderwidth=".5")
            self.UpdateTrack_btn.configure(disabledforeground="#a3a3a3")
            self.UpdateTrack_btn.configure(font="-family {Segoe UI} -size 12")
            self.UpdateTrack_btn.configure(foreground="#000000")
            self.UpdateTrack_btn.configure(highlightbackground="#d9d9d9")
            self.UpdateTrack_btn.configure(highlightcolor="black")
            self.UpdateTrack_btn.configure(pady="0")
            self.UpdateTrack_btn.configure(takefocus="0")
            self.UpdateTrack_btn.configure(text='''Update''')
            self.Label1 = tk.Label(top)
            self.Label1.place(relx=0.353, rely=0.289, height=61, width=406)
            self.Label1.configure(background="#fcf2f7")
            self.Label1.configure(disabledforeground="#a3a3a3")
            self.Label1.configure(font="-family {Segoe UI} -size 14 -weight bold -slant italic")
            self.Label1.configure(foreground="#000000")
            self.Label1.configure(text='''Create new track or add in existing track''')
            self.Label1.configure(width=406)
        elif Number == 1:
            _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
            _fgcolor = '#000000'  # X11 color: 'black'
            _compcolor = '#d9d9d9'  # X11 color: 'gray85'
            _ana1color = '#d9d9d9'  # X11 color: 'gray85'
            _ana2color = '#ececec'  # Closest X11 color: 'gray92'
            self.style = ttk.Style()
            if sys.platform == "win32":
                self.style.theme_use('winnative')
            self.style.configure('.', background=_bgcolor)
            self.style.configure('.', foreground=_fgcolor)
            self.style.configure('.', font="TkDefaultFont")
            self.style.map('.', background=
            [('selected', _compcolor), ('active', _ana2color)])

            top.geometry("737x450+269+167")
            top.title("Monitiring")
            top.configure(background="#ffffff")
            top.configure(highlightbackground="#f0f0f0f0f0f0")
            top.configure(highlightcolor="#646464646464")

            self.menubar = tk.Menu(top, font="TkMenuFont", bg='#ffffff', fg='#ffffff')
            top.configure(menu=self.menubar)

            self.HomeBtn = ttk.Button(top, command=Move_Between_Formms.Go_To_Home_Form)
            self.HomeBtn.place(relx=0.0, rely=0.044, height=85, width=176)
            self.HomeBtn.configure(takefocus="")
            self.HomeBtn.configure(text='''Home''')
            self.HomeBtn.configure(width=176)

            self.Statisticsbtn = ttk.Button(top, command=Move_Between_Formms.Go_To_Statistics_Form)
            self.Statisticsbtn.place(relx=0.0, rely=0.233, height=85, width=176)
            self.Statisticsbtn.configure(takefocus="")
            self.Statisticsbtn.configure(text='''Statistics''')
            self.Model_Btn = ttk.Button(top, command=Move_Between_Formms.Go_To_CreateModel_Form)
            self.Model_Btn.place(relx=0.0, rely=0.611, height=85, width=176)
            self.Model_Btn.configure(takefocus="")
            self.Model_Btn.configure(text='''Create Model''')

            self.Helpbtn = ttk.Button(top, command=Move_Between_Formms.Go_To_Help_Form)
            self.Helpbtn.place(relx=0.0, rely=0.811, height=85, width=176)
            self.Helpbtn.configure(takefocus="")
            self.Helpbtn.configure(text='''Help''')
            Toplevel1.formLevel = top

            self.Monitiringbtn = ttk.Button(top, command=Move_Between_Formms.Go_To_Monitiring_Form)
            self.Monitiringbtn.place(relx=0.0, rely=0.422, height=85, width=176)
            self.Monitiringbtn.configure(takefocus="")
            self.Monitiringbtn.configure(text='''Monitiring''')

            self.TCombobox1 = ttk.Combobox(top,values = Toplevel1.Fill_ComboBox(0))
            self.TCombobox1.place(relx=0.475, rely=0.244, relheight=0.047
                                  , relwidth=0.384)
            self.TCombobox1.configure(width=283)
            self.TCombobox1.configure(takefocus="")

            self.Label1 = tk.Label(top)
            self.Label1.place(relx=0.326, rely=0.244, height=21, width=84)
            self.Label1.configure(background="#f4f4f4")
            self.Label1.configure(disabledforeground="#a3a3a3")
            self.Label1.configure(foreground="#000000")
            self.Label1.configure(text='''Select Track ID''')
            self.Label1.configure(width=84)

            self.Button1 = tk.Button(top ,command = Toplevel1.Create_Graph)
            self.Button1.place(relx=0.543, rely=0.689, height=54, width=177)
            self.Button1.configure(activebackground="#ececec")
            self.Button1.configure(activeforeground="#000000")
            self.Button1.configure(background="#d9d9d9")
            self.Button1.configure(disabledforeground="#a3a3a3")
            self.Button1.configure(foreground="#000000")
            self.Button1.configure(highlightbackground="#d9d9d9")
            self.Button1.configure(highlightcolor="black")
            self.Button1.configure(pady="0")
            self.Button1.configure(text='''Show Result''')
            self.Button1.configure(width=177)
        elif Number == 5:
            '''Create New Track'''
            _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
            _fgcolor = '#000000'  # X11 color: 'black'
            _compcolor = '#d9d9d9'  # X11 color: 'gray85'
            _ana1color = '#d9d9d9'  # X11 color: 'gray85'
            _ana2color = '#ececec'  # Closest X11 color: 'gray92'
            self.style = ttk.Style()
            if sys.platform == "win32":
                self.style.theme_use('winnative')
            self.style.configure('.', background=_bgcolor)
            self.style.configure('.', foreground=_fgcolor)
            self.style.configure('.', font="TkDefaultFont")
            self.style.map('.', background=
            [('selected', _compcolor), ('active', _ana2color)])

            top.geometry("737x450+269+167")
            top.title("Monitiring")
            top.configure(background="#ffffff")
            top.configure(highlightbackground="#f0f0f0f0f0f0")
            top.configure(highlightcolor="#646464646464")

            self.menubar = tk.Menu(top, font="TkMenuFont", bg='#ffffff', fg='#ffffff')
            top.configure(menu=self.menubar)

            self.HomeBtn = ttk.Button(top, command=Move_Between_Formms.Go_To_Home_Form)
            self.HomeBtn.place(relx=0.0, rely=0.044, height=85, width=176)
            self.HomeBtn.configure(takefocus="")
            self.HomeBtn.configure(text='''Home''')
            self.HomeBtn.configure(width=176)

            self.Statisticsbtn = ttk.Button(top, command=Move_Between_Formms.Go_To_Statistics_Form)
            self.Statisticsbtn.place(relx=0.0, rely=0.233, height=85, width=176)
            self.Statisticsbtn.configure(takefocus="")
            self.Statisticsbtn.configure(text='''Statistics''')

            self.Monitiringbtn = ttk.Button(top, command=Move_Between_Formms.Go_To_Monitiring_Form)
            self.Monitiringbtn.place(relx=0.0, rely=0.422, height=85, width=176)
            self.Monitiringbtn.configure(takefocus="")
            self.Monitiringbtn.configure(text='''Monitiring''')

            self.Model_Btn = ttk.Button(top, command=Move_Between_Formms.Go_To_CreateModel_Form)
            self.Model_Btn.place(relx=0.0, rely=0.611, height=85, width=176)
            self.Model_Btn.configure(takefocus="")
            self.Model_Btn.configure(text='''Create Model''')

            self.Helpbtn = ttk.Button(top, command=Move_Between_Formms.Go_To_Help_Form)
            self.Helpbtn.place(relx=0.0, rely=0.811, height=85, width=176)
            self.Helpbtn.configure(takefocus="")
            self.Helpbtn.configure(text='''Help''')
            Toplevel1.formLevel = top

            self.Label1 = tk.Label(top)
            self.Label1.place(relx=0.326, rely=0.244, height=21, width=84)
            self.Label1.configure(background="#f4f4f4")
            self.Label1.configure(disabledforeground="#a3a3a3")
            self.Label1.configure(foreground="#000000")
            self.Label1.configure(text='''Enter Track ID''')
            self.Label1.configure(width=84)

            self.Create_Track_ = tk.Button(top ,command = Toplevel1.Create_Track)
            self.Create_Track_.place(relx=0.733, rely=0.778, height=54, width=127)
            self.Create_Track_.configure(activebackground="#ececec")
            self.Create_Track_.configure(activeforeground="#000000")
            self.Create_Track_.configure(background="#d9d9d9")
            self.Create_Track_.configure(disabledforeground="#a3a3a3")
            self.Create_Track_.configure(foreground="#000000")
            self.Create_Track_.configure(highlightbackground="#d9d9d9")
            self.Create_Track_.configure(highlightcolor="black")
            self.Create_Track_.configure(pady="0")
            self.Create_Track_.configure(text='''Save''')
            self.Create_Track_.configure(width=127)

            self.Entry1 = tk.Entry(top)
            self.Entry1.place(relx=0.475, rely=0.244, height=20, relwidth=0.399)
            self.Entry1.configure(background="white")
            self.Entry1.configure(disabledforeground="#a3a3a3")
            self.Entry1.configure(font="TkFixedFont")
            self.Entry1.configure(foreground="#000000")
            self.Entry1.configure(insertbackground="black")
            self.Entry1.configure(width=294)

            self.Label1_2 = tk.Label(top)
            self.Label1_2.place(relx=0.312, rely=0.344, height=21, width=94)
            self.Label1_2.configure(activebackground="#f9f9f9")
            self.Label1_2.configure(activeforeground="black")
            self.Label1_2.configure(background="#f4f4f4")
            self.Label1_2.configure(disabledforeground="#a3a3a3")
            self.Label1_2.configure(foreground="#000000")
            self.Label1_2.configure(highlightbackground="#d9d9d9")
            self.Label1_2.configure(highlightcolor="black")
            self.Label1_2.configure(text='''Select Plant Type''')
            self.Label1_2.configure(width=94)

            self.TCombobox1 = ttk.Combobox(top, values = Toplevel1.Fill_ComboBox(1))
            self.TCombobox1.place(relx=0.475, rely=0.344, relheight=0.047
                                  , relwidth=0.398)
            self.TCombobox1.configure(width=293)
            self.TCombobox1.configure(takefocus="")
        elif Number == 7:
            '''Update in Track'''
            Toplevel1.flag = 1
            _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
            _fgcolor = '#000000'  # X11 color: 'black'
            _compcolor = '#d9d9d9'  # X11 color: 'gray85'
            _ana1color = '#d9d9d9'  # X11 color: 'gray85'
            _ana2color = '#ececec'  # Closest X11 color: 'gray92'
            self.style = ttk.Style()
            if sys.platform == "win32":
                self.style.theme_use('winnative')
            self.style.configure('.', background=_bgcolor)
            self.style.configure('.', foreground=_fgcolor)
            self.style.configure('.', font="TkDefaultFont")
            self.style.map('.', background=
            [('selected', _compcolor), ('active', _ana2color)])

            top.geometry("737x450+269+167")
            top.title("Monitiring")
            top.configure(background="#ffffff")
            top.configure(highlightbackground="#f0f0f0f0f0f0")
            top.configure(highlightcolor="#646464646464")

            self.menubar = tk.Menu(top, font="TkMenuFont", bg='#ffffff', fg='#ffffff')
            top.configure(menu=self.menubar)

            self.HomeBtn = ttk.Button(top, command=Move_Between_Formms.Go_To_Home_Form)
            self.HomeBtn.place(relx=0.0, rely=0.044, height=85, width=176)
            self.HomeBtn.configure(takefocus="")
            self.HomeBtn.configure(text='''Home''')
            self.HomeBtn.configure(width=176)

            self.Statisticsbtn = ttk.Button(top, command=Move_Between_Formms.Go_To_Statistics_Form)
            self.Statisticsbtn.place(relx=0.0, rely=0.233, height=85, width=176)
            self.Statisticsbtn.configure(takefocus="")
            self.Statisticsbtn.configure(text='''Statistics''')

            self.Monitiringbtn = ttk.Button(top, command=Move_Between_Formms.Go_To_Monitiring_Form)
            self.Monitiringbtn.place(relx=0.0, rely=0.422, height=85, width=176)
            self.Monitiringbtn.configure(takefocus="")
            self.Monitiringbtn.configure(text='''Monitiring''')

            self.Model_Btn = ttk.Button(top, command=Move_Between_Formms.Go_To_CreateModel_Form)
            self.Model_Btn.place(relx=0.0, rely=0.611, height=85, width=176)
            self.Model_Btn.configure(takefocus="")
            self.Model_Btn.configure(text='''Create Model''')

            self.Helpbtn = ttk.Button(top, command=Move_Between_Formms.Go_To_Help_Form)
            self.Helpbtn.place(relx=0.0, rely=0.811, height=85, width=176)
            self.Helpbtn.configure(takefocus="")
            self.Helpbtn.configure(text='''Help''')
            #Toplevel1.formLevel = top

            self.Label1 = tk.Label(top)
            self.Label1.place(relx=0.326, rely=0.244, height=21, width=100)
            self.Label1.configure(background="#f4f4f4")
            self.Label1.configure(disabledforeground="#a3a3a3")
            self.Label1.configure(foreground="#000000")
            self.Label1.configure(text='''Select Folder Path''')
            self.Label1.configure(width=84)

            self.Create_Track_ = tk.Button(top ,command = Toplevel1.Update_Track)
            self.Create_Track_.place(relx=0.733, rely=0.778, height=54, width=127)
            self.Create_Track_.configure(activebackground="#ececec")
            self.Create_Track_.configure(activeforeground="#000000")
            self.Create_Track_.configure(background="#d9d9d9")
            self.Create_Track_.configure(disabledforeground="#a3a3a3")
            self.Create_Track_.configure(foreground="#000000")
            self.Create_Track_.configure(highlightbackground="#d9d9d9")
            self.Create_Track_.configure(highlightcolor="black")
            self.Create_Track_.configure(pady="0")
            self.Create_Track_.configure(text='''Save''')
            self.Create_Track_.configure(width=127)

            self.Entry1 = tk.Entry(top)
            self.Entry1.place(relx=0.475, rely=0.244, height=20, relwidth=0.399)
            self.Entry1.configure(background="white")
            self.Entry1.configure(disabledforeground="#a3a3a3")
            self.Entry1.configure(font="TkFixedFont")
            self.Entry1.configure(foreground="#000000")
            self.Entry1.configure(insertbackground="black")
            self.Entry1.configure(width=294)

            self.Label1_2 = tk.Label(top)
            self.Label1_2.place(relx=0.312, rely=0.344, height=21, width=94)
            self.Label1_2.configure(activebackground="#f9f9f9")
            self.Label1_2.configure(activeforeground="black")
            self.Label1_2.configure(background="#f4f4f4")
            self.Label1_2.configure(disabledforeground="#a3a3a3")
            self.Label1_2.configure(foreground="#000000")
            self.Label1_2.configure(highlightbackground="#d9d9d9")
            self.Label1_2.configure(highlightcolor="black")
            self.Label1_2.configure(text='''Select Track ID''')
            self.Label1_2.configure(width=94)

            self.TCombobox1 = ttk.Combobox(top, values = Toplevel1.Fill_ComboBox(0))
            self.TCombobox1.place(relx=0.475, rely=0.344, relheight=0.047
                                  , relwidth=0.398)
            self.TCombobox1.configure(width=293)
            self.TCombobox1.configure(takefocus="")

            self.Button1 = tk.Button(top)
            #relx = 0.475, rely = 0.244, height = 20, relwidth = 0.399
            self.Button1.place(relx=0.896, rely=0.244, height=24, width=47)
            self.Button1.configure(activebackground="#ececec")
            self.Button1.configure(activeforeground="#000000")
            self.Button1.configure(background="#d9d9d9")
            self.Button1.configure(command=Home_Form_Setting.creat_browse_button)
            self.Button1.configure(disabledforeground="#a3a3a3")
            self.Button1.configure(foreground="#000000")
            self.Button1.configure(highlightbackground="#d9d9d9")
            self.Button1.configure(highlightcolor="black")
            self.Button1.configure(pady="0")
            self.Button1.configure(text='''...''')
            self.Button1.configure(width=107)

            Toplevel1.formLevel = top

    def start_generate_model():

        str1 = top1.Entry1.get()
        str2 = top1.Entry1_10.get()
        call_back_end.Create_Model(str2,str1)


        #print(str1)
    def update_Entry(self, Text, level_Entry):
        print(level_Entry)
        if (level_Entry == 3):
            self.Entry1_10.delete(0, END)
            self.Entry1_10.insert(0, Text)
        elif (level_Entry == 0):
            self.Text1.delete(0, END)
            print('text ', Text)
            self.Text1.insert(0, Text)
        elif (level_Entry == 7):
            self.Entry1.delete(0, END)
            print('text ', Text)
            self.Entry1.insert(0, Text)
    def start_Test():
        str1 = top1.Text1.get()
        Data=call_back_end.Test_Model(str1, 'Apple', 'Apple',top1.flag)
        top1.Dis=Data[0]
        top1.Desc=Data[1]
        top1.Tre=Data[2]
        Move_Between_Formms.Go_TO_Dec()
    def Fill_ComboBox(Flag_Num):
        if Flag_Num == 0:
            Values = cnn.Tracking.Make_Combobox()
            return Values
        elif Flag_Num == 1:
            FileName = 'Modeles Name/Names.txt'
            file = open(FileName, "r+")
            x = file.read()
            x = x.split('\n')
            IDList = []
            for i in range(0, len(x)):
                IDList.append(x[i])
            print(IDList)
            return IDList
    def Update_Track():
        str1 = top1.Entry1.get()
        str2 = top1.TCombobox1.get()
        print(str2)
        call_back_end.Update_In_Track(str1, str2)
    def Create_Track():
        str1 = top1.Entry1.get()
        str2 = top1.TCombobox1.get()
        print(str1)
        print(str2)
        call_back_end.CreateNewTrack(str1, str2)

    def Create_Graph():
        str2 = top1.TCombobox1.get()
        print(str2)
        call_back_end.ShowGraph(str2)


class Move_Between_Formms:
    def Go_To_Home_Form():
        Toplevel1.formLevel.destroy()
        vp_start_gui(0)

    def Go_To_Statistics_Form():
        Toplevel1.formLevel.destroy()
        vp_start_gui(1)

    def Go_To_Monitiring_Form():
        Toplevel1.formLevel.destroy()
        vp_start_gui(2)

    def Go_To_CreateModel_Form():
        Toplevel1.formLevel.destroy()
        vp_start_gui(3)

    def Go_To_Help_Form():
        Toplevel1.formLevel.destroy()
        vp_start_gui(4)
    def Go_TO_Dec():
        '''this function is use to go to description for in home button '''
        Toplevel1.formLevel.destroy()
        vp_start_gui(6)
    def Go_TO_CreateNewTrack():
        '''this function is use to go to Create New Track '''
        Toplevel1.formLevel.destroy()
        vp_start_gui(5)
    def Go_TO_Update_In_Track():
        '''this function is use to go to Update in Track '''
        Toplevel1.formLevel.destroy()
        vp_start_gui(7)

if __name__ == '__main__':
    vp_start_gui(0)
