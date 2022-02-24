
from tkinter import *
from PIL import Image, ImageTk
import numpy as np
import ytb_check_combine as dl
import cv2

class GUI():
    def __init__(self,window):
        self.window = window
        #title
        self.window.title("Check_Product")
        self.window.geometry('1020x600+0+130')
        self.window["bg"] = "DimGray"

    def create_widgets(self):
        
        def Start_check():
            exit()
        
        #title
        self.lb_yn_lid = Label(self.window,text=' Lid: ',fg='WhiteSmoke',bg="DimGray",font=('Arial', 13))
        self.lb_ag_lb = Label(self.window,text=' Angle: ',fg='WhiteSmoke',bg="DimGray",font=('Arial', 13))
        self.lb_sp_lb = Label(self.window,text=' Shape: ',fg='WhiteSmoke',bg="DimGray",font=('Arial', 13))
        self.lb_cl_lb = Label(self.window,text=' Color: ',fg='WhiteSmoke',bg="DimGray",font=('Arial', 13))
        self.title = Label(self.window,text=" CHECKING PRODUCT ",fg='DarkRed',bg="DarkTurquoise",height=2,width=32,font=('Arial', 13))
        self.lb_total = Label(self.window,text=' Total: ',fg='WhiteSmoke',bg="DimGray",font=('Arial', 13))
        self.lb_good = Label(self.window,text=' Succeed: ',fg='WhiteSmoke',bg="DimGray",font=('Arial', 13))
        self.lb_failed = Label(self.window,text=' Failed: ',fg='WhiteSmoke',bg="DimGray",font=('Arial', 13))
        
        #position title
        self.lb_yn_lid.place(x=520, y=180)
        self.lb_ag_lb.place(x=770, y=180)
        self.lb_sp_lb.place(x=520, y=420)
        self.lb_cl_lb.place(x=770, y=420)
        self.title.place(x=600,y=520)
        self.lb_total.place(x=220, y=420)
        self.lb_good.place(x=220, y=480)
        self.lb_failed.place(x=350, y=480)
        
        # image
        self.fr_img_oj= Canvas(self.window, width=470, height=400, bg="WhiteSmoke")
        self.fr_img_ld= Canvas(self.window, width=220, height=165, bg="WhiteSmoke")
        self.fr_img_sp= Canvas(self.window, width=220, height=165, bg="WhiteSmoke")
        self.fr_img_ag= Canvas(self.window, width=220, height=165, bg="WhiteSmoke")
        self.fr_img_cl= Canvas(self.window, width=220, height=165, bg="DimGray")
        
        #position image
        self.fr_img_oj.place(x=10, y=10)
        self.fr_img_ld.place(x=520, y=10)
        self.fr_img_sp.place(x=520, y=250)
        self.fr_img_ag.place(x=770, y=10)
        self.fr_img_cl.place(x=770, y=250)
        
        
        #button
        self.start_button = Button(self.window,text=' Quit ',font=('calibri', 15),height=1,
                                   width=8,highlightcolor='purple',fg='WhiteSmoke',
                                   bg="BurlyWood", command = Start_check,
                                   activeforeground='orange', activebackground='red')
        #position button
        self.start_button.place(x=30,y=530)
        

            
    def update_frame(self):
        self.yn_lid,self.shape_lb,self.angle_lb,self.color_lb,self.img_mj,self.img_ld,self.img_shp,self.img_ag,self.img_cl,self.result_check,self.total_pr,self.good_pr,self.failed_pr,self.rawC = dl.doc_lb() 
        
        #convert
        self.img_mj = cv2.cvtColor(self.img_mj, cv2.COLOR_BGR2RGB)
        self.img_ld = cv2.cvtColor(self.img_ld, cv2.COLOR_BGR2RGB)
        self.img_shp = cv2.cvtColor(self.img_shp, cv2.COLOR_BGR2RGB)
        self.img_ag = cv2.cvtColor(self.img_ag, cv2.COLOR_BGR2RGB)
        self.img_cl = cv2.cvtColor(self.img_cl, cv2.COLOR_BGR2RGB)
        
        #take image
        self.pt_mj = ImageTk.PhotoImage(image=Image.fromarray(self.img_mj))
        self.pt_ld = ImageTk.PhotoImage(image=Image.fromarray(self.img_ld))
        self.pt_sp = ImageTk.PhotoImage(image=Image.fromarray(self.img_shp))
        self.pt_ag = ImageTk.PhotoImage(image=Image.fromarray(self.img_ag))
        self.pt_cl = ImageTk.PhotoImage(image=Image.fromarray(self.img_cl))
        
        #create image
        self.fr_img_oj.create_image(0,25, image=self.pt_mj, anchor=NW)
        self.fr_img_ld.create_image(0,0, image=self.pt_ld, anchor=NW)
        self.fr_img_sp.create_image(0,0, image=self.pt_sp, anchor=NW)
        self.fr_img_ag.create_image(0,0, image=self.pt_ag, anchor=NW)
        self.fr_img_cl.create_image(95,65, image=self.pt_cl, anchor=NW)
        
        #parameter
        self.yn_lid = Label(self.window,text= self.yn_lid,fg='Black',bg="WhiteSmoke",height=1,width=15,font=('Arial', 12))
        self.ag_lb = Label(self.window,text= self.angle_lb,fg='Black',bg="WhiteSmoke",height=1,width=15,font=('Arial', 12))
        self.sp_lb = Label(self.window,text= self.shape_lb,fg='Black',bg="WhiteSmoke",height=1,width=15,font=('Arial', 12))
        self.cl_lb = Label(self.window,text= self.color_lb,fg='Black',bg="WhiteSmoke",height=1,width=15,font=('Arial', 12))
        self.tt_pr = Label(self.window,text= self.total_pr,fg='Black',bg="WhiteSmoke",height=1,width=15,font=('Arial', 16))
        self.gd_pr = Label(self.window,text= self.good_pr,fg='Black',bg="WhiteSmoke",height=1,width=7,font=('Arial', 16))
        self.fd_pr = Label(self.window,text= self.failed_pr,fg='Black',bg="WhiteSmoke",height=1,width=7,font=('Arial', 16))


        #position parameter
        self.yn_lid.place(x=600, y=180)
        self.ag_lb.place(x=850, y=180)
        self.sp_lb.place(x=600, y=420)
        self.cl_lb.place(x=850, y=420)
        self.tt_pr.place(x=280, y=450)
        self.gd_pr.place(x=260, y=520)
        self.fd_pr.place(x=400, y=520)

        # result
        self.rl_pd = Label(self.window,text= self.result_check,fg='Gold',bg="DimGray",font=('Arial', 24))
        self.rl_pd.place(x=710,y=470)
        self.window.after(340, self.update_frame)        
        

def gui_start():

    my_window = Tk()
    my_gui = GUI(my_window)
    my_gui.create_widgets()
    my_gui.update_frame()
    my_window.mainloop()

  
gui_start()
