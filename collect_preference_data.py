#!/usr/bin/env/python
from __future__ import print_function, division

import pandas as pd
import random
import pylab as pl
import seaborn as sns
import time, datetime
import tkinter as tk
import tkinter.messagebox as mb
import numpy as np


if __name__ == "__main__":
    
    dateArray = datetime.datetime.utcfromtimestamp(time.time())
    start_time_str = dateArray.strftime("%Y--%m--%d %H:%M:%S")
    
    #receive message from subject
    subject_id = input("Please input your id: ")
    #subject_id = int(subject_id)

    data_path = "used_data/processed_clean_Science-DREAM-12868_2016_287_MOESM1_ESM.xlsx"
    sheetname = 0
    
    #target = 'intensity' #'intensity' 'pleasantness' 'familiarity'
    
    same_dilution = None #None 'low' 'high'
    
    data = pd.read_excel(data_path,sheet_name=sheetname,header=0)
    
    unique_cid_list = list(set([cid for cid in data['cid']]))
    
    result_dict = {'subject_id':[],'trial_data':[],'smi':[],'cid':[],'dilution':[],'intensity':[],'pleasantness':[],'familiarity':[],'preference_intensity':[],'preference_pleasantness':[],'preference_familiarity':[]}
    
    count = 0
    while True:
        mols_cids = random.sample(unique_cid_list, 2)
        
        dateArray = datetime.datetime.utcfromtimestamp(time.time())
        time_str = dateArray.strftime("%Y--%m--%d %H:%M:%S")
        
        compare_data = {'cid':[],'x':[],'y':[]}
        key_list = ["EDIBLE","BAKERY","SWEET","FRUIT","FISH","GARLIC","SPICES","COLD","SOUR","BURNT","ACID","WARM","MUSKY","SWEATY","AMMONIA/URINOUS","DECAYED","WOOD","GRASS","FLOWER","CHEMICAL"]
        #{"EDIBLE":[],"BAKERY":[],"SWEET":[],"FRUIT":[],"FISH":[],"GARLIC":[],"SPICES":[],"COLD":[],"SOUR":[],"BURNT":[],"ACID":[],"WARM":[],"MUSKY":[],"SWEATY":[],"AMMONIA/URINOUS":[],"DECAYED":[],"WOOD":[],"GRASS":[],"FLOWER":[],"CHEMICAL":[]}
        
        smell_list=[]
        
        for mol_cid in mols_cids:
            #process a molecule
            data_temp = data[data['cid']==mol_cid]
            smi = data_temp.iloc[0].at['smi']
            unique_dilution_list = list(set([dilution for dilution in data_temp['dilution']]))
            if same_dilution is None:
                dilution = random.sample(unique_dilution_list, 1)[0]
            elif same_dilution == 'low':
                if len(unique_dilution_list[0]) > len(unique_dilution_list[1]):
                    dilution = unique_dilution_list[0]
                else:
                    dilution = unique_dilution_list[1]
            elif same_dilution == 'high':
                if len(unique_dilution_list[0]) < len(unique_dilution_list[1]):
                    dilution = unique_dilution_list[0]
                else:
                    dilution = unique_dilution_list[1]
            else:
                print("unknow same_dilution %s"%same_dilution)
                exit(1)

            data_temp_temp = data_temp[data_temp['dilution']==dilution]
            #print(data_temp_temp)
            
            result_dict['subject_id'].append(subject_id)
            result_dict['trial_data'].append(time_str)
            result_dict['smi'].append(smi)
            result_dict['cid'].append(mol_cid)
            result_dict['dilution'].append(dilution)
            result_dict['intensity'].append(data_temp_temp.iloc[0].at['intensity'])
            result_dict['pleasantness'].append(data_temp_temp.iloc[0].at['pleasantness'])
            result_dict['familiarity'].append(data_temp_temp.iloc[0].at['familiarity'])
            result_dict['preference_intensity'].append(0)
            result_dict['preference_pleasantness'].append(0)
            result_dict['preference_familiarity'].append(0)
            
            temp_dict={}
            for key in key_list:
                compare_data['cid'].append(mol_cid)
                compare_data['x'].append(key)
                value = data_temp_temp.iloc[0].at[key]
                compare_data['y'].append(value)
                if np.isnan(value):
                    temp_dict[key]=0.
                else:
                    temp_dict[key]=value
            sorted_temp_dict = sorted(temp_dict.items(), key=lambda temp_dict:temp_dict[1],reverse=True)
            
            smell_list_one = []
            smell_list_one.append(mol_cid)
            for key, value in sorted_temp_dict[0:4]:
                if value > 0.:
                    smell_list_one.append(key)
                else:
                    break
            smell_list.append(smell_list_one)
        
        #print(smell_list)

        #--------------
        #show GUI
        #--------------
        window = tk.Tk()

        window.title('My Window')

        window.geometry('1200x800')
        
        #print(compare_data)
        fig = pl.figure(figsize=(3.5,3.5),dpi=80)
        sns.barplot(x='y',y='x',data=compare_data,hue="cid")
        #print(compare_data)
        #pl.show()
        pl.savefig("images/temp.png",bbox_inches='tight')
        #pl.close()

        #l = tk.Label(window, bg='#FFF8DC', width=20, text='look me')

        canvas = tk.Canvas(window, height=260, width=350)
    
        image_file = tk.PhotoImage(file='images/temp.png')
        image = canvas.create_image(178, 0, anchor='n',image=image_file)

        canvas.grid(row=0, column=2)
        
        height, width = 200, 200

        if smell_list[0][0] <= smell_list[1][0]:
            color_1 = 'SteelBlue'
            color_2 = 'Orange'
        else:
            color_1 = 'Orange'
            color_2 = 'SteelBlue'

        tk.Label(window, text=smell_list[0], bg=color_1, width=20, height=7, wraplength=80,
                 justify='left').grid(row=0, column=1)
        tk.Label(window, text=smell_list[1], bg=color_2, width=20, height=7, wraplength=80,
                 justify='left').grid(row=0, column=3)

        #show help message
        def create():
            help = tk.Toplevel()
            help.title('Help message')
            
            canvas_help = tk.Canvas(help, bg="#FFF8DC",height=600, width=900,scrollregion=(0,0,520,520))
            frame = tk.Frame(canvas_help, background="#ffffff")
            vsb = tk.Scrollbar(help, orient="vertical", command=canvas_help.yview)
            canvas_help.configure(yscrollcommand=vsb.set)
            vsb.pack(side="right", fill="y")
            canvas_help.pack(side="left", fill="both", expand=True)
            canvas_help.create_window((4,4), window=frame, anchor="nw")

            def onFrameConfigure(canvas):
                '''Reset the scroll region to encompass the inner frame'''
                canvas.configure(scrollregion=canvas.bbox("all"))
            
            frame.bind("<Configure>", lambda event, canvas=canvas_help: onFrameConfigure(canvas_help))

            tk.Label(frame, text="Illustration of each area", bg="#87CEFA", width=100, height=2).pack()
            
            canvas_help_img = tk.Canvas(frame, bg="#DCDCDC",height=600, width=900)
            #image_file_help = ImageTk.PhotoImage(Image.open("images/resize_helpmessage.png"))  # PIL solution
            image_file_help = tk.PhotoImage(file='images/resize_helpmessage.png')
            canvas_help_img.create_image(450, 0, anchor='n',image=image_file_help)
            canvas_help_img.pack()
            
            tk.Label(frame, text="Specific interpretation of descriptors", bg="#87CEFA", width=100, height=2).pack()

            text_1 = tk.Text(frame,bg="#DCDCDC")
            text_1.insert("insert", "I love ")
            text_1.insert("insert", "\r\n")
            text_1.insert("insert", "a new line ")
            text_1["state"] = tk.DISABLED
            text_1.pack()
                     
            tk.Label(frame, text="Questions to be answered", bg="#87CEFA", width=100, height=2).pack()


            text_2 = tk.Text(frame,bg="#DCDCDC")
            text_2.insert("insert", "I love ")
            text_2.insert("insert", "\r\n")
            text_2.insert("insert", "a new line ")
            text_2["state"] = tk.DISABLED
            text_2.pack()
        
            help.mainloop()
        

        tk.Button(window, text='Show help message', command=create).grid(row=0, column=4)


        max_num_candidate_imgs = 2
        #draw left images
        max_num_img = len(smell_list[0][1:])
        count_img = 0

        canvas_1_1 = tk.Canvas(window, bg=color_1, height=height, width=width)
        count_img += 1
        if count_img <= max_num_img:
            smell = smell_list[0][count_img]
            if smell == 'AMMONIA/URINOUS':
                smell = 'AMMONIA-URINOUS'
            image_file_1_1 = tk.PhotoImage(file='images/%s/resize_%s.png'%(smell,random.sample(range(1,max_num_candidate_imgs+1),1)[0]))
            canvas_1_1.create_image(width/2+2, 7, anchor='n',image=image_file_1_1)
            tk.Label(window, text=smell_list[0][count_img], width=20, height=1).grid(row=2, column=0)
        canvas_1_1.grid(row=1, column=0)

        canvas_1_2 = tk.Canvas(window, bg=color_1, height=height, width=width)
        count_img += 1
        if count_img <= max_num_img:
            smell = smell_list[0][count_img]
            if smell == 'AMMONIA/URINOUS':
                smell = 'AMMONIA-URINOUS'
            image_file_1_2 = tk.PhotoImage(file='images/%s/resize_%s.png'%(smell,random.sample(range(1,max_num_candidate_imgs+1),1)[0]))
            canvas_1_2.create_image(width/2+2, 7, anchor='n',image=image_file_1_2)
            tk.Label(window, text=smell_list[0][count_img], width=20, height=1).grid(row=2, column=1)
        canvas_1_2.grid(row=1, column=1)

        canvas_1_3 = tk.Canvas(window, bg=color_1, height=height, width=width)
        count_img += 1
        if count_img <= max_num_img:
            smell = smell_list[0][count_img]
            if smell == 'AMMONIA/URINOUS':
                smell = 'AMMONIA-URINOUS'
            image_file_1_3 = tk.PhotoImage(file='images/%s/resize_%s.png'%(smell,random.sample(range(1,max_num_candidate_imgs+1),1)[0]))
            canvas_1_3.create_image(width/2+2, 7, anchor='n',image=image_file_1_3)
            tk.Label(window, text=smell_list[0][count_img], width=20, height=1).grid(row=4, column=0)
        canvas_1_3.grid(row=3, column=0)

        canvas_1_4 = tk.Canvas(window, bg=color_1, height=height, width=width)
        count_img += 1
        if count_img <= max_num_img:
            smell = smell_list[0][count_img]
            if smell == 'AMMONIA/URINOUS':
                smell = 'AMMONIA-URINOUS'
            image_file_1_4 = tk.PhotoImage(file='images/%s/resize_%s.png'%(smell,random.sample(range(1,max_num_candidate_imgs+1),1)[0]))
            canvas_1_4.create_image(width/2+2, 7, anchor='n',image=image_file_1_4)
            tk.Label(window, text=smell_list[0][count_img], width=20, height=1).grid(row=4, column=1)
        canvas_1_4.grid(row=3, column=1)



        #draw right images
        max_num_img = len(smell_list[1][1:])
        count_img = 0

        canvas_2_1 = tk.Canvas(window, bg=color_2, height=height, width=width)
        count_img += 1
        if count_img <= max_num_img:
            smell = smell_list[1][count_img]
            if smell == 'AMMONIA/URINOUS':
                smell = 'AMMONIA-URINOUS'
            image_file_2_1 = tk.PhotoImage(file='images/%s/resize_%s.png'%(smell,random.sample(range(1,max_num_candidate_imgs+1),1)[0]))
            canvas_2_1.create_image(width/2+2, 7, anchor='n',image=image_file_2_1)
            tk.Label(window, text=smell_list[1][count_img], width=20, height=1).grid(row=2, column=3)
        canvas_2_1.grid(row=1, column=3)

        canvas_2_2 = tk.Canvas(window, bg=color_2, height=height, width=width)
        count_img += 1
        if count_img <= max_num_img:
            smell = smell_list[1][count_img]
            if smell == 'AMMONIA/URINOUS':
                smell = 'AMMONIA-URINOUS'
            image_file_2_2 = tk.PhotoImage(file='images/%s/resize_%s.png'%(smell,random.sample(range(1,max_num_candidate_imgs+1),1)[0]))
            canvas_2_2.create_image(width/2+2, 7, anchor='n',image=image_file_2_2)
            tk.Label(window, text=smell_list[1][count_img], width=20, height=1).grid(row=2, column=4)
        canvas_2_2.grid(row=1, column=4)

        canvas_2_3 = tk.Canvas(window, bg=color_2, height=height, width=width)
        count_img += 1
        if count_img <= max_num_img:
            smell = smell_list[1][count_img]
            if smell == 'AMMONIA/URINOUS':
                smell = 'AMMONIA-URINOUS'
            image_file_2_3 = tk.PhotoImage(file='images/%s/resize_%s.png'%(smell,random.sample(range(1,max_num_candidate_imgs+1),1)[0]))
            canvas_2_3.create_image(width/2+2, 7, anchor='n',image=image_file_2_3)
            tk.Label(window, text=smell_list[1][count_img], width=20, height=1).grid(row=4, column=3)
        canvas_2_3.grid(row=3, column=3)

        canvas_2_4 = tk.Canvas(window, bg=color_2, height=height, width=width)
        count_img += 1
        if count_img <= max_num_img:
            smell = smell_list[1][count_img]
            if smell == 'AMMONIA/URINOUS':
                smell = 'AMMONIA-URINOUS'
            image_file_2_4 = tk.PhotoImage(file='images/%s/resize_%s.png'%(smell,random.sample(range(1,max_num_candidate_imgs+1),1)[0]))
            canvas_2_4.create_image(width/2+2, 7, anchor='n',image=image_file_2_4)
            tk.Label(window, text=smell_list[1][count_img], width=20, height=1).grid(row=4, column=4)
        canvas_2_4.grid(row=3, column=4)

        canvas_center = tk.Canvas(window, bg='white', height=height, width=350)
        #draw center
        image_file_center = tk.PhotoImage(file='images/nose.png')
        image_center = canvas_center.create_image(178, 40, anchor='n',image=image_file_center)
        canvas_center.grid(row=1, column=2)

        frame_choose = tk.Frame(window)
        frame_choose.grid(row=3, column=2)

        tk.Label(frame_choose, bg='#FFF8DC', width=40, text='Please choose your preference on intensity:').pack()
        
        frame_choose_1 = tk.Frame(frame_choose)
        frame_choose_1.pack()
    
        v_1 = tk.IntVar()
        tk.Radiobutton(frame_choose_1, text='Left ', variable=v_1, value=1).pack(side=tk.LEFT,expand=tk.YES,fill=tk.BOTH)
        tk.Radiobutton(frame_choose_1, text='Right', variable=v_1, value=2).pack(side=tk.RIGHT,expand=tk.YES,fill=tk.BOTH)
        
        tk.Label(frame_choose, bg='#FFF8DC', width=40, text='Please choose your preference on pleasantness:').pack()
        
        frame_choose_2 = tk.Frame(frame_choose)
        frame_choose_2.pack()
        
        v_2 = tk.IntVar()
        tk.Radiobutton(frame_choose_2, text='Left ', variable=v_2, value=1).pack(side=tk.LEFT,expand=tk.YES,fill=tk.BOTH)
        tk.Radiobutton(frame_choose_2, text='Right', variable=v_2, value=2).pack(side=tk.RIGHT,expand=tk.YES,fill=tk.BOTH)
        
        tk.Label(frame_choose, bg='#FFF8DC', width=40, text='Please choose your preference on familiarity:').pack()
        
        frame_choose_3 = tk.Frame(frame_choose)
        frame_choose_3.pack()
        
        v_3 = tk.IntVar()
        tk.Radiobutton(frame_choose_3, text='Left ', variable=v_3, value=1).pack(side=tk.LEFT,expand=tk.YES,fill=tk.BOTH)
        tk.Radiobutton(frame_choose_3, text='Right', variable=v_3, value=2).pack(side=tk.RIGHT,expand=tk.YES,fill=tk.BOTH)
        
        preference_intensity = 0
        preference_pleasantness = 0
        preference_familiarity = 0
        def hit_me():
            global preference_intensity,preference_pleasantness,preference_familiarity
            
            preference_intensity = v_1.get()
            preference_pleasantness = v_2.get()
            preference_familiarity = v_3.get()
            
            if preference_intensity!=0 and preference_pleasantness!=0 and preference_familiarity!=0:
                window.destroy()
            else:
                mb.showinfo('Warning','Please make your choice!')

        b_1 = tk.Button(frame_choose, text='Submit', font=('Arial', 16), width=10, height=2, bd=5, relief='ridge', command=hit_me).pack()

        window.mainloop()
        
        #--------------
        #exit(1)
        if preference_intensity==0 or preference_pleasantness==0 or preference_familiarity==0:
            exit(1)
        print("Your chice: ",preference_intensity,preference_pleasantness,preference_familiarity)

        result_dict['preference_intensity'][preference_intensity-3]=1
        result_dict['preference_pleasantness'][preference_pleasantness-3]=1
        result_dict['preference_familiarity'][preference_familiarity-3]=1
        
        count += 1
        print("Congratulations! You have done %s tests, good job!"%count)

        result_data = pd.DataFrame(result_dict)
        #save collected file
        result_data.to_excel("collected_data/collected_preference_data_%s_%s.xlsx"%(subject_id,start_time_str))


    



