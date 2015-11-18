import cv2
import os
import glob
import numpy as np
import Tkinter
import tkFileDialog

class TwoImages:
    def __init__(self):
        self.mode = 0
        self.tmp_message = ""
        self.window_name = "compare"
        self.align = "h"
        self.enlarge_rate = 100
    def set_files(self, files):
        self.imgs = [cv2.imread(f) for f in files]
        self.filename = files[0].split("\\")[-1]

        if self.align == "h":
            self.concat = cv2.hconcat(self.imgs)
        else:
            self.concat = cv2.vconcat(self.imgs)
    def show_image(self):
        message = self._set_message()
        cv2.putText(self.concat, message, (0,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,255), 3)
        width = self.concat.shape[1] * self.enlarge_rate / 100
        height = self.concat.shape[0] * self.enlarge_rate / 100
        disp_img = cv2.resize(self.concat, (width, height))
        cv2.imshow(self.window_name, disp_img)
    def set_identical_mode(self):
        self.mode = 1
    def set_show_filename_mode(self):
        self.mode = 2
    def save(self):
        cv2.imwrite(self.filename, self.concat)
        self.tmp_message = "saved"
        self.once_message_flag = True
    def reset_window_position(self):
        cv2.moveWindow(self.window_name, 0, 0)
    def set_align_vertical(self):
        self.align = "v"
    def set_align_horizontal(self):
        self.align = "h"
    def enlarge_image(self):
        self.enlarge_rate = min(self.enlarge_rate + 10, 500)
    def decrease_image(self):
        self.enlarge_rate = max(self.enlarge_rate - 10, 10)

    def _set_message(self):
        message = ""
        if self.tmp_message == "":
            if self.mode == 1:
                message = self._are_same_images()
            elif self.mode == 2:
                message = self.filename
        else:
            message = self.tmp_message
            self.tmp_message = ""
        return message
    def _are_same_images(self):
        for img in self.imgs:
            if not np.array_equal(self.imgs[0],img):
                return "NOT SAME"
        return "SAME"
    def __del__( self ):
        cv2.destroyAllWindows()

def show_two_images(files, dirs):
    length = len(files)
    counter = 0
    
    two_images = TwoImages()
    while(True):
        f = files[counter]
        filePaths = [os.path.join(dir, f) for dir in dirs]

        two_images.set_files(filePaths)
        two_images.show_image()
    
        key = cv2.waitKey(0)

        if key == 27:       # esc
            break
        elif key == ord('n'):
            counter += 1
        elif key == ord('p'):
            counter -= 1
        elif key == ord('?'):
            two_images.set_identical_mode()
        elif key == ord('0'):
            two_images.reset_window_position()
        elif key == ord('f'):
            two_images.set_show_filename_mode()
        elif key == ord('s'):
            two_images.save()
        elif key == ord('v'):
            two_images.set_align_vertical()
        elif key == ord('h'):
            two_images.set_align_horizontal()
        elif key == ord('+'):
            two_images.enlarge_image()
        elif key == ord('-'):
            two_images.decrease_image()

        if counter >= length:
            counter = length - 1
        if counter < 0:
            counter = 0
    
#        print key
        
    cv2.destroyAllWindows()

def uniq_arrays(arrays):
    ret_arr = []
    for item in arrays[0]:
        if all(item in arr for arr in arrays):
            ret_arr.append(item)
    return ret_arr
            
def get_image_files(dir):
    files = []
    for ext in ['png', 'jpg', 'jpeg', 'bmp', 'gif']:
        files += glob.glob(dir + '\*.' + ext)
    files = [f.split("\\")[-1] for f in files]
    return files

def set_n_directory():
    # root setting to prepend blank window
    root = Tkinter.Tk()
    root.withdraw()
    dirs = []
    dir_opt = options = {}
    while True:
        tmp = tkFileDialog.askdirectory(**dir_opt)
        if not tmp:
            break
        dirs.append(tmp)
        options['initialdir'] = tmp

    root.destroy()
    return dirs

def main_exe():
    dirs = set_n_directory()

    files_set = [get_image_files(dir) for dir in dirs]
    files = uniq_arrays(files_set)
    if len(files) == 0:
        return

    show_two_images(files, dirs)

if __name__ == "__main__":
    main_exe()

    
