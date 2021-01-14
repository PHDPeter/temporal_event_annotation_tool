import cv2
import os
import json
import textwrap

import time

DISPLAY_IMAGE_SIZE = 500
BORDER_SIZE = 50
recorde_BORDER_COLOR = (0, 0, 255)
none_act_BORDER_COLOR = (0, 255, 0)


font                   = cv2.FONT_HERSHEY_SIMPLEX
topLeftCornerOfText = (10,48)#48)
bottomLeftCornerOfText = (10,460)
centerOfText=(150,250)
bottomRightCornerOfText = (100,460)
fontScale              = 0.5
fontColor              = (255,255,255)
lineType               = 2


def testing_frame():
    video_name="/media/peter/Maxtor/UCF_Crimes/Videos/Fighting/Fighting005_x264.mp4"
    # Open the video file
    cap = cv2.VideoCapture(video_name)

    # Set frame_no in range 0.0-1.0
    # In this example we have a video of 30 seconds having 25 frames per seconds, thus we have 750 frames.
    # The examined frame must get a value from 0 to 749.
    # For more info about the video flags see here: https://stackoverflow.com/questions/11420748/setting-camera-parameters-in-opencv-python
    # Here we select the last frame as frame sequence=749. In case you want to select other frame change value 749.
    # BE CAREFUL! Each video has different time length and frame rate.
    # So make sure that you have the right parameters for the right video!
    time_length = 30.0
    fps = 25
    frame_seq = 749
    frame_no = (frame_seq / (time_length * fps))

    # The first argument of cap.set(), number 2 defines that parameter for setting the frame selection.
    # Number 2 defines flag CV_CAP_PROP_POS_FRAMES which is a 0-based index of the frame to be decoded/captured next.
    # The second argument defines the frame number in range 0.0-1.0
    cap.set(1, frame_no);

    # Read the next frame from the video. If you set frame 749 above then the code will return the last frame.
    ret, frame = cap.read()

    # Set grayscale colorspace for the frame.
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Cut the video extension to have the name of the video
    my_video_name = video_name.split(".")[0]

    # Display the resulting frame
    cv2.imshow(my_video_name + ' frame ' + str(frame_seq), gray)

def nothing(x):
    pass


def tool(NAME_OF_SOURCE_VIDEO,PATH_FILE_NAME_TO_SAVE_RESULT,PATH_FILE\
         ,start_frame=[],end_frame=[],last_store=[None]):
    videoReader = cv2.VideoCapture(PATH_FILE+"/"+NAME_OF_SOURCE_VIDEO)

    length = int(videoReader.get(cv2.CAP_PROP_FRAME_COUNT))
    cv2.namedWindow('Frame')
    cv2.createTrackbar('scrub bar', 'Frame', 0, length, nothing)
    #cv2.createTrackbar('progress bar', 'Frame', 0, length,nothing)
    #cv2.createTrackbar('end', 'mywindow', 100, length, onChange)

    #onChange(0,videoReader)
    #end = cv2.getTrackbarPos('end', 'Frame')

    shouldSaveResult = (PATH_FILE_NAME_TO_SAVE_RESULT != None)

    listOfForwardTime = []
    #
    frame_cout=0
    #start_frame=[]
    #end_frame=[]
    start_done = False
    end_done = False
    curent_BORDER_COLOR=none_act_BORDER_COLOR
    if len(start_frame)>=0:
        if len(start_frame)==len(end_frame):
            text_used = "nothing recording [" + str(start_frame) + "," + str(end_frame) + "]"
            curent_BORDER_COLOR = none_act_BORDER_COLOR
        else:
            text_used = "Action recording [" + str(start_frame) + "," + str(end_frame) + "]"
            curent_BORDER_COLOR = recorde_BORDER_COLOR
            start_done = True

    else:
        text_used = "nothing recording [[],[]]"
