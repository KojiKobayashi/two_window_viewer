import cv2
import os
import glob
import numpy as np
import Tkinter
import tkFileDialog

class TwoImages:
    def __init__(self):
        self.mode = 0
    def set_files(self, file1, file2):
        self.img1 = cv2.imread(file1)
        self.img2 = cv2.imread(file2)
    def show_image(self):
        concat = cv2.hconcat([self.img1, self.img2])
        message = ""
        print self.mode
        if self.mode == 1:
            message = self._are_same_images()
        cv2.putText(concat, message, (0,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,255), 3)
        cv2.imshow("compare", concat)
    def set_identical_mode(self):
        self.mode = 1
    def _are_same_images(self):
        if np.array_equal(self.img1, self.img2):
            return "SAME"
        else:
            return "NOT SAME"
    def reset_window_position(self):
        cv2.moveWindow("compare", 0, 0)
    def __del__( self ):
        cv2.destroyAllWindows()

def show_two_images(files, dir1, dir2):
    length = len(files)
    counter = 0
    
    two_images = TwoImages()
    while(True):
        f = files[counter]
        file1 = dir1 + "\\" + f
        file2 = dir2 + "\\" + f

        two_images.set_files(file1, file2)
        two_images.show_image()
    
        key = cv2.waitKey(0)
        
        if key == 27:   # esc
            break
        if key == 110:  # n
            counter += 1
        if key == 112:  # p
            counter -= 1
        if key == 63:   # ?
            two_images.set_identical_mode()
        if key == 48:   # 0
            two_images.reset_window_position()

#        print key, message

        if counter >= length:
            counter = 0
        if counter < 0:
            counter = 0
        
    cv2.destroyAllWindows()

def uniq_arrays(arr1, arr2):
    ret_arr = []
    for elem in arr1:
        if elem in arr2:
            ret_arr.append(elem)
    return ret_arr
            
def get_image_files(dir):
    files = []
    for ext in ['png', 'jpg', 'jpeg', 'bmp', 'gif']:
        files += glob.glob(dir + '\*.' + ext)
    files = [f.split("\\")[-1] for f in files]
    return files

def set_two_directory():
    # root setting to prepend blank window
    root = Tkinter.Tk()
    root.withdraw()
    dir1 = tkFileDialog.askdirectory()
    dir2 = tkFileDialog.askdirectory()
    root.destroy()
    return [dir1, dir2]

def main_exe():
    dirs = set_two_directory()

    files1 = get_image_files(dirs[0])
    files2 = get_image_files(dirs[1])

    files = uniq_arrays(files1, files2)

    show_two_images(files, dirs[0], dirs[1])

if __name__ == "__main__":
    main_exe()

    
