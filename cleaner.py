import sys
from time import sleep
from os import scandir, rename, mkdir
from os.path import splitext, exists, join
from shutil import move
from watchdog.observers import Observer
from watchdog.events import FileSystemEvent, FileSystemEventHandler
import pystray
from pystray import Icon as icon, Menu as menu, MenuItem as item
from PIL import Image

sourceDir = r'...'
fileDestDir = r'...'

def moveFile(dest,currDir,name):
    filename , ext = splitext(name)
    print(dest)
    dest = join(dest,ext.replace('.',''))
    print(dest)
    DirectoryExists = exists(f'{dest}')
    if not(DirectoryExists):
        print(dest)
        mkdir(dest)
        
    FileExists = exists(f'{dest}/{name}')
    newName = name
    if FileExists:
        
        count = 1
        while exit(f'{dest}/{newName}'):
            newName=f'{filename} ({str(count)}{ext})'
            cont +=1
    oldName = join(currDir,name)
    newName = join(currDir,newName)
    rename (oldName,newName)
    move(newName,dest)

for entry in scandir(sourceDir):
    if entry.is_file():
        print(entry.name)
        moveFile(fileDestDir, sourceDir, entry.name)

imageExt = ['.png', '.jpeg', '.jpg', '.jfi', '.jpe', '.jif', '.jfif', '.heif', '.heic',
            '.gif', '.svg', '.svg2', '.eps', '.webp', '.tiff', '.tif', '.ind', '.ai', '.psd']

class Watcher(FileSystemEventHandler):
    def on_modified(self, _):
        self.clean()

    def clean(self):
        with scandir(sourceDir) as entries:
            for entry in entries:
                if entry.is_dir():
                    continue
                for ext in imageExt:
                    if entry.name.endswith(ext):
                        moveFile(fileDestDir,sourceDir,entry.name)
                        break

watcher = Watcher()
observer = Observer()
observer.schedule(watcher,sourceDir,recursive=True)
observer.start()
sleep(20)
observer.stop()
observer.join()

image = Image.new('RGB',(64,64), 'red')
def stop (icon, _):
    observer.stop()
    observer.join()
    icon.stop()

tray = icon(
    'Computer Cleaner',
    icon = image,
    menu=menu(
        item('Exit', stop)
    )
).run
