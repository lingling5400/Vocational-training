import cv2

cap = cv2.VideoCapture(0)
if cap.isOpened():
    # 設定攝影機
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    cap.set(cv2.CAP_PROP_FPS, 60)
    # 測試畫面讀取
    ret, frame = cap.read()
    if not ret:
        print('Failed to read first frame')
    else:
        # 取得畫面間隔時間
        FPS = cap.get(cv2.CAP_PROP_FPS)
        INTERVAL = int(1000 / FPS)
        WIDTH = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        HEIGHT = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        # 建立輸出影片的寫出器
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter('output.avi', fourcc, FPS, (WIDTH, HEIGHT))
        is_writing = False
        while ret == True:
            cv2.imshow('haha me', frame)
            key_pressed = cv2.waitKey(INTERVAL)
            # 檢查鍵盤按鍵
            if key_pressed == ord('q'):
                print('Q pressed')
                break
            elif key_pressed == ord(' '):
                is_writing = not is_writing
                print(f'正在錄製嗎: {is_writing}')
            # 如果正在錄影，就寫出新的frame
            if is_writing:
                out.write(frame)
            # 讀下一個frame
            ret, frame = cap.read()
        # 關閉Writer
        out.release()
else:
    print('Video not opened')

# 釋放所有視訊資源
cap.release()
cv2.destroyAllWindows()
