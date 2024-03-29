import csv
import time
import board
import busio
import adafruit_adxl34x
import adafruit_tca9548a
from datetime import datetime
from time import sleep
import os
# from seismic_trial_plotting import *
from led_alert import *
# from lcd_display_alert import *
from threading import *
from buzzer_alert import *

i2c = busio.I2C(board.SCL, board.SDA)
tca = adafruit_tca9548a.TCA9548A(i2c)

accel_1 = adafruit_adxl34x.ADXL345(tca[2])
accel_2 = adafruit_adxl34x.ADXL345(tca[3])
accel_3 = adafruit_adxl34x.ADXL345(tca[4])
accel_4 = adafruit_adxl34x.ADXL345(tca[5])
# accelerometer = adafruit_adxl34x.ADXL345(i2c)

# now = datetime.now()


trial_dir = "trial_" + input("Create trial file: ")+"/"
intensity_dir = "intensity_" + input("Create intensity directory: ")
parent_dir = 'trial_seismic_data/'+intensity_dir+"/"
#folder = parent_dir+trial_dir

path = os.path.join(parent_dir, trial_dir)

try:
    os.makedirs(path)
except OSError as error:
    print(error)

x_raw_data = []
y_raw_data = []
z_raw_data = []

green_led()
# display_alert()

class Logger():
#class Logger(Thread):
    def __init__(self):
        self.data_dict = {}
        # Thread.__init__(self)

    def collect_data(self):
        # with open('offset_data/mean_accel_1.csv', 'r') as sensor1_data:
#             sensor1_reader = csv.reader(sensor1_data)
#             for row1 in sensor1_reader:
#                 accel_1_offset = row1
#         with open('offset_data/mean_accel_2.csv', 'r') as sensor2_data:
#             sensor2_reader = csv.reader(sensor2_data)
#             for row2 in sensor2_reader:
#                 accel_2_offset = row2
#         with open('offset_data/mean_accel_3.csv', 'r') as sensor3_data:
#             sensor3_reader = csv.reader(sensor3_data)
#             for row3 in sensor3_reader:
#                 accel_3_offset = row3
#         with open('offset_data/mean_accel_4.csv', 'r') as sensor4_data:
#             sensor4_reader = csv.reader(sensor4_data)
#             for row4 in sensor4_reader:
#                 accel_4_offset = row4
#         '''collect data of accel_1 and assign to class variable'''
#         self.data_dict['accel_1'] = (datetime.now(), accel_1.acceleration[0]-float(accel_1_offset[0]), accel_1.acceleration[1]-float(accel_1_offset[1]), accel_1.acceleration[2]-float(accel_1_offset[2]))
#         '''collect data of accel_2 and assign to class variable'''
#         self.data_dict['accel_2'] = (datetime.now(), accel_2.acceleration[0]-float(accel_2_offset[0]), accel_2.acceleration[1]-float(accel_2_offset[1]), accel_2.acceleration[2]-float(accel_2_offset[2]))
#         '''collect data of accel_3 and assign to class variable'''
#         self.data_dict['accel_3'] = (datetime.now(), accel_3.acceleration[0]-float(accel_3_offset[0]), accel_3.acceleration[1]-float(accel_3_offset[1]), accel_3.acceleration[2]-float(accel_3_offset[2]))
#         '''collect data of accel_4 and assign to class variable'''
#         self.data_dict['accel_4'] = (datetime.now(), accel_4.acceleration[0]-float(accel_4_offset[0]), accel_4.acceleration[1]-float(accel_4_offset[1]), accel_4.acceleration[2]-float(accel_4_offset[2]))

        '''collect data of accel_1 and assign to class variable'''
        self.data_dict['accel_1'] = (datetime.now(), *accel_1.acceleration)
        '''collect data of accel_2 and assign to class variable'''
        self.data_dict['accel_2'] = (datetime.now(), *accel_2.acceleration)
        '''collect data of accel_3 and assign to class variable'''
        self.data_dict['accel_3'] = (datetime.now(), *accel_3.acceleration)
        '''collect data of accel_4 and assign to class variable'''
        self.data_dict['accel_4'] = (datetime.now(), *accel_4.acceleration)

    def print_data(self):
        '''print select data with formatting'''
        print('*'*70)
        print("{0:%Y-%m-%d-%H:%M:%S} , accel_x1:{1:,.3f}, accel_y1:{2:,.3f}, accel_z1:{3:,.3f}".format(*self.data_dict['accel_1']))
        print("{0:%Y-%m-%d-%H:%M:%S} , accel_x2:{1:,.3f}, accel_y2:{2:,.3f}, accel_z2:{3:,.3f}".format(*self.data_dict['accel_2']))
        print("{0:%Y-%m-%d-%H:%M:%S} , accel_x3:{1:,.3f}, accel_y3:{2:,.3f}, accel_z3:{3:,.3f}".format(*self.data_dict['accel_3']))
        print("{0:%Y-%m-%d-%H:%M:%S} , accel_x4:{1:,.3f}, accel_y4:{2:,.3f}, accel_z4:{3:,.3f}".format(*self.data_dict['accel_4']))

    def data_logger(self):
        for file, data in self.data_dict.items():
            with open(path + file + '.csv', 'a+', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(data)

    def earthquake_detection(self):

        accel_1.enable_motion_detection(threshold = 20)
        motion_1 = str(accel_1.events["motion"])
#         print(motion_1)

        accel_2.enable_motion_detection()
        motion_2 = str(accel_2.events["motion"])
#         print(motion_2)

        accel_3.enable_motion_detection()
        motion_3 = str(accel_3.events["motion"])
#         print(motion_3)

        accel_4.enable_motion_detection()
        motion_4 = str(accel_4.events["motion"])
     #    print(motion_4)

        if motion_1 == 'True':
            intensity_level_1()
            red_led()
        elif motion_1 == 'False':
            blue_led()
            red_led_off()
        else:
            pass
        # motion_compare = [motion_1, motion_2, motion_3, motion_4]
#         print(type(motion_compare))
#         detected = all(motion_compare)
#         print(detected)

def main():
    while True:
        logger = Logger()
        logger.collect_data()
        logger.data_logger()
        logger.print_data()
        logger.earthquake_detection()
        sleep(0.05)
#         sleep(1)

main()