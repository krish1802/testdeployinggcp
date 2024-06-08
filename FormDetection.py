import cv2
import numpy as np
import time
import PoseModule as pm
import math
import os

class TestingMain:
    def __init__(self):
        self.output_file = None
        self.performanceFile = None
        self.secPerformanceFile = None

    def mainFunction(self, filename_input):
        cap = cv2.VideoCapture(f"uploads/{filename_input}")

        # Assuming pm is imported or defined somewhere
        detector = pm.poseDetector()
        count = 0
        dir = 0
        pTime = 0

        # Get video properties
        frame_width = int(cap.get(3))
        frame_height = int(cap.get(4))
        fps = int(cap.get(cv2.CAP_PROP_FPS))

        # Define the codec and create VideoWriter object
        output_file = 'outputs/output_video.mp4'
        file_exists = os.path.exists(output_file)
        count = 1

        while file_exists:
            filename, extension = os.path.splitext(output_file)
            output_file = f"{filename}{count}{extension}"
            count += 1
            file_exists = os.path.exists(output_file)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_file, fourcc, fps, (frame_width, frame_height))

        while True:
            success, img = cap.read()
            if not success:
                break

            # Perform pose detection
            img = detector.findPose(img, False)
            lmList = detector.findPosition(img, False)
            if len(lmList) != 0:
                angle = detector.findAngle(img, 12, 14, 16)
                per = np.interp(angle, (60, 160), (100, 0))
                bar = np.interp(angle, (60, 160), (100, 650))
                color = (0, 0, 255)
                # Check for the dumbbell curls
                if per == 100:
                    color = (0, 0, 255)
                    if dir == 0:
                        count += 0.5
                        dir = 1
                if per == 0:
                    color = (0, 255, 0)
                    if dir == 1:
                        count += 0.5
                        dir = 0

                # Draw Bar
                overlay = img.copy()
                alpha = 0.5  # Adjust opacity here
                cv2.rectangle(overlay, (150, 150), (0, 0), color, cv2.FILLED)
                cv2.rectangle(overlay, (int(bar), 100), (0, 0), color, cv2.FILLED)
                img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

                # Draw Rep Count with adjusted opacity
                overlay = img.copy()
                alpha = 0.5  # Adjust opacity here
                cv2.rectangle(overlay, (0, 100), (120, 50), color, cv2.FILLED)
                img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

                # Draw Percentage with adjusted opacity
                overlay = img.copy()
                alpha = 0.5  # Adjust opacity here
                cv2.putText(overlay, f'{int(per)} %', (20, 150), cv2.FONT_HERSHEY_PLAIN, 4, (255, 0, 0), 4)
                img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

                # Draw Rep Count with adjusted opacity
                overlay = img.copy()
                alpha = 0.5  # Adjust opacity here
                cv2.putText(overlay, f'{count}', (0, 100), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)
                img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

            # Write the frame to the output video
            out.write(img)

            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime

        # Release the VideoCapture and VideoWriter objects
        cap.release()
        out.release()
        
        # Set the output file
        self.output_file = output_file
    
    def bicepCurls(self, filename_input): # THIS ONE IS FROM RHS
        # For Importing Video {Devansh}
        cap = cv2.VideoCapture(f"uploads/{filename_input}")

        detector = pm.poseDetector()
        count = 0
        dir = 0
        pTime = 0
        timestamps = []
        shoulder_timestamp = 0
        shoulder_timestamps = []
        backBend = False
        shoulder_backBend = False
        start_time = time.time()
        counted = False
        shoulder_counted = False
        timestamp = 0
        ui_width = 170
        lineColor = (0,255,0)

        # Define the codec and create VideoWriter object
        output_file = 'outputs/output_video.mp4'
        file_exists = os.path.exists(output_file)
        counting = 1

        while file_exists:
            filename, extension = os.path.splitext(output_file)
            output_file = f"{filename}{counting}{extension}"
            counting += 1
            file_exists = os.path.exists(output_file)
        output_frame_width = int(cap.get(3))
        output_frame_height = int(cap.get(4))
        fps = int(cap.get(cv2.CAP_PROP_FPS))

        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_file, fourcc, fps, (output_frame_width+170, output_frame_height))

        while True:
            success, img = cap.read()
            if not success:
                break
            img = detector.findPose(img, False)
            lmList = detector.findPosition(img, False)
            if len(lmList) != 0:
                # #Right Arm
                angle = detector.findAngle(img, 12, 14, 16,lineColor=lineColor)
                hipangle = detector.findAngle(img, 12,24,26, lineColor=lineColor)
                shoudler_angle = detector.findAngle(img, 24, 12, 14, lineColor=lineColor)

                if hipangle > 190:
                    frame_height, frame_width = img.shape[:2]
                    lineColor = (0,0,255)
                    text = "KEEP YOUR BACK STRAIGHT"
                    position = (20, 60)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    scale = 1
                    UI_Color = (0, 0, 0)
                    thickness = 2
                    text_position = put_text_in_frame(img, text, position, font, scale, (0,0,255), thickness)
                    overlay = img.copy()
                    alpha = 0.5  # Adjust opacity here
                    cv2.rectangle(overlay, (frame_width, 100), (0, 0), UI_Color, cv2.FILLED)
                    # cv2.rectangle(overlay, (int(bar), 100), (0, 0), (255,255,255), cv2.FILLED)
                    img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

                    # Get the correct position to ensure text is within the frame
                    
                    cv2.rectangle(overlay, (frame_width,100), (0,0), UI_Color, cv2.FILLED)
                    cv2.putText(img, text, text_position, font, scale, (255,255,255), thickness)
                    backBend = True
                    if counted == True:
                        backBend = False
                        counted = False
                    if backBend == True:
                        end_time = time.time()
                        timestamp = end_time - start_time
                        counted = True
                elif 10 > shoudler_angle > 4:
                    frame_height, frame_width = img.shape[:2]
                    lineColor = (0,0,255)
                    text = "KEEP YOUR HANDS STABLE"
                    position = (20, 60)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    scale = 1
                    UI_Color = (0, 0, 0)
                    thickness = 2
                    text_position = put_text_in_frame(img, text, position, font, scale, (0,0,255), thickness)
                    overlay = img.copy()
                    alpha = 0.5  # Adjust opacity here
                    cv2.rectangle(overlay, (frame_width, 100), (0, 0), UI_Color, cv2.FILLED)
                    # cv2.rectangle(overlay, (int(bar), 100), (0, 0), (255,255,255), cv2.FILLED)
                    img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

                    # Get the correct position to ensure text is within the frame
                    
                    cv2.rectangle(overlay, (frame_width,100), (0,0), UI_Color, cv2.FILLED)
                    cv2.putText(img, text, text_position, font, scale, (255,255,255), thickness)
                    shoulder_backBend = True
                    if shoulder_counted == True:
                        shoulder_backBend = False
                        shoulder_counted = False
                    if shoulder_backBend == True:
                        shoudler_end_time = time.time()
                        shoulder_timestamp = shoudler_end_time - start_time
                        shoulder_counted = True
                else:
                    frame_height, frame_width = img.shape[:2]
                    lineColor = (0,255,0)
                    text = "PROMPTS WILL SHOW HERE"
                    position = (20, 60)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    scale = 1
                    UI_Color = (0, 0, 0)
                    thickness = 2
                    text_position = put_text_in_frame(img, text, position, font, scale, (0,0,255), thickness)
                    overlay = img.copy()
                    alpha = 0.7  # Adjust opacity here
                    cv2.rectangle(overlay, (frame_width, 100), (0, 0), UI_Color, cv2.FILLED)
                    # cv2.rectangle(overlay, (int(bar), 100), (0, 0), (255,255,255), cv2.FILLED)
                    img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

                    # Get the correct position to ensure text is within the frame
                    
                    cv2.rectangle(overlay, (frame_width,100), (0,0), UI_Color, cv2.FILLED)
                    cv2.putText(img, text, text_position, font, scale, (255,255,255), thickness)
                timestamps.append(int(timestamp))
                shoulder_timestamps.append(int(shoulder_timestamp))
                #Left Arm
                # detector.findAngle(img, 11, 13, 15)
                per = np.interp(angle, (60, 160), (100,0))
                bar = np.interp(angle, (60, 160), (100, 700))

                color = (0, int(255 * (per / 100)), int(255 * (1 - per / 100)))  # Gradual color change from red to green

                if per == 100:
                    color = (0, 255, 0)
                    if dir == 0:
                        count += 0.5
                        dir = 1
                if per == 0:
                    color = (0, 0, 255)
                    if dir == 1:
                        count += 0.5
                        dir = 0
            timestamps = list(set(timestamps))
            shoulder_timestamps = list(set(shoulder_timestamps))
            cTime = time.time()
            fps = 1/(cTime -pTime)
            pTime = cTime


            canvas = np.zeros((frame_height, frame_width + ui_width, 3), dtype=np.uint8)

            # Overlay background image onto canvas
            canvas[:, :frame_width] = img
            # Draw the bar on the right side of the canvas
            cv2.rectangle(canvas, (frame_width, 100), (frame_width + 170, 0), color, cv2.FILLED)
            cv2.rectangle(canvas, (frame_width, int(bar)), (frame_width + 170, frame_height), color, cv2.FILLED)
            cv2.putText(canvas, f'{int(per)}%', (frame_width + 60, int(bar) - 10), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

            # Draw Rep Count on the right side of the canvas
            cv2.putText(canvas, f'Reps: {int(count)}', (frame_width + 20, 45), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)


            out.write(canvas)
        
        cap.release()
        out.release()
        
        # Set the output file
        self.output_file = output_file
 
        self.performanceFile =  hip_instability(timestamps, img)
        self.secPerformanceFile = legStraight(shoulder_timestamps, img)

    
    def bencHTricepDips(self, filename_input):
        # r is used because windows automatically puts backslashes when copying path, but we need forward slashes in python
        cap = cv2.VideoCapture(f"uploads/{filename_input}")

        detector = pm.poseDetector()
        count = 0
        dir = 0
        pTime = 0
        camera_warning_shown = False
        ui_width = 170
        lineColor = (0,255,0)
        kneeBend = False
        counted = False
        start_time = time.time()
        timestamps = []
        timestamp = None

        output_file = 'outputs/output_video.mp4'
        file_exists = os.path.exists(output_file)
        counting = 1

        while file_exists:
            filename, extension = os.path.splitext(output_file)
            output_file = f"{filename}{counting}{extension}"
            counting += 1
            file_exists = os.path.exists(output_file)
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_file, fourcc, fps, (frame_width + 170, frame_height))


        while True:
            success, img = cap.read()
            if not success:
                break
            # img = cv2.imread("test.jpg")
            # img.resize((1280, 720))
            # img_resized = resize_image(img, width=800)  # Resize the frame
            img = detector.findPose(img, False)
            lmList = detector.findPosition(img, False)
            if len(lmList) != 0:
                #Right Arm 74 Being minimum and 159 being maximum
                angle = detector.findAngle(img, 12, 14, 16,)
                kneeAngle = detector.findAngle(img, 24, 26, 28, lineColor=lineColor)
                #Left Arm
                # angle = detector.findAngle(img, 11, 13, 15)
                per = np.interp(angle, (90, 159), (100,0))
                bar = np.interp(angle, (90, 159), (100, 650))
                #print(per)

                if kneeAngle > 200 or kneeAngle < 170:
                    frame_height, frame_width = img.shape[:2]
                    lineColor = (0,0,255)
                    text = "KEEP YOUR LEGS STRAIGHT"
                    position = (20, 60)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    scale = 1
                    UI_Color = (0, 0, 0)
                    thickness = 2
                    text_position = put_text_in_frame(img, text, position, font, scale, (0,0,255), thickness)
                    overlay = img.copy()
                    alpha = 0.5  # Adjust opacity here
                    cv2.rectangle(overlay, (frame_width, 100), (0, 0), UI_Color, cv2.FILLED)
                    # cv2.rectangle(overlay, (int(bar), 100), (0, 0), (255,255,255), cv2.FILLED)
                    img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

                    # Get the correct position to ensure text is within the frame
                    
                    cv2.rectangle(overlay, (frame_width,100), (0,0), UI_Color, cv2.FILLED)
                    cv2.putText(img, text, text_position, font, scale, (255,255,255), thickness)
                    kneeBend = True
                    if counted == True:
                        kneeBend = False
                        counted = False
                    if kneeBend == True:
                        end_time = time.time()
                        timestamp = end_time - start_time
                        counted = True
                else:
                    frame_height, frame_width = img.shape[:2]
                    lineColor = (0,255,0)
                    text = "PROMPTS WILL SHOW HERE"
                    position = (20, 60)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    scale = 1
                    UI_Color = (0, 0, 0)
                    thickness = 2
                    text_position = put_text_in_frame(img, text, position, font, scale, (0,0,255), thickness)
                    overlay = img.copy()
                    alpha = 0.5  # Adjust opacity here
                    cv2.rectangle(overlay, (frame_width, 100), (0, 0), UI_Color, cv2.FILLED)
                    # cv2.rectangle(overlay, (int(bar), 100), (0, 0), (255,255,255), cv2.FILLED)
                    img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

                    # Get the correct position to ensure text is within the frame
                    
                    cv2.rectangle(overlay, (frame_width,100), (0,0), UI_Color, cv2.FILLED)
                    cv2.putText(img, text, text_position, font, scale, (255,255,255), thickness)
                timestamps.append(int(timestamp))
                
                # Check for the dumbbell curls
                color = (0,255,0)
                if per == 100:
                    color = (0,0,255)
                    if dir ==0:
                        count += 0.5
                        dir = 1
                if per == 0:
                    color = (0,255,0)
                    if dir == 1:
                        count += 0.5
                        dir = 0

                if len(lmList) < 2 and not camera_warning_shown:
                    cv2.putText(img, "Adjust camera position!", (250, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    camera_warning_shown = True

            timestamps = list(set(timestamps))
            color = (0, int(255 * (per / 100)), int(255 * (1 - per / 100)))  # Gradual color change from red to green        
            cTime = time.time()
            fps = 1/(cTime -pTime)
            pTime = cTime
            #cv2.putText(img, f'{fps}', (50, 100), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)
            canvas = np.zeros((frame_height, frame_width + ui_width, 3), dtype=np.uint8)

            # Overlay background image onto canvas
            canvas[:, :frame_width] = img
            # Draw the bar on the right side of the canvas
            cv2.rectangle(canvas, (frame_width, 100), (frame_width + 170, 0), color, cv2.FILLED)
            cv2.rectangle(canvas, (frame_width, int(bar)), (frame_width + 170, frame_height), color, cv2.FILLED)
            cv2.putText(canvas, f'{int(per)}%', (frame_width + 60, int(bar) - 10), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

            # Draw Rep Count on the right side of the canvas
            cv2.putText(canvas, f'Reps: {int(count)}', (frame_width + 20, 45), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)


            out.write(canvas)
        
        cap.release()
        out.release()
        cv2.destroyAllWindows()
        
        # Set the output file
        self.output_file = output_file
        check = 0
        
        self.performanceFile =  legStraight(timestamps, img)

    def tricepropepushdown(self, filename_input):
        # r is used because windows automatically puts backslashes when copying path, but we need forward slashes in python
        cap = cv2.VideoCapture(f"uploads/{filename_input}")

        detector = pm.poseDetector()
        count = 0
        dir = 0
        pTime = 0
        camera_warning_shown = False
        timestamps = []
        shoulder_unstable = False
        start_time = time.time()
        counted = False
        timestamp = 0
        ui_width = 170
        lineColor = (0,255,0)
        shoulder_counted = False

        output_file = 'outputs/output_video.mp4'
        file_exists = os.path.exists(output_file)
        counting = 1

        while file_exists:
            filename, extension = os.path.splitext(output_file)
            output_file = f"{filename}{counting}{extension}"
            counting += 1
            file_exists = os.path.exists(output_file)
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_file, fourcc, fps, (frame_width + 170, frame_height))

        while True:
            success, img = cap.read()
            if not success:
                break
            # img = cv2.imread("test.jpg")
            # img_resized = resize_image(img, width=800)  # Resize the frame
            img = detector.findPose(img, False)
            lmList = detector.findPosition(img, False)
            if len(lmList) != 0:
                #Right Arm 74 Being minimum and 159 being maximum
                angle = detector.findAngle(img, 11,13,15)
                shoulder_angle = detector.findAngle(img, 13, 11, 23, lineColor=lineColor)
                #Left Arm
                # angle = detector.findAngle(img, 11, 13, 15)
                per = np.interp(angle, (190, 260), (100,0))
                bar = np.interp(angle, (190, 260), (100, 650))
                #print(per)
                color = (0, int(255 * (per / 100)), int(255 * (1 - per / 100)))
                # Check for the exercise
                color = (0,255,0)
                if per == 100:
                    color = (0,0,255)
                    if dir ==0:
                        count += 0.5
                        dir = 1
                if per == 0:
                    color = (0,255,0)
                    if dir == 1:
                        count += 0.5
                        dir = 0
                if shoulder_angle > 350:
                    frame_height, frame_width = img.shape[:2]
                    lineColor = (0,0,255)
                    text = "RAISE YOUR SHOULDER"
                    position = (20, 60)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    scale = 1
                    UI_Color = (0, 0, 0)
                    thickness = 2
                    text_position = put_text_in_frame(img, text, position, font, scale, (0,0,255), thickness)
                    overlay = img.copy()
                    alpha = 0.5  # Adjust opacity here
                    cv2.rectangle(overlay, (frame_width, 100), (0, 0), UI_Color, cv2.FILLED)
                    # cv2.rectangle(overlay, (int(bar), 100), (0, 0), (255,255,255), cv2.FILLED)
                    img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

                    # Get the correct position to ensure text is within the frame
                    
                    cv2.rectangle(overlay, (frame_width,100), (0,0), UI_Color, cv2.FILLED)
                    cv2.putText(img, text, text_position, font, scale, (255,255,255), thickness)
                    shoulder_unstable = True
                    if shoulder_counted == True:
                        shoulder_unstable = False
                        shoulder_counted = False
                    if shoulder_unstable == True:
                        end_time = time.time()
                        timestamp = end_time - start_time
                        shoulder_counted = True

                if shoulder_angle < 310:
                    frame_height, frame_width = img.shape[:2]
                    lineColor = (0,0,255)
                    text = "LOWER YOUR SHOULDE"
                    position = (20, 60)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    scale = 1
                    UI_Color = (0, 0, 0)
                    thickness = 2
                    text_position = put_text_in_frame(img, text, position, font, scale, (0,0,255), thickness)
                    overlay = img.copy()
                    alpha = 0.5  # Adjust opacity here
                    cv2.rectangle(overlay, (frame_width, 100), (0, 0), UI_Color, cv2.FILLED)
                    # cv2.rectangle(overlay, (int(bar), 100), (0, 0), (255,255,255), cv2.FILLED)
                    img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

                    # Get the correct position to ensure text is within the frame
                    
                    cv2.rectangle(overlay, (frame_width,100), (0,0), UI_Color, cv2.FILLED)
                    cv2.putText(img, text, text_position, font, scale, (255,255,255), thickness)
                    backBend = True
                    if counted == True:
                        backBend = False
                        counted = False
                    if backBend == True:
                        end_time = time.time()
                        timestamp = end_time - start_time
                        counted = True
                else:
                    frame_height, frame_width = img.shape[:2]
                    lineColor = (0,255,0)
                    text = "PROMPTS WILL SHOW HERE"
                    position = (20, 60)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    scale = 1
                    UI_Color = (0, 0, 0)
                    thickness = 2
                    text_position = put_text_in_frame(img, text, position, font, scale, (0,0,255), thickness)
                    overlay = img.copy()
                    alpha = 0.7  # Adjust opacity here
                    cv2.rectangle(overlay, (frame_width, 100), (0, 0), UI_Color, cv2.FILLED)
                    # cv2.rectangle(overlay, (int(bar), 100), (0, 0), (255,255,255), cv2.FILLED)
                    img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

                    # Get the correct position to ensure text is within the frame
                    
                    cv2.rectangle(overlay, (frame_width,100), (0,0), UI_Color, cv2.FILLED)
                    cv2.putText(img, text, text_position, font, scale, (255,255,255), thickness)


                if len(lmList) < 2 and not camera_warning_shown:
                    frame_height, frame_width = img.shape[:2]
                    lineColor = (0,0,255)
                    text = "ADJUST CAMERA POSITION"
                    position = (20, 60)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    scale = 1
                    UI_Color = (0, 0, 0)
                    thickness = 2
                    text_position = put_text_in_frame(img, text, position, font, scale, (0,0,255), thickness)
                    overlay = img.copy()
                    alpha = 0.5  # Adjust opacity here
                    cv2.rectangle(overlay, (frame_width, 100), (0, 0), UI_Color, cv2.FILLED)
                    # cv2.rectangle(overlay, (int(bar), 100), (0, 0), (255,255,255), cv2.FILLED)
                    img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

                    # Get the correct position to ensure text is within the frame
                    
                    cv2.rectangle(overlay, (frame_width,100), (0,0), UI_Color, cv2.FILLED)
                    cv2.putText(img, text, text_position, font, scale, (255,255,255), thickness)

                timestamps.append(int(timestamp))

            timestamps = list(set(timestamps))        
            cTime = time.time()
            fps = 1/(cTime -pTime)
            pTime = cTime
            #cv2.putText(img, f'{fps}', (50, 100), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)
            
            canvas = np.zeros((frame_height, frame_width + ui_width, 3), dtype=np.uint8)
            color = (0, int(255 * (per / 100)), int(255 * (1 - per / 100)))
            # Overlay background image onto canvas
            canvas[:, :frame_width] = img
            # Draw the bar on the right side of the canvas
            cv2.rectangle(canvas, (frame_width, 100), (frame_width + 170, 0), color, cv2.FILLED)
            cv2.rectangle(canvas, (frame_width, int(bar)), (frame_width + 170, frame_height), color, cv2.FILLED)
            cv2.putText(canvas, f'{int(per)}%', (frame_width + 60, int(bar) - 10), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

            # Draw Rep Count on the right side of the canvas
            cv2.putText(canvas, f'Reps: {int(count)}', (frame_width + 20, 45), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
            out.write(canvas)

        cap.release()
        out.release()
        cv2.destroyAllWindows()
        self.output_file = output_file     
        self.performanceFile =  legStraight(timestamps, img)
    
    def cableRows(self, filename_input):
        # r is used because windows automatically puts backslashes when copying path, but we need forward slashes in python
        cap = cv2.VideoCapture(f"uploads/{filename_input}")

        detector = pm.poseDetector()
        count = 0
        dir = 0
        pTime = 0
        camera_warning_shown = False
        timestamps = []
        backBend = False
        shoulder_backBend = False
        start_time = time.time()
        counted = False
        timestamp = 0
        shoulder_timestamp = 0
        shoulder_timestamps = []
        shoulder_counted = False
        ui_width = 170
        lineColor = (0,255,0)

        output_file = 'outputs/output_video.mp4'
        file_exists = os.path.exists(output_file)
        counting = 1

        while file_exists:
            filename, extension = os.path.splitext(output_file)
            output_file = f"{filename}{counting}{extension}"
            counting += 1
            file_exists = os.path.exists(output_file)
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_file, fourcc, fps, (frame_width + 170, frame_height))

        while True:
            success, img = cap.read()
            if not success:
                break
            # img = cv2.imread("test.jpg")
            img = detector.findPose(img, False)
            lmList = detector.findPosition(img, False)
            shoulderDistance = detector.findDistance(img, 11, 15, lineColor=lineColor)
            if len(lmList) != 0:
                #Right Arm 74 Being minimum and 159 being maximum
                angle = detector.findAngle(img, 11,13,15)
                hipangle = detector.findAngle(img, 25, 23, 11)

                #Left Arm
                # angle = detector.findAngle(img, 11, 13, 15)
                per = np.interp(angle, (205, 265), (0,100))
                bar = np.interp(angle, (205, 265), (650, 100))
                #print(per)
                if hipangle < 80:
                    frame_height, frame_width = img.shape[:2]
                    text = "DO NOT LEAN THAT FORWARD"
                    position = (20, 60)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    scale = 1
                    UI_Color = (0, 0, 0)
                    thickness = 2
                    text_position = put_text_in_frame(img, text, position, font, scale, (0,0,255), thickness)
                    overlay = img.copy()
                    alpha = 0.5  # Adjust opacity here
                    cv2.rectangle(overlay, (frame_width, 100), (0, 0), UI_Color, cv2.FILLED)
                    # cv2.rectangle(overlay, (int(bar), 100), (0, 0), (255,255,255), cv2.FILLED)
                    img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

                    # Get the correct position to ensure text is within the frame
                    
                    cv2.rectangle(overlay, (frame_width,100), (0,0), UI_Color, cv2.FILLED)
                    cv2.putText(img, text, text_position, font, scale, (255,255,255), thickness)
                    shoulder_backBend = True
                    if shoulder_counted == True:
                        shoulder_backBend = False
                        shoulder_counted = False
                    if shoulder_backBend == True:
                        shoudler_end_time = time.time()
                        shoulder_timestamp = shoudler_end_time - start_time
                        shoulder_counted = True
                if shoulderDistance < 95:
                    frame_height, frame_width = img.shape[:2]
                    lineColor = (0,0,255)
                    text = "LOWER YOUR HANDS"
                    position = (20, 60)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    scale = 1
                    UI_Color = (0, 0, 0)
                    thickness = 2
                    text_position = put_text_in_frame(img, text, position, font, scale, (0,0,255), thickness)
                    overlay = img.copy()
                    alpha = 0.5  # Adjust opacity here
                    cv2.rectangle(overlay, (frame_width, 100), (0, 0), UI_Color, cv2.FILLED)
                    # cv2.rectangle(overlay, (int(bar), 100), (0, 0), (255,255,255), cv2.FILLED)
                    img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

                    # Get the correct position to ensure text is within the frame
                    
                    cv2.rectangle(overlay, (frame_width,100), (0,0), UI_Color, cv2.FILLED)
                    cv2.putText(img, text, text_position, font, scale, (255,255,255), thickness)
                    backBend = True
                    if counted == True:
                        backBend = False
                        counted = False
                    if backBend == True:
                        end_time = time.time()
                        timestamp = end_time - start_time
                        counted = True
                else:
                    frame_height, frame_width = img.shape[:2]
                    lineColor = (0,255,0)
                    text = "PROMPTS WILL SHOW HERE"
                    position = (20, 60)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    scale = 1
                    UI_Color = (0, 0, 0)
                    thickness = 2
                    text_position = put_text_in_frame(img, text, position, font, scale, (0,0,255), thickness)
                    overlay = img.copy()
                    alpha = 0.7  # Adjust opacity here
                    cv2.rectangle(overlay, (frame_width, 100), (0, 0), UI_Color, cv2.FILLED)
                    # cv2.rectangle(overlay, (int(bar), 100), (0, 0), (255,255,255), cv2.FILLED)
                    img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

                    # Get the correct position to ensure text is within the frame
                    
                    cv2.rectangle(overlay, (frame_width,100), (0,0), UI_Color, cv2.FILLED)
                    cv2.putText(img, text, text_position, font, scale, (255,255,255), thickness)
                # Check for the exercise
                color = (0, int(255 * (per / 100)), int(255 * (1 - per / 100)))  # Gradual color change from red to green
                if per == 100:
                    color = (0,255,0)
                    if dir ==0:
                        count += 0.5
                        dir = 1
                if per == 0:
                    color = (0,0,255)
                    if dir == 1:
                        count += 0.5
                        dir = 0

                if len(lmList) < 2 and not camera_warning_shown:
                    frame_height, frame_width = img.shape[:2]
                    text = "BODY IS NOT VISIBLE"
                    position = (250, 250)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    scale = 1
                    color = (0, 0, 255)
                    thickness = 2

                    # Get the correct position to ensure text is within the frame
                    text_position = put_text_in_frame(img, text, position, font, scale, color, thickness)
                    cv2.putText(img, text, text_position, font, scale, color, thickness)
                    camera_warning_shown = True

                timestamps.append(int(timestamp))
                shoulder_timestamps.append(int(shoulder_timestamp))

            timestamps = list(set(timestamps))  
            shoulder_timestamps = list(set(shoulder_timestamps))
                    
            cTime = time.time()
            fps = 1/(cTime -pTime)
            pTime = cTime
            #cv2.putText(img, f'{fps}', (50, 100), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)
            
            canvas = np.zeros((frame_height, frame_width + ui_width, 3), dtype=np.uint8)

            # Overlay background image onto canvas
            canvas[:, :frame_width] = img
            # Draw the bar on the right side of the canvas
            cv2.rectangle(canvas, (frame_width, 100), (frame_width + 170, 0), color, cv2.FILLED)
            cv2.rectangle(canvas, (frame_width, int(bar)), (frame_width + 170, frame_height), color, cv2.FILLED)
            cv2.putText(canvas, f'{int(per)}%', (frame_width + 60, int(bar) - 10), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

            # Draw Rep Count on the right side of the canvas
            cv2.putText(canvas, f'Reps: {int(count)}', (frame_width + 20, 45), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)


            out.write(canvas)
        
        cap.release()
        out.release()
        cv2.destroyAllWindows()
        self.output_file = output_file     
        self.performanceFile =  legStraight(timestamps, img)
        self.secPerformanceFile = hip_instability(shoulder_timestamps, img)
    
    def tBarRows(self, filename_input):
        # For Importing Video {Devansh}
        cap = cv2.VideoCapture(f"uploads/{filename_input}")

        detector = pm.poseDetector()
        count = 0
        dir = 0
        pTime = 0
        backBend = False
        start_time = time.time()
        counted = False
        ui_width = 170
        lineColor = (0,255,0)
        timestamp=0
        timestamps=[]
        shoulder_backBend = False
        shoulder_timestamp = 0
        shoulder_timestamps = []
        shoulder_counted = False


        output_file = 'outputs/output_video.mp4'
        file_exists = os.path.exists(output_file)
        counting = 1

        while file_exists:
            filename, extension = os.path.splitext(output_file)
            output_file = f"{filename}{counting}{extension}"
            counting += 1
            file_exists = os.path.exists(output_file)
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_file, fourcc, fps, (frame_width + 170, frame_height))


        while True:
            success, img = cap.read()
            if not success:
                break
            # img_resized = resize_image(img, width=800)  # Resize the frame
            img = detector.findPose(img, False)
            lmList = detector.findPosition(img, False)
            
            if len(lmList) == 0:
                    frame_height, frame_width = img.shape[:2]
                    lineColor = (0,0,255)
                    text = "BODY IS NOT VISIBLE"
                    position = (250, 250)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    scale = 1
                    color = (0, 0, 255)
                    thickness = 2

                    # Get the correct position to ensure text is within the frame
                    text_position = put_text_in_frame(img, text, position, font, scale, color, thickness)
                    cv2.putText(img, text, text_position, font, scale, color, thickness)
                    camera_warning_shown = True

            if len(lmList) != 0:
                # #Right Arm
                angle = detector.findAngle(img, 11, 13, 15)
                knee_angle = detector.findAngle(img, 25, 23,11, lineColor=lineColor)
                if knee_angle > 105 or knee_angle < 65:
                    frame_height, frame_width = img.shape[:2]
                    text = "PLEASE KEEP YOUR HIPS AND BACK STABLE"
                    lineColor = (0,0,255)
                    position = (20, 60)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    scale = 1
                    UI_Color = (0, 0, 0)
                    thickness = 2
                    text_position = put_text_in_frame(img, text, position, font, scale, (0,0,255), thickness)
                    overlay = img.copy()
                    alpha = 0.5  # Adjust opacity here
                    cv2.rectangle(overlay, (frame_width, 100), (0, 0), UI_Color, cv2.FILLED)
                    # cv2.rectangle(overlay, (int(bar), 100), (0, 0), (255,255,255), cv2.FILLED)
                    img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

                    # Get the correct position to ensure text is within the frame
                    
                    cv2.rectangle(overlay, (frame_width,100), (0,0), UI_Color, cv2.FILLED)
                    cv2.putText(img, text, text_position, font, scale, (255,255,255), thickness)
                    shoulder_backBend = True
                    if shoulder_counted == True:
                        shoulder_backBend = False
                        shoulder_counted = False
                    if shoulder_backBend == True:
                        shoudler_end_time = time.time()
                        shoulder_timestamp = shoudler_end_time - start_time
                        shoulder_counted = True


                # Calculate backbend angle
                backbend_angle = calculate_backbend_angle(lmList)
                
                # Visualize backbend angle on image
                # cv2.putText(img, f'Backbend Angle: {backbend_angle}', (20, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
                
                # Check if backbend angle is more than 60 degrees
                if backbend_angle > 55:
                    frame_height, frame_width = img.shape[:2]
                    lineColor = (0,0,255)
                    # Show "backbend" prompt
                    text = "YOUR BACK IS BENDING"
                    position = (20, 60)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    scale = 1
                    UI_Color = (0, 0, 0)
                    thickness = 2
                    text_position = put_text_in_frame(img, text, position, font, scale, (0,0,255), thickness)
                    overlay = img.copy()
                    alpha = 0.5  # Adjust opacity here
                    cv2.rectangle(overlay, (frame_width, 100), (0, 0), UI_Color, cv2.FILLED)
                    # cv2.rectangle(overlay, (int(bar), 100), (0, 0), (255,255,255), cv2.FILLED)
                    img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

                    # Get the correct position to ensure text is within the frame
                    
                    cv2.rectangle(overlay, (frame_width,100), (0,0), UI_Color, cv2.FILLED)
                    cv2.putText(img, text, text_position, font, scale, (255,255,255), thickness)
                    camera_warning_shown = True
                    backBend = True
                    if counted == True:
                        backBend = False
                        counted = False
                    if backBend == True:
                        end_time = time.time()
                        timestamp = end_time - start_time
                        counted = True
                else:
                    frame_height, frame_width = img.shape[:2]
                    lineColor = (0,255,0)
                    text = "PROMPTS WILL SHOW HERE"
                    position = (20, 60)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    scale = 1
                    UI_Color = (0, 0, 0)
                    thickness = 2
                    text_position = put_text_in_frame(img, text, position, font, scale, (0,0,255), thickness)
                    overlay = img.copy()
                    alpha = 0.7  # Adjust opacity here
                    cv2.rectangle(overlay, (frame_width, 100), (0, 0), UI_Color, cv2.FILLED)
                    # cv2.rectangle(overlay, (int(bar), 100), (0, 0), (255,255,255), cv2.FILLED)
                    img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

                    # Get the correct position to ensure text is within the frame
                    
                    cv2.rectangle(overlay, (frame_width,100), (0,0), UI_Color, cv2.FILLED)
                    cv2.putText(img, text, text_position, font, scale, (255,255,255), thickness)
                timestamps.append(int(timestamp))
                shoulder_timestamps.append(int(shoulder_timestamp))

                #Left Arm
                # detector.findAngle(img, 11, 13, 15)
                per = np.interp(angle, (200, 270), (0,100))
                bar = np.interp(angle, (200, 270), (650, 100))
                #print(per)
                color = (0, int(255 * (per / 100)), int(255 * (1 - per / 100))) 
                # Check for the dumbbell curls
                if per == 100:
                    color = (0,255,0)
                    if dir ==0:
                        count += 0.5
                        dir = 1
                if per == 0:
                    color = (0,0,255)
                    if dir == 1:
                        count += 0.5
                        dir = 0
            timestamps = list(set(timestamps))
            shoulder_timestamps = list(set(shoulder_timestamps))
            # Display FPS
            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime
            # cv2.putText(img, f'FPS: {int(fps)}', (20, 150), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

            canvas = np.zeros((frame_height, frame_width + ui_width, 3), dtype=np.uint8)

            # Overlay background image onto canvas
            canvas[:, :frame_width] = img
            # Draw the bar on the right side of the canvas
            cv2.rectangle(canvas, (frame_width, 100), (frame_width + 170, 0), color, cv2.FILLED)
            cv2.rectangle(canvas, (frame_width, int(bar)), (frame_width + 170, frame_height), color, cv2.FILLED)
            cv2.putText(canvas, f'{int(per)}%', (frame_width + 60, int(bar) - 10), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

            # Draw Rep Count on the right side of the canvas
            cv2.putText(canvas, f'Reps: {int(count)}', (frame_width + 20, 45), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

            out.write(canvas)
        
        cap.release()
        out.release()
        cv2.destroyAllWindows()
        self.output_file = output_file   
        self.performanceFile = hip_instability(timestamps, img)
        self.secPerformanceFile = legStraight(shoulder_timestamps, img)
        
    def dumbbellRows(self, filename_input):
        # For Importing Video {Devansh}
        start_time = time.time()
        cap = cv2.VideoCapture(f"uploads/{filename_input}")
        forwardbend = False
        end_time = 0
        end_time_backward = 0
        backward_bend_elapsed = 0
        detector = pm.poseDetector()
        count = 0
        dir = 0
        pTime = 0
        new_arr = []
        knee_angle_count = 0  # Initialize a variable to count knee angle occurrences
        counted = False
        backwardcounted = False
        backwardbendcount = 0
        backwardbendarr = []
        timestamp = 0
        timestamps=[]
        ui_width = 170
        lineColor = (0,255,0)
        shoulder_backBend = False
        shoulder_counted = 0
        shoulder_timestamp = 0 
        shoulder_timestamps = []

        output_file = 'outputs/output_video.mp4'
        file_exists = os.path.exists(output_file)
        counting = 1

        while file_exists:
            filename, extension = os.path.splitext(output_file)
            output_file = f"{filename}{counting}{extension}"
            counting += 1
            file_exists = os.path.exists(output_file)
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_file, fourcc, fps, (frame_width + 170, frame_height))



        while True:
            success, img = cap.read()
            if not success:
                break
            img = detector.findPose(img, False)
            lmList = detector.findPosition(img, False)

            if len(lmList) == 0:
                cv2.putText(img, 'Body is not correctly visible', (20, 300), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
                

            if len(lmList) != 0:
                angle = detector.findAngle(img, 12, 14, 16)
                knee_angle = detector.findAngle(img, 12, 24, 26)
                distance_elbow_hips = detector.findDistance(img, 14, 12)
                if distance_elbow_hips < 85:
                    frame_height, frame_width = img.shape[:2]
                    text = "MOVE YOUR HAND TOWARDS YOUR HIP"
                    #position = (250, 500)
                    position = (20, 60)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    scale = 1
                    UI_Color = (0, 0, 0)
                    thickness = 2
                    text_position = put_text_in_frame(img, text, position, font, scale, (0,0,255), thickness)
                    overlay = img.copy()
                    alpha = 0.5  # Adjust opacity here
                    cv2.rectangle(overlay, (frame_width, 100), (0, 0), UI_Color, cv2.FILLED)
                    # cv2.rectangle(overlay, (int(bar), 100), (0, 0), (255,255,255), cv2.FILLED)
                    img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

                    # Get the correct position to ensure text is within the frame
                    
                    cv2.rectangle(overlay, (frame_width,100), (0,0), UI_Color, cv2.FILLED)
                    cv2.putText(img, text, text_position, font, scale, (255,255,255), thickness)
                    camera_warning_shown = True
                    shoulder_backBend = True
                    if shoulder_counted == True:
                        shoulder_backBend = False
                        shoulder_counted = False
                    if shoulder_backBend == True:
                        shoudler_end_time = time.time()
                        shoulder_timestamp = shoudler_end_time - start_time
                        shoulder_counted = True

                
                if knee_angle > 120:
                    frame_height, frame_width = img.shape[:2]
                    text = "LEAN FORWARD"
                    #position = (250, 500)
                    position = (20, 60)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    scale = 1
                    UI_Color = (0, 0, 0)
                    thickness = 2
                    text_position = put_text_in_frame(img, text, position, font, scale, (0,0,255), thickness)
                    overlay = img.copy()
                    alpha = 0.5  # Adjust opacity here
                    cv2.rectangle(overlay, (frame_width, 100), (0, 0), UI_Color, cv2.FILLED)
                    # cv2.rectangle(overlay, (int(bar), 100), (0, 0), (255,255,255), cv2.FILLED)
                    img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

                    # Get the correct position to ensure text is within the frame
                    
                    cv2.rectangle(overlay, (frame_width,100), (0,0), UI_Color, cv2.FILLED)
                    cv2.putText(img, text, text_position, font, scale, (255,255,255), thickness)
                    camera_warning_shown = True
                    forwardbend = True
                    if counted == True:
                        forwardbend = False                
                    if forwardbend == True:
                        knee_angle_count += 1  # Increment the count when knee angle is greater than 90
                        end_time = time.time()
                        timestamp = end_time - start_time
                        counted = True


                if knee_angle < 100 and knee_angle > 50:
                    counted = False
                    backwardcounted = False
            
                elif knee_angle < 50:
                    frame_height, frame_width = img.shape[:2]
                    text = "LEAN BACKWARD"
                    position = (20, 60)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    scale = 1
                    UI_Color = (0, 0, 0)
                    thickness = 2
                    text_position = put_text_in_frame(img, text, position, font, scale, (0,0,255), thickness)
                    overlay = img.copy()
                    alpha = 0.5  # Adjust opacity here
                    cv2.rectangle(overlay, (frame_width, 100), (0, 0), UI_Color, cv2.FILLED)
                    # cv2.rectangle(overlay, (int(bar), 100), (0, 0), (255,255,255), cv2.FILLED)
                    img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

                    # Get the correct position to ensure text is within the frame
                    
                    cv2.rectangle(overlay, (frame_width,100), (0,0), UI_Color, cv2.FILLED)
                    cv2.putText(img, text, text_position, font, scale, (255,255,255), thickness)
                    camera_warning_shown = True
                    backwardbend = True
                    if backwardcounted == True:
                        backwardbend = False                
                    if backwardbend == True:
                        backwardbendcount += 1  # Increment the count when knee angle is greater than 90
                        end_time = time.time()
                        backwardcounted = True
                        timestamp = end_time - start_time

                backbend_angle = calculate_backbend_angle(lmList)
                
                if backbend_angle > 70:
                    frame_height, frame_width = img.shape[:2]
                    text = "YOUR BACK IS BENDING"
                    position = (20, 60)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    scale = 1
                    UI_Color = (0, 0, 0)
                    thickness = 2
                    text_position = put_text_in_frame(img, text, position, font, scale, (0,0,255), thickness)
                    overlay = img.copy()
                    alpha = 0.5  # Adjust opacity here
                    cv2.rectangle(overlay, (frame_width, 100), (0, 0), UI_Color, cv2.FILLED)
                    # cv2.rectangle(overlay, (int(bar), 100), (0, 0), (255,255,255), cv2.FILLED)
                    img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

                    # Get the correct position to ensure text is within the frame
                    
                    cv2.rectangle(overlay, (frame_width,100), (0,0), UI_Color, cv2.FILLED)
                    cv2.putText(img, text, text_position, font, scale, (255,255,255), thickness)
                    camera_warning_shown = True
                    backBend = True
                    if counted == True:
                        backBend = False
                        counted = False
                    if backBend == True:
                        end_time = time.time()
                        timestamp = end_time - start_time
                        counted = True
                    else:
                        frame_height, frame_width = img.shape[:2]
                        text = "PROMPTS WILL SHOW HERE"
                        position = (20, 60)
                        font = cv2.FONT_HERSHEY_SIMPLEX
                        scale = 1
                        UI_Color = (0, 0, 0)
                        thickness = 2
                        text_position = put_text_in_frame(img, text, position, font, scale, (0,0,255), thickness)
                        overlay = img.copy()
                        alpha = 0.5  # Adjust opacity here
                        cv2.rectangle(overlay, (frame_width, 100), (0, 0), UI_Color, cv2.FILLED)
                        # cv2.rectangle(overlay, (int(bar), 100), (0, 0), (255,255,255), cv2.FILLED)
                        img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

                        # Get the correct position to ensure text is within the frame
                        
                        cv2.rectangle(overlay, (frame_width,100), (0,0), UI_Color, cv2.FILLED)
                        cv2.putText(img, text, text_position, font, scale, (255,255,255), thickness)

                timestamps.append(int(timestamp))
                shoulder_timestamps.append(int(shoulder_timestamp))

                #Left Arm
                per = np.interp(angle, (105,175 ), (100,0))
                bar = np.interp(angle, (105,175 ), (100, 650))
                color = (0, int(255 * (per / 100)), int(255 * (1 - per / 100)))  # Gradual color change from red to green

                if per == 100:
                    color = (0,255,0)
                    if dir ==0:
                        count += 0.5
                        dir = 1
                if per == 0:
                    color = (0,0,255)
                    if dir == 1:
                        count += 0.5
                        dir = 0


            shoulder_timestamps = list(set(shoulder_timestamps))
            timestamps = list(set(timestamps))        
            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime

            canvas = np.zeros((frame_height, frame_width + ui_width, 3), dtype=np.uint8)

            # Overlay background image onto canvas
            canvas[:, :frame_width] = img
            # Draw the bar on the right side of the canvas
            cv2.rectangle(canvas, (frame_width, 100), (frame_width + 170, 0), color, cv2.FILLED)
            cv2.rectangle(canvas, (frame_width, int(bar)), (frame_width + 170, frame_height), color, cv2.FILLED)
            cv2.putText(canvas, f'{int(per)}%', (frame_width + 60, int(bar) - 10), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

            # Draw Rep Count on the right side of the canvas
            cv2.putText(canvas, f'Reps: {int(count)}', (frame_width + 20, 45), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)


            out.write(canvas)
        
        cap.release()
        out.release()
        cv2.destroyAllWindows()
        self.output_file = output_file   
        self.performanceFile = hip_instability(timestamps, img)
        self.secPerformanceFile = legStraight(shoulder_timestamps, img)

    def deadlift(self, filename_input):
        # For Importing Video {Devansh}
        cap = cv2.VideoCapture(f"uploads/{filename_input}")

        detector = pm.poseDetector()
        count = 0
        dir = 0
        pTime = 0
        timestamps = []
        backBend = False
        start_time = time.time()
        counted = False
        timestamp = 0
        ui_width = 170
        lineColor = (0,255,0)
        shoulder_backBend = False
        shoulder_counted = 0
        shoulder_timestamp = 0 
        shoulder_timestamps = []

        output_file = 'outputs/output_video.mp4'
        file_exists = os.path.exists(output_file)
        counting = 1

        while file_exists:
            filename, extension = os.path.splitext(output_file)
            output_file = f"{filename}{counting}{extension}"
            counting += 1
            file_exists = os.path.exists(output_file)
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_file, fourcc, fps, (frame_width + 170, frame_height))



        while True:
            success, img = cap.read()
            if not success:
                break
            #img_resized = resize_image(img, width=800)  # Resize the frame
            img = detector.findPose(img, False)
            lmList = detector.findPosition(img, False)
            
            if len(lmList) != 0:
                # Calculate backbend angle
                backbend_angle = calculate_backbend_angle(lmList)
                angle = detector.findAngle(img, 11, 23, 25)
                kneeangle = detector.findAngle(img, 23,25,27, lineColor=lineColor)

                per = np.interp(kneeangle, (96, 180), (0,100))
                bar = np.interp(kneeangle, (96, 180), (650, 100))
                #print(per)

                # Check for the dumbbell curls
                color = (0,255,0)
                if per == 100:
                    color = (0,0,255)
                    if dir ==0:
                        count += 1
                        dir = 1
                if per == 0:
                    color = (0,255,0)
                    if dir == 1:
                        count += 0
                        dir = 0
                
                # Visualize backbend angle on image
                # cv2.putText(img, f'Backbend Angle: {backbend_angle}', (20, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
                
                # Check if backbend angle is more than 60 degrees
                if 230 < angle < 350 and per > 60:
                    frame_height, frame_width = img.shape[:2]
                    text = "LIFT YOUR BODY ALTOGETHER"
                    #position = (250, 500)
                    position = (20, 60)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    scale = 1
                    UI_Color = (0, 0, 0)
                    thickness = 2
                    text_position = put_text_in_frame(img, text, position, font, scale, (0,0,255), thickness)
                    overlay = img.copy()
                    alpha = 0.5  # Adjust opacity here
                    cv2.rectangle(overlay, (frame_width, 100), (0, 0), UI_Color, cv2.FILLED)
                    # cv2.rectangle(overlay, (int(bar), 100), (0, 0), (255,255,255), cv2.FILLED)
                    img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)
                    # Get the correct position to ensure text is within the frame

                    cv2.rectangle(overlay, (frame_width,100), (0,0), UI_Color, cv2.FILLED)
                    cv2.putText(img, text, text_position, font, scale, (255,255,255), thickness)
                    camera_warning_shown = True
                    shoulder_backBend = True
                    if shoulder_counted == True:
                        shoulder_backBend = False
                        shoulder_counted = False
                    if shoulder_backBend == True:
                        shoudler_end_time = time.time()
                        shoulder_timestamp = shoudler_end_time - start_time
                        shoulder_counted = True
                elif backbend_angle > 55:
                    frame_height, frame_width = img.shape[:2]
                    text = "KEEP YOUR BACK STRAIGHT"
                    #position = (250, 500)
                    position = (20, 60)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    scale = 1
                    UI_Color = (0, 0, 0)
                    thickness = 2
                    text_position = put_text_in_frame(img, text, position, font, scale, (0,0,255), thickness)
                    overlay = img.copy()
                    alpha = 0.5  # Adjust opacity here
                    cv2.rectangle(overlay, (frame_width, 100), (0, 0), UI_Color, cv2.FILLED)
                    # cv2.rectangle(overlay, (int(bar), 100), (0, 0), (255,255,255), cv2.FILLED)
                    img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)
                    # Get the correct position to ensure text is within the frame

                    cv2.rectangle(overlay, (frame_width,100), (0,0), UI_Color, cv2.FILLED)
                    cv2.putText(img, text, text_position, font, scale, (255,255,255), thickness)
                    backBend = True
                    if counted == True:
                        backBend = False
                        counted = False
                    if backBend == True:
                        end_time = time.time()
                        timestamp = end_time - start_time
                        counted = True
                # You can add further actions here when backbend is detected

                else:
                    frame_height, frame_width = img.shape[:2]
                    lineColor = (0,255,0)
                    text = "PROMPTS WILL SHOW HERE"
                    position = (20, 60)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    scale = 1
                    UI_Color = (0, 0, 0)
                    thickness = 2
                    text_position = put_text_in_frame(img, text, position, font, scale, (0,0,255), thickness)
                    overlay = img.copy()
                    alpha = 0.7  # Adjust opacity here
                    cv2.rectangle(overlay, (frame_width, 100), (0, 0), UI_Color, cv2.FILLED)
                    # cv2.rectangle(overlay, (int(bar), 100), (0, 0), (255,255,255), cv2.FILLED)
                    img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

                    # Get the correct position to ensure text is within the frame
                    
                    cv2.rectangle(overlay, (frame_width,100), (0,0), UI_Color, cv2.FILLED)
                    cv2.putText(img, text, text_position, font, scale, (255,255,255), thickness)
                timestamps.append(int(timestamp))
                shoulder_timestamps.append(int(shoulder_timestamp))
                    
                
                            #Right Arm 74 Being minimum and 159 being maximum
                
                #Left Arm
                # angle = detector.findAngle(img, 11, 13, 15)
                

                if len(lmList) < 2 and not camera_warning_shown:
                    text = "BODY NOT VISIBLE"
                    position = (250, 250)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    scale = 1
                    color = (0, 0, 255)
                    thickness = 2

                    # Get the correct position to ensure text is within the frame
                    text_position = put_text_in_frame(img, text, position, font, scale, color, thickness)
                    cv2.putText(img, text, text_position, font, scale, color, thickness)
                    camera_warning_shown = True

            timestamps = list(set(timestamps))
            shoulder_timestamps = list(set(shoulder_timestamps))

            color = (0, int(255 * (per / 100)), int(255 * (1 - per / 100)))  # Gradual color change from red to green
            cTime = time.time()
            fps = 1/(cTime -pTime)
            pTime = cTime



            canvas = np.zeros((frame_height, frame_width + ui_width, 3), dtype=np.uint8)

            # Overlay background image onto canvas
            canvas[:, :frame_width] = img
            # Draw the bar on the right side of the canvas
            cv2.rectangle(canvas, (frame_width, 100), (frame_width + 170, 0), color, cv2.FILLED)
            cv2.rectangle(canvas, (frame_width, int(bar)), (frame_width + 170, frame_height), color, cv2.FILLED)
            cv2.putText(canvas, f'{int(per)}%', (frame_width + 60, int(bar) - 10), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

            # Draw Rep Count on the right side of the canvas
            cv2.putText(canvas, f'Reps: {int(count)}', (frame_width + 20, 45), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)


            out.write(canvas)
        
        cap.release()
        out.release()
        cv2.destroyAllWindows()
        self.output_file = output_file   
        self.performanceFile = hip_instability(timestamps, img)
        self.secPerformanceFile = legStraight(shoulder_timestamps, img)

    






def ensure_unique_file(filename):
    if os.path.exists(f"performanceOutput/{filename}"):
        base, extension = os.path.splitext(filename)
        counter = 1
        new_filename = f"{base}{counter}{extension}"
        while os.path.exists(f"performanceOutput/{new_filename}"):
            counter += 1
            new_filename = f"{base}{counter}{extension}"
        filename = new_filename
    return filename

def hip_instability(timestamps, img):
    filename = ensure_unique_file("hip_angle_output.txt")

    with open(f"performanceOutput/{filename}", 'w') as file:
        i = 0
        while i < len(timestamps):
            file.write(f"{timestamps[i]}\n")
            i += 1
    return f"performanceOutput/{filename}"

def legStraight(timestamps, img):
    filename = ensure_unique_file("knee_straight_output.txt")

    with open(f"performanceOutput/{filename}", 'w') as file:
        i = 0
        while i < len(timestamps):
            file.write(f"{timestamps[i]}\n")
            i += 1
    return f"performanceOutput/{filename}"

def back_bend(timestamps, img):
    filename = ensure_unique_file("back_bend_output.txt")

    with open(filename, 'w') as file:
        file.write("Your back was bend at:\n")
        for i, timestamp in enumerate(timestamps):
            message = f'{time.strftime("%H:%M:%S", time.localtime(timestamp))}\n'
            cv2.putText(img, message, (50, 50 + i * 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            file.write(message)




def resize_image(image, width=None, height=None):
    # Resize the image while maintaining aspect ratio
    if width is None and height is None:
        return image
    elif width is not None and height is not None:
        raise ValueError("Only one of 'width' or 'height' should be provided.")
    
    if width is not None:
        aspect_ratio = image.shape[1] / image.shape[0]
        new_height = int(width / aspect_ratio)
        return cv2.resize(image, (width, new_height))
    else:
        aspect_ratio = image.shape[0] / image.shape[1]
        new_width = int(height / aspect_ratio)
        return cv2.resize(image, (new_width, height))

def squat_backbend(lmList):
    # Function to calculate the backbend angle
    # This function calculates the angle between the vectors representing the upper body and lower body
    
    # Indexes of relevant keypoints
    right_shoulder = lmList[14]  # Right shoulder
    right_hip = lmList[24]       # Right hip
    spine = lmList[12]           # Middle of the spine

    # Calculate the vectors representing the upper body (shoulder to spine) and the lower body (hip to spine)
    upper_body_vector = [right_shoulder[1] - spine[1], right_shoulder[2] - spine[2]]  # [y_diff, x_diff]
    lower_body_vector = [right_hip[1] - spine[1], right_hip[2] - spine[2]]                # [y_diff, x_diff]

    # Calculate the dot product of the two vectors
    dot_product = upper_body_vector[0] * lower_body_vector[0] + upper_body_vector[1] * lower_body_vector[1]

    # Calculate the magnitudes of the vectors
    upper_body_magnitude = math.sqrt(upper_body_vector[0] ** 2 + upper_body_vector[1] ** 2)
    lower_body_magnitude = math.sqrt(lower_body_vector[0] ** 2 + lower_body_vector[1] ** 2)

    # Calculate the cosine of the angle between the vectors using the dot product formula
    cos_angle = dot_product / (upper_body_magnitude * lower_body_magnitude)

    # Calculate the angle in radians using the arccosine function
    angle_rad = math.acos(cos_angle)

    # Convert the angle from radians to degrees
    angle_deg = math.degrees(angle_rad)

    return angle_deg

def calculate_backbend_angle(lmList):
    # Function to calculate the backbend angle
    # This function calculates the angle between the vectors representing the upper body and lower body
    
    # Indexes of relevant keypoints
    right_shoulder = lmList[14]  # Right shoulder
    right_hip = lmList[24]       # Right hip
    spine = lmList[12]           # Middle of the spine

    # Calculate the vectors representing the upper body (shoulder to spine) and the lower body (hip to spine)
    upper_body_vector = [right_shoulder[1] - spine[1], right_shoulder[2] - spine[2]]  # [y_diff, x_diff]
    lower_body_vector = [right_hip[1] - spine[1], right_hip[2] - spine[2]]                # [y_diff, x_diff]

    # Calculate the dot product of the two vectors
    dot_product = upper_body_vector[0] * lower_body_vector[0] + upper_body_vector[1] * lower_body_vector[1]

    # Calculate the magnitudes of the vectors
    upper_body_magnitude = math.sqrt(upper_body_vector[0] ** 2 + upper_body_vector[1] ** 2)
    lower_body_magnitude = math.sqrt(lower_body_vector[0] ** 2 + lower_body_vector[1] ** 2)

    # Calculate the cosine of the angle between the vectors using the dot product formula
    cos_angle = dot_product / (upper_body_magnitude * lower_body_magnitude)

    # Calculate the angle in radians using the arccosine function
    angle_rad = math.acos(cos_angle)

    # Convert the angle from radians to degrees
    angle_deg = math.degrees(angle_rad)

    return angle_deg

def put_text_in_frame(image, text, position, font, scale, color, thickness):
    """
    Helper function to ensure the text is within the frame.
    """
    text_size = cv2.getTextSize(text, font, scale, thickness)[0]
    # Ensure the text is within the frame
    x = max(position[0], 0)
    y = max(position[1], text_size[1])
    if x + text_size[0] > image.shape[1]:
        x = image.shape[1] - text_size[0]
    if y + text_size[1] > image.shape[0]:
        y = image.shape[0] - text_size[1]
    return (x, y)

def bicepCurls():
    cap = cv2.VideoCapture("uploads/formDetection.mp4")
    detector = pm.poseDetector()
    count = 0
    dir = 0
    pTime = 0

    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('output_video.mp4', fourcc, fps, (frame_width, frame_height))

    while True:
        success, img = cap.read()
        if not success:
            break

        # Perform pose detection
        img = detector.findPose(img, False)
        lmList = detector.findPosition(img, False)
        if len(lmList) != 0:
            angle = detector.findAngle(img, 12, 14, 16)
            per = np.interp(angle, (60, 160), (100,0))
            bar = np.interp(angle, (60, 160), (100, 650))

            color = (0,255,0)
            if per == 100:
                color = (0,0,255)
                if dir ==0:
                    count += 0.5
                    dir = 1
            if per == 0:
                color = (0,255,0)
                if dir == 1:
                    count += 0.5
                    dir = 0

            overlay = img.copy()
            alpha = 0.5  
            cv2.rectangle(overlay, (150, 150), (0, 0), color, cv2.FILLED)
            cv2.rectangle(overlay, (int(bar), 100), (0, 0), color, cv2.FILLED)
            img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

            overlay = img.copy()
            alpha = 0.5  
            cv2.rectangle(overlay, (0, 100), (120, 50), color, cv2.FILLED)
            img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

            overlay = img.copy()
            alpha = 0.5  
            cv2.putText(overlay, f'{int(per)} %', (20, 150), cv2.FONT_HERSHEY_PLAIN, 4, (255, 0, 0), 4)
            img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

            overlay = img.copy()
            alpha = 0.5  
            cv2.putText(overlay, f'{count}', (0, 100), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)
            img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

        out.write(img)
        cTime = time.time()
        fps = 1/(cTime -pTime)
        pTime = cTime
    
    cap.release()
    out.release()


def preacherCurls():
    # r is used because windows automatically puts backslashes when copying path, but we need forward slashes in python
    cap = cv2.VideoCapture("uploads/preachercurls.mp4")

    detector = pm.poseDetector()
    count = 0
    dir = 0
    pTime = 0
    camera_warning_shown = False

    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('output_video.mp4', fourcc, fps, (frame_width, frame_height))


    while True:
        success, img = cap.read()
        if not success:
            break

        # Perform pose detection
        img = detector.findPose(img, False)
        lmList = detector.findPosition(img, False)
        if len(lmList) != 0:
            #Right Arm 74 Being minimum and 159 being maximum
            angle = detector.findAngle(img, 11, 13, 15)
            #Left Arm
            #angle = detector.findAngle(img, 11, 13, 15)
            per = np.interp(angle, (220, 300), (0,100))
            bar = np.interp(angle, (220, 300), (100, 650))
            #print(per)

            # Check for the dumbbell curls
            color = (0,255,0)
            if per == 100:
                color = (0,0,255)
                if dir ==0:
                    count += 0.5
                    dir = 1
            if per == 0:
                color = (0,255,0)
                if dir == 1:
                    count += 0.5
                    dir = 0

            if len(lmList) < 2 and not camera_warning_shown:
                cv2.putText(img, "Adjust camera position!", (250, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                camera_warning_shown = True

            overlay = img.copy()
            alpha = 0.5  
            cv2.rectangle(overlay, (150, 150), (0, 0), color, cv2.FILLED)
            cv2.rectangle(overlay, (int(bar), 100), (0, 0), color, cv2.FILLED)
            img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

            overlay = img.copy()
            alpha = 0.5  
            cv2.rectangle(overlay, (0, 100), (120, 50), color, cv2.FILLED)
            img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

            overlay = img.copy()
            alpha = 0.5  
            cv2.putText(overlay, f'{int(per)} %', (20, 150), cv2.FONT_HERSHEY_PLAIN, 4, (255, 0, 0), 4)
            img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

            overlay = img.copy()
            alpha = 0.5  
            cv2.putText(overlay, f'{count}', (0, 100), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)
            img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

        out.write(img)
        cTime = time.time()
        fps = 1/(cTime -pTime)
        pTime = cTime
    
    cap.release()
    out.release()


def hammerCurls():
    # r is used because windows automatically puts backslashes when copying path, but we need forward slashes in python
    cap = cv2.VideoCapture(r"Exercise_Vids\Exercises\hammercurlvid.mp4")

    detector = pm.poseDetector()
    count = 0
    dir = 0
    pTime = 0
    camera_warning_shown = False

    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('output_video.mp4', fourcc, fps, (frame_width, frame_height))

    while True:
        success, img = cap.read()
        if not success:
            break

        # Perform pose detection
        img = detector.findPose(img, False)
        lmList = detector.findPosition(img, False)
        if len(lmList) != 0:
            #Right Arm 74 Being minimum and 159 being maximum
            angle = detector.findAngle(img, 12, 14, 16)
            #Left Arm
            # angle = detector.findAngle(img, 11, 13, 15)
            per = np.interp(angle, (60, 160), (100,0))
            bar = np.interp(angle, (60, 160), (100, 650))
            #print(per)

            # Check for the dumbbell curls
            color = (0,255,0)
            if per == 100:
                color = (0,0,255)
                if dir ==0:
                    count += 0.5
                    dir = 1
            if per == 0:
                color = (0,255,0)
                if dir == 1:
                    count += 0.5
                    dir = 0

            if len(lmList) < 2 and not camera_warning_shown:
                cv2.putText(img, "Adjust camera position!", (250, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                camera_warning_shown = True

            overlay = img.copy()
            alpha = 0.5  
            cv2.rectangle(overlay, (150, 150), (0, 0), color, cv2.FILLED)
            cv2.rectangle(overlay, (int(bar), 100), (0, 0), color, cv2.FILLED)
            img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

            overlay = img.copy()
            alpha = 0.5  
            cv2.rectangle(overlay, (0, 100), (120, 50), color, cv2.FILLED)
            img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

            overlay = img.copy()
            alpha = 0.5  
            cv2.putText(overlay, f'{int(per)} %', (20, 150), cv2.FONT_HERSHEY_PLAIN, 4, (255, 0, 0), 4)
            img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

            overlay = img.copy()
            alpha = 0.5  
            cv2.putText(overlay, f'{count}', (0, 100), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)
            img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

        out.write(img)
        cTime = time.time()
        fps = 1/(cTime -pTime)
        pTime = cTime
    
    cap.release()
    out.release()


