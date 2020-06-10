import cv2
import os

def resize(dir,filename, width_, height_):
    img = cv2.imread("%s/%s"%(dir,filename), -1)
    if img is None:
        print("Error: could not load image")
        os._exit(0)

    height, width = img.shape[:2]

    size = (width_,height_)
    shrink = cv2.resize(img, size, interpolation=cv2.INTER_AREA)

    cv2.imwrite("%s/resize_%s"%(dir,filename),shrink)



def eachFile(filepath):
    pathDir =  os.listdir(filepath)
    for allDir in pathDir:
        child = os.path.join('%s%s' % (filepath, allDir))
        if os.path.isdir(child):
            pathDir_ =  os.listdir(child)
            for allDir_ in pathDir_:
                child_ = os.path.join('%s/%s' % (child, allDir_))
                print(child_)
                resize(child,allDir_,190,190)

if __name__ == '__main__':
    eachFile('./')
    #resize(".","helpmessage.png", 900, 600)
    


