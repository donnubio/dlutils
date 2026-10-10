import numpy as np
import os
import requests
import subprocess
# import dropbox
from pathlib import Path


import zipfile
import shutil 
from IPython.display import FileLink, FileLinks
import glob

def md(dir):
    try: 
        os.makedirs(dir)
    except:
        pass 


def get_all_filenames_from_dir(dir, mask='*', ext='.png'):
    fn = Path(dir).with_suffix('')
    fn = sorted(list(fn.glob(mask+ext)))  
    return fn


def get_links_on_files(dir):
    '''
        get_links_on_files('./log/*')
        отримати посилання для закачки 
    '''
    [print( FileLink(f) ) for f in glob.glob(dir) if os.path.isfile(f)]

#######################################################

def add_folder_and_multiple_files_to_zip(zip_file_path,
                                         folder_to_add = None, 
                                         files_to_add = None, 
                                         add_without_file_path=True):
    '''
        add_folder_and_multiple_files_to_zip(zip_file_path='/home/user/wk/tmp/cnn/aa5.zip',
                                            folder_to_add=tensorboard_log_dir,##log directory for TensorBoard
                                            files_to_add=[csvlog_filepath, checkpoint_filepath], #.log .h5
                                            add_without_file_path=True)
    '''

    if folder_to_add is not None:
        if os.path.isdir(folder_to_add):
            farch = shutil.make_archive(zip_file_path.rsplit('.',1)[-2], zip_file_path.rsplit('.',1)[-1], 
                                        root_dir=os.path.normpath(folder_to_add).rsplit("/",1)[-2],
                                        base_dir=os.path.normpath(folder_to_add).rsplit("/",1)[-1])
    with zipfile.ZipFile(zip_file_path, 'a') as zip_ref:
        if files_to_add is not None:
            for file in files_to_add:
                if os.path.isfile(file):
                    if add_without_file_path:
                        zip_ref.write(file, os.path.basename(file))
                    else:
                        zip_ref.write(file)
    return FileLink(zip_file_path)


def send_msg_telegram(chat_id, token, msg):
    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={msg}"
    #print(requests.get(url).json()) # this sends the message    
    requests.get(url).json()

def send_file_telegram(chat_id, token, fname):
    document = open(fname, "rb")
    url = f"https://api.telegram.org/bot{token}/sendDocument"
    response = requests.post(url, data={'chat_id': chat_id}, files={'document': document})


def gdrive_download(url, out_path_fn=None):
    #url = 'https://drive.google.com/file/d/1FRSE3ios0biBn8h0P2BM_rE78925LYRR/view?usp=sharing'
    #out_path_fn = 'model1.keras' '/a/b/' '/a/b/c.txt' None
    try:
        import gdown
    except ModuleNotFoundError:
        #!pip install gdown -q
        subprocess.run(["pip", "install", "gdown", "-q"]) 
        import gdown
    fn = gdown.download(url, output=out_path_fn, quiet=True, fuzzy=True)
    return fn


def Upload2Dropbox(token, in_fn, target_dir, target_fn=None):
    # Upload2Dropbox(token=TOKEN,in_fn='a.txt',target_dir='/2', target_fn=None)
    # Upload2Dropbox(token=TOKEN,in_fn='a.txt',target_dir='/2', target_fn='e.txt')
    # https://www.geeksforgeeks.org/how-to-automate-the-storage-using-dropbox-api-in-python/
    # токен генерувати в ост чергу
    # big files and other see:
    # https://stackoverflow.com/questions/23894221/upload-file-to-my-dropbox-from-python-script

    try:
        import dropbox
    except ModuleNotFoundError:
        #!pip install dropbox -q
        subprocess.run(["pip", "install", "dropbox", "-q"]) 
        import dropbox

    in_fn=Path(in_fn) 
    target_dir=Path(target_dir)
    if target_fn is None:
        target_fn = target_dir / in_fn
    else:
        target_fn = target_dir / target_fn
    
    # Create a dropbox object using an API v2 key
    d = dropbox.Dropbox(token)
    # open the file and upload it
    with in_fn.open("rb") as f:
       # upload gives you metadata about the file
       meta = d.files_upload(f.read(), str(target_fn), mode=dropbox.files.WriteMode("overwrite"))