#    currentImage_store=[]
#    while isCurrentFrameValid:
#        targetSize = DISPLAY_IMAGE_SIZE - 2 * BORDER_SIZE
#        currentImage_store.append(cv2.resize(currentImage, (targetSize, targetSize)))

    loop_end=True
    pues=False
    #last_store=[None]
    while loop_end:
        videoReader.set(1, frame_cout)
        isCurrentFrameValid, currentImage = videoReader.read()
        cv2.imshow('Frame',currentImage)
        targetSize = DISPLAY_IMAGE_SIZE - 2 * BORDER_SIZE
        currentImage = cv2.resize(currentImage, (targetSize, targetSize))

        #borrder coler
        resultImage = cv2.copyMakeBorder(currentImage,
                                         BORDER_SIZE,
                                         BORDER_SIZE,
                                         BORDER_SIZE,
                                         BORDER_SIZE,
                                         cv2.BORDER_CONSTANT,
                                         value=curent_BORDER_COLOR)
        #text
        wrapped_text = textwrap.wrap(text_used, width=40)
        iy=0
        for line in wrapped_text:
            textsize = cv2.getTextSize(line, font, fontScale, lineType)[0]
            gap = textsize[1] + 10
            y = int((topLeftCornerOfText[0] + textsize[1])) + iy * gap
            x = topLeftCornerOfText[1] #- textsize[0]) / 2)
            resultImage=cv2.putText(resultImage, line,
                                    (x,y),
                    font,
                    fontScale,
                    fontColor,
                    lineType)
            iy=iy+1
        #frame cout
        resultImage=cv2.putText(resultImage, str(frame_cout)+"/"+str(length),
                    bottomLeftCornerOfText,
                    font,
                    fontScale,
                    fontColor,
                    lineType)

        #file name
        resultImage=cv2.putText(resultImage, " - "+str(NAME_OF_SOURCE_VIDEO),
                    bottomRightCornerOfText,
                    font,
                    fontScale,
                    fontColor,
                    lineType)


        cv2.imshow('Frame', resultImage)
        userResponse = cv2.waitKey(40)
        if userResponse == ord('s'): #and end_done==False:
            if start_done==False:
                start_frame.append(frame_cout)
                last_store.append("start_store")
                print("start frame " + str(start_frame))
                #print("start_done "+str(start_done))
                start_done=True
                #print("start_done " + str(start_done))
                curent_BORDER_COLOR=recorde_BORDER_COLOR
                text_used="Action recording ["+str(start_frame)+","+str(end_frame)+"]"
            else:
                end_frame.append(frame_cout)
                last_store.append("end_store")
                print("end frame " + str(end_frame))
                curent_BORDER_COLOR = none_act_BORDER_COLOR
                text_used = "nothing recording ["+str(start_frame)+","+str(end_frame)+"]"
                #end_done=True
                start_done = False

        if userResponse == ord('d'): #and end_done==False:
            if last_store[-1] == "start_store":
                del start_frame[-1]
                del last_store[-1]
                curent_BORDER_COLOR = none_act_BORDER_COLOR
                text_used = "nothing recording ["+str(start_frame)+","+str(end_frame)+"]"
                start_done = False
            elif last_store[-1] == "end_store":
                del end_frame[-1]
                del last_store[-1]
                curent_BORDER_COLOR=recorde_BORDER_COLOR
                text_used="Action recording ["+str(start_frame)+","+str(end_frame)+"]"
                start_done = True
            elif last_store[-1]==None:
                print("silly you nothing to get rid of yet")

        #userResponse = cv2.waitKey(25)
        if userResponse == ord('q'):#if userResponse == ord('q'):
            loop_end=False
            videoReader.release()
            #cv2.destroyAllWindows()
            break

        #else:
            #isCurrentFrameValid, currentImage = videoReader.read()

        barFrame = cv2.getTrackbarPos('scrub bar', 'Frame')

        if userResponse==ord('z'):#27:
            #frame_cout = frame_cout - 1
            barFrame=barFrame-1
            userResponse = cv2.waitKey(40)
        elif userResponse == ord('c'):
            #frame_cout = frame_cout + 4
            barFrame = barFrame +4
            userResponse = cv2.waitKey(40)
        elif userResponse == ord('v'):
            #frame_cout = frame_cout + 6
            barFrame = barFrame + 6
            userResponse = cv2.waitKey(40)
        elif userResponse==ord('x'):
            if pues!=True:
                #frame_cout = frame_cout #+ 2
                pues=True
            else:
                #frame_cout = frame_cout
                pues = False

        elif pues==True:
            barFrame = barFrame
            #frame_cout = frame_cout
        else:
            barFrame = barFrame+1
            #frame_cout = frame_cout + 1


        # get current positions of four trackbars
        #cv2.setTrackbarPos('scrub bar', 'Frame', frame_cout)

        #barFrame = cv2.getTrackbarPos('scrub bar', 'Frame')

        #print(barFrame)
        #print("frame "+str(frame_cout))
        if int(barFrame) != int(frame_cout+1):
            #cv2.setTrackbarPos('scrub bar', 'Frame', barFrame)
            #fame_cout=fame_cout+1
            #print("changeing the due to")
            frame_cout=barFrame
            cv2.setTrackbarPos('scrub bar', 'Frame', frame_cout)  # barFrame ==
        else:
            frame_cout=frame_cout + 1
            cv2.setTrackbarPos('scrub bar', 'Frame', frame_cout)# barFrame ==


        #print("frame_cout "+str(frame_cout))
        #print("frame " + str(frame_cout))
        #print(length)
        if frame_cout==length-1 or frame_cout==length or frame_cout>length:
            loop_end = False

        #if frame_cout
    # end mesage
    resultImage = cv2.putText(resultImage, str("Ended? ('N' to next 'R' to redo)"),
                              centerOfText,
                              font,
                              fontScale,
                              fontColor,
                              lineType)
    cv2.imshow('Frame', resultImage)

    # When everything done, release the video capture object
    videoReader.release()
    #cv2.destroyAllWindows()
    print("start frame "+str(start_frame))
    #if end_frame==None:
    print("end frame "+str(end_frame))
    return start_frame,end_frame,last_store

