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

if __name__=="__main__":
    path=input("Enter the path of the folder that needs to be sorted : ")
    ans=input("Are you sure you want to begin file sorting ? (y,n) : ")
    if ans=='y' or ans =='Y':
        sort_folder(path)