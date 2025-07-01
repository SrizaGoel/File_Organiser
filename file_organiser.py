'''
# Sort files:

import os
import shutil
file_types={
    "Document":[".doc",".docs","xls",".xlsx",".xlsm",".ppt",".pptx",".pdf","txt",".md",".csv","json",".xml",".yaml",".yml",".log"],
    "Image":[".jpg",".jpeg",".png",".gif",".webp",".svg"],
    "Video":[".mp4"],
    "Audio":[".mp3"],
    "Compressed_files":[".zip"],
    "Code_files":[".py",".java",".cpp",".c",".html",".css",".json",".sql",".ipynb`"]
}
def move_file(filename,file_destination):
    if not os.path.exists(file_destination):
        os.makedirs(file_destination)
    shutil.move(filename,file_destination)


def sort_folder(source_folder):
    for file in os.listdir(source_folder):
        found=False
        if os.path.isfile(os.path.join(source_folder, file)):
            extension=os.path.splitext(file)[1]
            full_file_path = os.path.join(source_folder, file)
            for category,ext in file_types.items():
                if extension in ext:
                    move_file(full_file_path,os.path.join(source_folder,category))
                    found=True
                    break
            if found==False:
                move_file(full_file_path,os.path.join(source_folder,"Others")) 
'''

# Sort + Undo
import os
import shutil
import json
import streamlit as st
import time

file_types={
    "Document":[".doc",".docs","xls",".xlsx",".xlsm",".ppt",".pptx",".pdf","txt",".md",".csv",".json",".xml",".yaml",".yml",".log"],
    "Image":[".jpg",".jpeg",".png",".gif",".webp",".svg"],
    "Video":[".mp4"],
    "Audio":[".mp3"],
    "Compressed_files":[".zip"],
    "Code_files":[".py",".java",".cpp",".c",".html",".css",".sql",".ipynb"]
}

Log_file = "undo.json"

def move_file(filename,file_destination):
    if not os.path.exists(file_destination):
        os.makedirs(file_destination)
    shutil.move(filename,os.path.join(file_destination,os.path.basename(filename)))

def log_file_move(original_path,new_path):
    data={
        'from': original_path,
        'to': os.path.join(new_path,os.path.basename(original_path))
    }
    if not os.path.exists(Log_file):
        undofile=open("undo.json","w")
        data_list=[data]
        json.dump(data_list,undofile,indent=1)
        undofile.close()
    else:
        undofile=open(Log_file,"r+")
        try:
            log_list=json.load(undofile)
        except:
            log_list=[]
        log_list.append(data)
        undofile.seek(0)
        json.dump(log_list, undofile, indent=1)
        undofile.close()

def remove_data(remove_from):
    if os.path.exists(Log_file):
        undofile=open(Log_file,"r+")
        new_data=[]
        try:
            log_list=json.load(undofile)

            for entry in log_list:
                if entry['to']!=remove_from:
                    new_data.append(entry)
            undofile.seek(0)
            undofile.truncate()
            json.dump(new_data,undofile,indent=1)
        except:
            return
        undofile.close()

def is_empty(filename):
    try:
        with open(filename, 'r') as f:
            content = f.read().strip()
            if content == "[]":
                return True
    except:
        return False


def undo(number_undo):
    if not os.path.exists(Log_file) or is_empty(Log_file):
        return
    if os.path.exists(Log_file):
        undofile=open(Log_file,"r")
        try:
            log_list=json.load(undofile)
        except:
            return
        undofile.close()
        for file in reversed(log_list):
            if number_undo:
                if(os.path.exists(file['to'])):
                    move_file(file['to'],os.path.dirname(file['from']))
                    remove_data(file['to'])
                    
                    number_undo=number_undo-1
                    if is_empty(Log_file):
                        st.error("No more file to undo")
                        break
            else:
                st.warning("File not found for undo operation")
                return 0
        undofile.close()
        return 1

def sort_folder(source_folder):
    for file in os.listdir(source_folder):
        found=False
        if os.path.isfile(os.path.join(source_folder,file)):
            extension=os.path.splitext(file)[1]
            full_file_path=os.path.join(source_folder,file)
            for category,ext in file_types.items():
                if extension in ext:
                    dest_path=os.path.join(source_folder,category)
                    move_file(full_file_path,dest_path)
                    log_file_move(full_file_path,dest_path)
                    found=True
                    break
            if not found:
                move_file(full_file_path,os.path.join(source_folder,"Others"))
                log_file_move(full_file_path,os.path.join(source_folder,"Others"))



st.title("Automatic File Organiser")
st.divider()
st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
path=st.text_input("Enter the path of the folder that needs to be sorted : ")
st.markdown("######")
ans=st.selectbox("Are you sure you want to begin file sorting ?  ",["Select","Yes","No"])
st.markdown("</div>", unsafe_allow_html=True)
st.markdown("####")

col1, col2, col3 = st.columns([1, 4, 1])
with col1:

        filesort=st.button("Sort Folder")
    
with col3:

        undomove=st.button("Undo move")

if filesort:
    if path:
         if ans=='Yes':
            with st.spinner("Sorting in progress... "):
                time.sleep(2)
                sort_folder(path)
            st.success("Folder sorted successfully!")
         elif ans == "No":
            st.warning("Sorting cancelled.")
         else:
            st.info("Please confirm Yes or No.")
    else:
         st.error("Please enter a valid folder path")

undo_choice=st.selectbox("Do yo want to undo any moves ? ",["Select","Yes","No"])
if undo_choice.lower().strip() == 'yes':
    number=st.number_input("Enter number of moves to undo : ",min_value=1,step=1)
if undomove:
    if path:
        if undo_choice.lower().strip() == 'yes':
            with st.spinner(f"Undoing {number} last move(s)..."):
                time.sleep(2)
                success=undo(number)    
            if(success):
               st.success(f"Last {number} move(s) undone successfully!")
                
        elif undo_choice.lower().strip() == 'no':
             st.warning("Undo failed")
        else:
             st.info("Please confirm Yes or No.")
    else:
         st.error("Please enter a valid folder path")