def annotation_openCV(PATH_FILE):
    #/media/peter/Maxtor/data/Real Life Violence Dataset/Violence
    #PATH_FILE ='/home/barbara/Desktop/car_data/Normal/Nevsky prospect traffic surveillance video'#"/media/peter/Maxtor/youtube_cctv_data"#"/home/peter/Documents/IISP/youtube_cctv_data"

    #PATH_FILE_NAME_OF_SOURCE_VIDEO_list=["/home/peter/Documents/gits/data/Punch/v_Punch_g02_c01.avi","/home/peter/Documents/gits/data/Punch/v_Punch_g02_c02.avi"]
    NAME_OF_SOURCE_VIDEO_list=os.listdir(PATH_FILE)

    while all([os.path.isfile(PATH_FILE + "/" + vid) for vid in NAME_OF_SOURCE_VIDEO_list]) is False:
        # vido_files=os.listdir(parth)
        # os.chdir(parth + "/antation_of_data")
        print(len(NAME_OF_SOURCE_VIDEO_list))
        for vid in NAME_OF_SOURCE_VIDEO_list:
            path = str(PATH_FILE + "/" + vid)
            print(path)
            if os.path.isfile(path) == False:
                print("removed " + str(vid))
                b = NAME_OF_SOURCE_VIDEO_list.index(vid)
                print(NAME_OF_SOURCE_VIDEO_list[b])
                del NAME_OF_SOURCE_VIDEO_list[b]

    if "antation_of_data" in NAME_OF_SOURCE_VIDEO_list:
        b = NAME_OF_SOURCE_VIDEO_list.index("antation_of_data")
        del NAME_OF_SOURCE_VIDEO_list[b]
    if "antated_vidos" in NAME_OF_SOURCE_VIDEO_list:
            b = NAME_OF_SOURCE_VIDEO_list.index("antated_vidos")
            del NAME_OF_SOURCE_VIDEO_list[b]
    if "Need_to_redo"  in NAME_OF_SOURCE_VIDEO_list:
            b = NAME_OF_SOURCE_VIDEO_list.index("Need_to_redo")
            del NAME_OF_SOURCE_VIDEO_list[b]

    PATH_FILE_NAME_TO_SAVE_RESULT=None
    #for PATH_FILE_NAME_OF_SOURCE_VIDEO in PATH_FILE_NAME_OF_SOURCE_VIDEO_list:
    running = True
    t=0
    start_frame=[]
    end_frame = []
    last_store = [None]
    while running==True and t<len(NAME_OF_SOURCE_VIDEO_list):
        if ".webm" in NAME_OF_SOURCE_VIDEO_list[t]:
            set_n = 5
        else:
            set_n = 4
        FeaturePath = NAME_OF_SOURCE_VIDEO_list[t][0:-set_n]
        print("t "+str(t))
        print(FeaturePath+'.json')
        if os.path.exists(PATH_FILE+"/antation_of_data/"+FeaturePath+'.json'):
            print("skip as it is done")
            t=t+1
        else:
            start_frame,end_frame,last_store=tool(NAME_OF_SOURCE_VIDEO_list[t],\
                                       PATH_FILE_NAME_TO_SAVE_RESULT,PATH_FILE,\
                                       start_frame=start_frame,end_frame=end_frame,last_store=last_store)
            next_vid=False
            while next_vid!=True:
                #time.sleep(1)
                userResponse = cv2.waitKey(40)
                if userResponse==ord('n'):
                    next_vid = True
                    cv2.destroyAllWindows()
                    annotation={"start_frame":start_frame,'end_frame':end_frame}
                    #FeaturePath = NAME_OF_SOURCE_VIDEO_list[t][0:-4]
                    print("saving?")
                    print(os.getcwd())
                    print(FeaturePath)
                    if os.path.exists(PATH_FILE+"/antation_of_data")==False:
                        os.mkdir(PATH_FILE+"/antation_of_data")
                        #os.chdir(PATH_FILE+"/antation_of_data")
                    #else:
                    os.chdir(PATH_FILE + "/antation_of_data")
                    #filename = rs.SaveFileName(PATH_FILE+'.txt', filter)
                    with open(FeaturePath+'.json', 'w') as json_file:
                        print(json_file)
                        json.dump(annotation, json_file)
                    t=t+1
                    start_frame=[]
                    end_frame=[]
                    last_store = [None]
                if userResponse==ord('r'):
                    next_vid = True
                    t=t#not need but to ponit out
                    start_frame=start_frame
                    end_frame=end_frame
                    last_store = last_store

                elif userResponse == ord('q'):
                    print("Dont save just move to the next one")
                    t=t+1
                    start_frame=[]
                    end_frame=[]
                    last_store = [None]
                    next_vid = True




    cv2.destroyAllWindows()

