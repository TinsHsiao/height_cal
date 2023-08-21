from PyQt5 import QtCore 
from PyQt5.QtGui import QImage, QPixmap
import cv2



class img_controller(object):
    def __init__(self, img_path, label_img, label_file_path, label_ratio, label_img_shape, label_first_click_pos,
                 label_second_click_pos, label_norm_pos, label_real_pos, height):
        self.img_path = img_path
        self.label_img = label_img
        self.label_file_path = label_file_path
        self.label_ratio= label_ratio
        self.label_img_shape = label_img_shape
        self.label_first_click_pos = label_first_click_pos
        self.label_second_click_pos = label_second_click_pos
        self.label_norm_pos = label_norm_pos
        self.label_real_pos = label_real_pos
        self.height = height
        self.ratio_value = 50
        self.read_file_and_init()
        self.__update_img()

    def read_file_and_init(self):
        try:
            print(self.img_path)
            self.img = cv2.imread(self.img_path)
            self.origin_height, self.origin_width, self.origin_channel = self.img.shape            
        except:
            self.img = cv2.imread('test.jpg')
            self.origin_height, self.origin_width, self.origin_channel = self.img.shape    

        bytesPerline = 3 * self.origin_width
        self.qimg = QImage(self.img, self.origin_width, self.origin_height, bytesPerline, QImage.Format_RGB888).rgbSwapped()
        self.origin_qpixmap = QPixmap.fromImage(self.qimg)
        self.ratio_value = 50        
        self.__update_text_file_path()
        self.set_img_ratio()

    def set_img_ratio(self):
        self.ratio_rate = pow(10, (self.ratio_value - 50)/50)
        qpixmap_height = self.origin_height * self.ratio_rate
        self.qpixmap = self.origin_qpixmap.scaledToHeight(qpixmap_height)
        self.__update_img()
        self.__update_text_ratio()
        self.__update_text_img_shape()

    def set_path(self, img_path):
        self.img_path = img_path
        self.read_file_and_init()
        self.__update_img()        

    def __update_img(self):      
        self.label_img.setPixmap(self.qpixmap)
        self.label_img.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.label_img.mousePressEvent = self.get_first_clicked_position
        #self.label_img.mousePressEvent = self.get_second_clicked_position
        

    def __update_text_file_path(self):
        self.label_file_path.setText(f"File path = {self.img_path}")

    def __update_text_ratio(self):
        self.label_ratio.setText(f"{int(100*self.ratio_rate)} %")

    def __update_text_clicked_position_first(self, x, y):
        self.label_first_click_pos.setText(f"first postion = ({int(self.norm_x1*self.origin_width)}, {int(self.norm_y1*self.origin_height)})")
        # self.label_norm_pos.setText(f"Normalized postion = ({self.norm_x:.3f}, {self.norm_y:.3f})")
        # self.label_real_pos.setText(f"Real postion = ({int(self.norm_x*self.origin_width)}, {int(self.norm_y*self.origin_height)})")

    def __update_text_clicked_position_second(self, x, y):
        self.label_second_click_pos.setText(f"second postion = ({int(self.norm_x2*self.origin_width)}, {int(self.norm_y2*self.origin_height)})")

    def __update_text_img_shape(self):
        current_text = f"Current img shape = ({self.qpixmap.width()}, {self.qpixmap.height()})"
        origin_text = f"Origin img shape = ({self.origin_width}, {self.origin_height})"
        self.label_img_shape.setText(current_text+"\t"+origin_text)

    def set_zoom_in(self):
        self.ratio_value = max(0, self.ratio_value - 1)
        self.set_img_ratio()

    def set_zoom_out(self):
        self.ratio_value = min(100, self.ratio_value + 1)
        self.set_img_ratio()

    def set_slider_value(self, value):
        self.ratio_value = value
        self.set_img_ratio()

    def get_first_clicked_position(self, event):
        x = event.pos().x()
        y = event.pos().y() 
        self.norm_x1 = x/self.qpixmap.width()
        self.norm_y1 = y/self.qpixmap.height()
        print(f"first (x, y) = ({int(self.norm_x1*self.origin_width)}, {int(self.norm_y1*self.origin_height)})")
        self.__update_text_clicked_position_first(x, y)
        self.label_img.mousePressEvent = self.get_second_clicked_position

    def get_second_clicked_position(self, event):
        x = event.pos().x()
        y = event.pos().y() 
        self.norm_x2 = x/self.qpixmap.width()
        self.norm_y2 = y/self.qpixmap.height()
        print(f"second (x, y) = ({int(self.norm_x2*self.origin_width)}, {int(self.norm_y2*self.origin_height)})")
        self.__update_text_clicked_position_second(x, y)
        self.calculate_height()

        
    def calculate_height(self) :
        self.deep = 0.3 # m
        self.f = 0.026
        self.pixel_to_realaLength = 0.000025
        self.pixel_difference = abs( int(self.norm_y2*self.origin_height) - int(self.norm_y1*self.origin_height) ) * self.pixel_to_realaLength
        self.height_by_cal = ( self.pixel_difference*self.deep )/self.f
        print(f"Height = {self.height_by_cal:.3f} m ")


