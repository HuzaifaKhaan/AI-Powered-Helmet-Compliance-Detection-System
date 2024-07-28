from my_functions import *
from paddleocr import PaddleOCR
import os
import mysql.connector

# Establish a connection to the MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Programmer.12",
    database="helmet_detection_db",
    port=3306
)

cursor = conn.cursor()

source = 'main2.mp4' 
save_video = True
show_video = True
save_img = True



helmet_wearer_folder = 'helmet_wearers'
non_helmet_wearer_folder = 'non_helmet_wearers'
helmet_license_plate_folder = 'helmet_license_plates'
non_helmet_license_plate_folder = 'non_helmet_license_plates'

# Create folders if they don't exist
os.makedirs(helmet_wearer_folder, exist_ok=True)
os.makedirs(non_helmet_wearer_folder, exist_ok=True)
os.makedirs(helmet_license_plate_folder, exist_ok=True)
os.makedirs(non_helmet_license_plate_folder, exist_ok=True)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, frame_size)

cap = cv2.VideoCapture(source)

while(cap.isOpened()):
    ret, frame = cap.read()
    
    if ret:
        frame = cv2.resize(frame, frame_size)
        orifinal_frame = frame.copy()
        frame, results = object_detection(frame) 

        rider_list = []
        head_list = []
        number_list = []

        for result in results:
            x1, y1, x2, y2, cnf, clas = result
            if clas == 0:
                rider_list.append(result)
            elif clas == 1:
                head_list.append(result)
            elif clas == 2:
                number_list.append(result)

        for rdr in rider_list:
            time_stamp = str(time.time())
            x1r, y1r, x2r, y2r, cnfr, clasr = rdr
            
            for hd in head_list:
                x1h, y1h, x2h, y2h, cnfh, clash = hd

                if inside_box([x1r, y1r, x2r, y2r], [x1h, y1h, x2h, y2h]): 
                    try:
                        head_img = orifinal_frame[y1h:y2h, x1h:x2h]
                        helmet_present = img_classify(head_img)
                    except:
                        helmet_present = [None, None]

                    if helmet_present[0] == True:
                        print("Helmet present True")
                        frame = cv2.rectangle(frame, (x1h, y1h), (x2h, y2h), (0, 255, 0), 1)
                        frame = cv2.putText(frame, f'{round(helmet_present[1], 1)}', (x1h, y1h + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)

                        try:
                            print("Try block")
                            cv2.imwrite(os.path.join(helmet_wearer_folder, f'{time_stamp}.jpg'), frame[y1r:y2r, x1r:x2r])

                            for num in number_list:
                                x1_num, y1_num, x2_num, y2_num, conf_num, clas_num = num

                                if inside_box([x1r, y1r, x2r, y2r], [x1_num, y1_num, x2_num, y2_num]):
                                    conf_num = num[4]
                                    print("if reached------------------------------------------------")
                                    if conf_num is not None:
                                        num_img = orifinal_frame[y1_num:y2_num, x1_num:x2_num]
                                        cv2.imwrite(os.path.join(helmet_license_plate_folder, f'{time_stamp}_{conf_num}.jpg'), num_img)

                                    try:
                                        print("TRY BLOCK FOR NUMBER")
                                        cv2.imwrite(os.path.join(helmet_wearer_folder, f'{time_stamp}.jpg'), frame[y1r:y2r, x1r:x2r])
                                        cv2.imwrite(os.path.join(helmet_license_plate_folder, f'{time_stamp}_{conf_num}.jpg'), num_img)

                                        ocr = PaddleOCR(use_angle_cls=True, lang='en')
                                        img_path = os.path.join(helmet_wearer_folder, f'{time_stamp}.jpg')
                                        result = ocr.ocr(img_path, cls=True)
                                        print(result,"-----------result---------------")

                                        for idx in range(len(result)):
                                            res = result[idx]
                                            for line in res:
                                                print(line,"_______________________line______________")
                                                HelmetRiders=(line[1][0])
                                                print(HelmetRiders,"_________________riders________________")

                                                insert_query = "INSERT INTO LicensePlate (HelmetRiders) VALUES (%s)"
                                                cursor.execute(insert_query, (HelmetRiders,))

                                                conn.commit()
                                                
                                
                                    except Exception as e:
                                        print(e)
                                        print('could not save number plate')

                        except Exception as e:
                            print(e)
                            print('could not save rider')

                    elif helmet_present[0] == None:
                        print("Helmet present None")
                        frame = cv2.rectangle(frame, (x1h, y1h), (x2h, y2h), (0, 255, 255), 1)
                        frame = cv2.putText(frame, f'{round(helmet_present[1], 1)}', (x1h, y1h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)

                    elif helmet_present[0] == False:
                        print("Helmet present False")
                        frame = cv2.rectangle(frame, (x1h, y1h), (x2h, y2h), (0, 0, 255), 1)
                        frame = cv2.putText(frame, f'{round(helmet_present[1], 1)}', (x1h, y1h + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)

                        try:
                            cv2.imwrite(os.path.join(non_helmet_wearer_folder, f'{time_stamp}.jpg'), frame[y1r:y2r, x1r:x2r])

                            for num in number_list:
                                x1_num, y1_num, x2_num, y2_num, conf_num, clas_num = num

                                if inside_box([x1r, y1r, x2r, y2r], [x1_num, y1_num, x2_num, y2_num]):
                                    conf_num = num[4]
                                    num_img = orifinal_frame[y1_num:y2_num, x1_num:x2_num]
                                    cv2.imwrite(os.path.join(non_helmet_license_plate_folder, f'{time_stamp}_{conf_num}.jpg'), num_img)

                                    try:
                                        cv2.imwrite(os.path.join(non_helmet_wearer_folder, f'{time_stamp}.jpg'), frame[y1r:y2r, x1r:x2r])
                                        cv2.imwrite(os.path.join(non_helmet_license_plate_folder, f'{time_stamp}_{conf_num}.jpg'), num_img)

                                        ocr = PaddleOCR(use_angle_cls=True, lang='en')
                                        img_path = os.path.join(non_helmet_license_plate_folder, f'{time_stamp}_{conf_num}.jpg')
                                        result = ocr.ocr(img_path, cls=True)


                                        for idx in range(len(result)):
                                            res = result[idx]
                                            for line in res:
                                                print(line,"---------------line-------------------")
                                                Non_HelmetRiders=(line[1][0])
                                                print(Non_HelmetRiders,"-------------non-helmet-riders--------------")
                                                

                                               #insert_query = "INSERT INTO LicensePlate (Non_HelmetRiders) VALUES (%s)"
                                                #cursor.execute(insert_query, (Non_HelmetRiders,))
        
      
                                                #conn.commit()
                                    except Exception as e:
                                        print(e)
                                        print('could not save number plate')

                        except Exception as e:
                            print(e)
                            print('could not save rider')

        if save_video:
            out.write(frame)

        if save_img:
            cv2.imwrite('saved_frame.jpg', frame)

        if show_video:
            frame = cv2.resize(frame, (900, 450))
            cv2.imshow('Frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    else:
        break

cap.release()
cv2.destroyAllWindows()
print('Execution completed')
