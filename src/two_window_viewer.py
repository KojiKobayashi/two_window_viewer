import cv2
import os
import glob
import numpy as np
import tkinter
import tkinter.filedialog


class TwoImages:

    def __init__(self):
        self.mode = 0
        self.tmp_message = ""
        self.window_name = "compare"
        self.align = "h"
        self.enlarge_rate = 100

    def set_files(self, files):
        self.imgs = [cv2.imread(f.encode("shift_jis").decode("utf-8"))
                     for f in files]
        self.filename = files[0].split("\\")[-1]

        if self.align == "h":
            max_h = max([img.shape[0] for img in self.imgs])
            show_imgs = [self._resize_h(img, max_h) for img in self.imgs]
            self.concat = cv2.hconcat(show_imgs)
        else:
            max_w = max([img.shape[1] for img in self.imgs])
            show_imgs = [self._resize_w(img, max_w) for img in self.imgs]
            self.concat = cv2.vconcat(show_imgs)

    def show_image(self):
        message = self._set_message()
        width = self.concat.shape[1] * self.enlarge_rate // 100
        height = self.concat.shape[0] * self.enlarge_rate // 100
        disp_img = cv2.resize(self.concat, (width, height))
        cv2.putText(disp_img, message, (0, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 3)
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

    def reset_window_message(self):
        self.mode = 0

    def are_same_images(self):
        return self._are_same_images()

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
            if not np.array_equal(self.imgs[0], img):
                return "NOT SAME"
        return "SAME"

    def _resize_w(self, img, w):
        h = img.shape[0] * w // img.shape[1]
        return cv2.resize(img, (w, h))

    def _resize_h(self, img, h):
        w = img.shape[1] * h // img.shape[0]
        return cv2.resize(img, (w, h))

    def __del__(self):
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
        elif key == ord('a'):
            counter = 0
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
        elif key == ord('r'):
            two_images.reset_window_message()
        elif key == ord('j'):
            if two_images.are_same_images() == "NOT SAME":
                while(key == ord('j')):
                    key = cv2.waitKey(100)
            else:
                counter += 1

        if counter >= length:
            counter = length - 1
        if counter < 0:
            counter = 0

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
    root = tkinter.Tk()
    root.withdraw()
    dirs = []
    dir_opt = options = {}
    while True:
        tmp = tkinter.filedialog.askdirectory(**dir_opt)
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
