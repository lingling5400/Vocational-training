import cv2
import numpy as np

def conv_filter(frame:np.ndarray):      #卷積（Convolution）
    height,width=frame.shape[:2]
    Kernel= np.array([[1/9,1/9,1/9],[1/9,1/9,1/9],[1/9,1/9,1/9]])  #用來模糊+平滑+去雜訊
    out = np.zeros_like(frame)
    for h in range(1,height-1):      #因為要抓自身數周圍的八個數來做卷積計算
        for w in range(1,width-1):   #所以這裡要用range來抓index
            T=np.array([[frame[h-1,w-1],frame[h-1,w],frame[h-1,w+1]], [frame[h,w-1],frame[h,w],frame[h,w+1]], [frame[h+1,w-1],frame[h+1,w],frame[h+1,w+1]]])
            outKernel=T*Kernel       #逐元素相乘（element-wise multiplication）
            out[h,w]=np.sum(outKernel) #把壓縮值放到相對應位置
        
    return out


cap = cv2.VideoCapture(0)
if cap.isOpened():
    ret, frame = cap.read()    
    # 依據flag狀態做影像處理
    filterflag=False
    
    while ret:
        # 處理鍵盤事件
        key = cv2.waitKey(1)

        if key == ord('b'): filterflag=not filterflag
        elif key == ord('q'): break
        
        # 轉灰階並轉為小數
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = frame.astype(float) / 255.0
        frame=conv_filter(frame)
 

        # 顯示處理後的影像
        cv2.imshow('filters', frame)
        # 讀取下一個frame
        ret, frame = cap.read()


cap.release()
cv2.destroyAllWindows()