if __name__ == '__main__':#
    #PATH_FILE='/home/peter/Documents/gits/data/Punch'
    #PATH_FILE='/home/peter/Documents/IISP/youtube_cctv_data'

    #PATH_FILE='/media/peter/Maxtor/UCF_Crimes/Videos/Fighting'
    #PATH_FILE='/media/peter/Maxtor/UCF_Crimes/Videos/Assault'
    #PATH_FILE ='/media/peter/Maxtor/UCF_Crimes/Videos/Abuse'
    #PATH_FILE ='/media/peter/Maxtor/UCF_Crimes/Videos/Arrest'

    #PATH_FILE ="/media/peter/Maxtor/UCF_Crimes/Videos/Fighting/Need_to_redo"
    PATH_FILE = '/home/barbara/Desktop/car_data/Normal/Nevsky prospect traffic surveillance video'  # "/media/peter/Maxtor/youtube_cctv_data"#"/home/peter/Documents/IISP/youtube_cctv_data"
    annotation_openCV(PATH_FILE)

    # #/media/peter/Maxtor/data/Real Life Violence Dataset/Violence
    # PATH_FILE ='/home/barbara/Desktop/car_data/Normal/Nevsky prospect traffic surveillance video'#"/media/peter/Maxtor/youtube_cctv_data"#"/home/peter/Documents/IISP/youtube_cctv_data"
    #
    # #PATH_FILE_NAME_OF_SOURCE_VIDEO_list=["/home/peter/Documents/gits/data/Punch/v_Punch_g02_c01.avi","/home/peter/Documents/gits/data/Punch/v_Punch_g02_c02.avi"]
    # NAME_OF_SOURCE_VIDEO_list=os.listdir(PATH_FILE)
    #
    # while all([os.path.isfile(PATH_FILE + "/" + vid) for vid in NAME_OF_SOURCE_VIDEO_list]) is False:
    #     # vido_files=os.listdir(parth)
    #     # os.chdir(parth + "/antation_of_data")
    #     print(len(NAME_OF_SOURCE_VIDEO_list))
    #     for vid in NAME_OF_SOURCE_VIDEO_list:
    #         path = str(PATH_FILE + "/" + vid)
    #         print(path)
    #         if os.path.isfile(path) == False:
    #             print("removed " + str(vid))
    #             b = NAME_OF_SOURCE_VIDEO_list.index(vid)
    #             print(NAME_OF_SOURCE_VIDEO_list[b])
    #             del NAME_OF_SOURCE_VIDEO_list[b]
    #
    # if "antation_of_data" in NAME_OF_SOURCE_VIDEO_list:
    #     b = NAME_OF_SOURCE_VIDEO_list.index("antation_of_data")
    #     del NAME_OF_SOURCE_VIDEO_list[b]
    # if "antated_vidos" in NAME_OF_SOURCE_VIDEO_list:
    #         b = NAME_OF_SOURCE_VIDEO_list.index("antated_vidos")
    #         del NAME_OF_SOURCE_VIDEO_list[b]
    # if "Need_to_redo"  in NAME_OF_SOURCE_VIDEO_list:
    #         b = NAME_OF_SOURCE_VIDEO_list.index("Need_to_redo")
    #         del NAME_OF_SOURCE_VIDEO_list[b]
    #
    # PATH_FILE_NAME_TO_SAVE_RESULT=None
    # #for PATH_FILE_NAME_OF_SOURCE_VIDEO in PATH_FILE_NAME_OF_SOURCE_VIDEO_list:
    # running = True
    # t=0
    # start_frame=[]
    # end_frame = []
    # last_store = [None]
    # while running==True and t<len(NAME_OF_SOURCE_VIDEO_list):
    #     if ".webm" in NAME_OF_SOURCE_VIDEO_list[t]:
    #         set_n = 5
    #     else:
    #         set_n = 4
    #     FeaturePath = NAME_OF_SOURCE_VIDEO_list[t][0:-set_n]
    #     print("t "+str(t))
    #     print(FeaturePath+'.json')
    #     if os.path.exists(PATH_FILE+"/antation_of_data/"+FeaturePath+'.json'):
    #         print("skip as it is done")
    #         t=t+1
    #     else:
    #         start_frame,end_frame,last_store=tool(NAME_OF_SOURCE_VIDEO_list[t],\
    #                                    PATH_FILE_NAME_TO_SAVE_RESULT,PATH_FILE,\
    #                                    start_frame=start_frame,end_frame=end_frame,last_store=last_store)
    #         next_vid=False
    #         while next_vid!=True:
    #             #time.sleep(1)
    #             userResponse = cv2.waitKey(40)
    #             if userResponse==ord('n'):
    #                 next_vid = True
    #                 cv2.destroyAllWindows()
    #                 annotation={"start_frame":start_frame,'end_frame':end_frame}
    #                 #FeaturePath = NAME_OF_SOURCE_VIDEO_list[t][0:-4]
    #                 print("saving?")
    #                 print(os.getcwd())
    #                 print(FeaturePath)
    #                 if os.path.exists(PATH_FILE+"/antation_of_data")==False:
    #                     os.mkdir(PATH_FILE+"/antation_of_data")
    #                     #os.chdir(PATH_FILE+"/antation_of_data")
    #                 #else:
    #                 os.chdir(PATH_FILE + "/antation_of_data")
    #                 #filename = rs.SaveFileName(PATH_FILE+'.txt', filter)
    #                 with open(FeaturePath+'.json', 'w') as json_file:
    #                     print(json_file)
    #                     json.dump(annotation, json_file)
    #                 t=t+1
    #                 start_frame=[]
    #                 end_frame=[]
    #                 last_store = [None]
    #             if userResponse==ord('r'):
    #                 next_vid = True
    #                 t=t#not need but to ponit out
    #                 start_frame=start_frame
    #                 end_frame=end_frame
    #                 last_store = last_store
    #
    #             elif userResponse == ord('q'):
    #                 print("Dont save just move to the next one")
    #                 t=t+1
    #                 start_frame=[]
    #                 end_frame=[]
    #                 last_store = [None]
    #                 next_vid = True
    #
    #
    #
    #
    # cv2.destroyAllWindows()

#    testing_frame()