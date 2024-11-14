# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 11:06:12 2024
@author: PDog
"""
from pygaze.keyboard import Keyboard
from pygaze.logfile import Logfile as log
from pygaze.eyetracker import EyeTracker
from pygaze.screen import Screen
from pygaze.display import Display
from pygaze.libtime import get_time,pause
#Visual
DISPSIZE = (1366, 768)
DISPTYPE = 'pygame'
disp = Display()
scr = Screen()
img= r"C:\Users\MACLab\Downloads\philliptest\data"

#Input
tracker= EyeTracker(disp,trackertype='opengaze')
kb= Keyboard()

#Relevant data
fixation= tracker.wait_for_fixation_start()
fixation_end= tracker.wait_for_fixation_end([0])
LPupil, RPupil= tracker.pupil_size()
fixation_start,(fix_x,fix_y)= fixation


#create data file name and header
log =log(filename='EyeData').write(["Timestamp","Fixation_Start","Fixation_End","Fixation_X","Fixation_Y","LPupil","RPupil"])
scr.draw_image(img)
disp.show()

#Start Recording====================================================================================================================
tracker.start_recording()
tracker.log("startexp")

#Zoomin on Fixation Location
if fixation_start != 0:
    tracker.log_var("Fixation_Start",fixation_start)
    tracker.log_var("Fixation_X",fix_x)
    tracker.log_var("Fixation_Y",fix_y)
    scr.draw_image(img,pos=(fix_x,fix_y),scale= 4)
    disp.show()
    
#Pupil diameter every 200ms for 5 seconds since fixation
if fixation_start != 0:
    try:
        for i in range(25):  # now get pupil size for next 5 seconds
            LPupil, RPupil = tracker.pupil_size()
            Timestamp = get_time()
            tracker.log_var("Timestamp", Timestamp)
            tracker.log_var("LPupil", LPupil)
            tracker.log_var("RPupil", RPupil)
            pause(200)

            if kb.get_key(["escape"]):
                scr.draw_image(img, pos=None, scale=None)
                disp.show()
                break  # Exit loop if escape is pressed

        # Log timestamp after the fixation ends
        Timestamp = get_time()
        tracker.log_var("Timestamp", Timestamp)

    except Exception as e:
        print(f"Error occurred: {e}")
     
#DONE
if kb.get_key(['F']):
    tracker.stop_recording()
    tracker.close()
    log.close()
    disp.close()