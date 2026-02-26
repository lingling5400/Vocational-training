import cv2
import numpy as np

RADIUS = 5

def pad_once(frame:np.ndarray):
    height, width = frame.shape[:2]
    out = np.zeros((height+2, width+2))
    out[1:height+1, 1:width+1] = frame # 中間
    out[0, 1:width+1] = frame[0] # 上
    out[-1, 1:width+1] = frame[-1] # 下
    out[1:height+1, 0] = frame[:,0] # 左
    out[1:height+1, -1] = frame[:,-1] # 右
    # 四個角落
    out[0,0] = frame[0,0]
    out[-1,0] = frame[-1,0]
    out[0,-1] = frame[0,-1]
    out[-1,-1] = frame[-1,-1]
    return out
    
def pad(frame:np.ndarray, radius=RADIUS):
    for _ in range(radius):
        frame = pad_once(frame)
    return frame

# kernel可以是一個np.array(直接套用)
# 或者是特殊設計: tuple(方法, 尺寸) ('median', 3)
def apply_kernel(frame:np.ndarray, kernel):
    height, width = frame.shape[:2]
    if type(kernel) == tuple:
        method, kernel_size = kernel
    else:
        kernel_size = kernel.shape[0]
        method = 'base'

    out = np.zeros((height-kernel_size+1, width-kernel_size+1))
    for y in range(height-kernel_size+1):
        for x in range(width-kernel_size+1):
            _input = frame[y:y+kernel_size, x:x+kernel_size]
            if method == 'median':
                _input = np.sort(_input, axis=None)
                out[y,x] = _input[int((kernel_size**2)/2)]
            elif method == 'base':
                out[y,x] = (kernel*_input).sum()

    return out

def box_blur(frame:np.ndarray, kernel_size=RADIUS*2+1):
    kernel = np.ones((kernel_size,kernel_size)) / (kernel_size**2)
    return apply_kernel(frame, kernel)

def gaussian_blur(frame:np.ndarray, kernel_size=RADIUS*2+1):
    def pascal(level):
        if level == 0: return np.array([1])
        else:
            out = np.ones(level+1, int)
            prev = pascal(level-1)
            for i in range(level-1):
                out[i+1] = prev[i] + prev[i+1]
            return out
            
    def get_gaussian_kernel(size):
        a = np.array([pascal(size-1)]*size)
        k = a * a.T
        return(k / np.sum(k))

    return apply_kernel(frame, get_gaussian_kernel(kernel_size))


def median_blur(frame:np.ndarray, kernel_size=RADIUS*2+1): 
    return apply_kernel(frame, ('median', kernel_size))

def sobel_blur(frame:np.ndarray): #邊緣偵測
    sobel_x=np.array([[-1 , 0 , 1],[-2 , 0 , 2],[-1 , 0 , 1]])
    sobel_y=np.array([[-1 , -2 , -1],[0 , 0 , 0],[1 , 2 , 1]])
    new_frame=pad(frame)
    Gx=apply_kernel(new_frame, sobel_x)
    Gy=apply_kernel(new_frame, sobel_y)
    print(new_frame.dtype)
    return np.sqrt(Gx**2 + Gy**2)

    #return apply_kernel(frame, get_gaussian_kernel(kernel_size))
    



cap = cv2.VideoCapture('chengdu.mp4')
if cap.isOpened():
    ret, frame = cap.read()
    bbflag = False
    padflag = False
    gaussianflag = False
    medianflag = False
    sobelflag = False


    while ret:
        # 處理鍵盤事件
        key = cv2.waitKey(1)
        if key == ord('b'): bbflag = not bbflag
        elif key == ord('p'): padflag = not padflag
        elif key == ord('m'): medianflag = not medianflag
        elif key == ord('g'): gaussianflag = not gaussianflag
        elif key == ord('s'): sobelflag = not sobelflag
        elif key == ord('q'): break
        
        # 轉灰階並轉為小數
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = np.astype(frame, float) / 255.0

        # 依據flag狀態做影像處理
        if padflag: frame = pad(frame)
        if bbflag: frame = box_blur(frame)
        if gaussianflag: frame = gaussian_blur(frame)
        if medianflag: frame = median_blur(frame)
        if sobelflag: frame=sobel_blur(frame)

        # 顯示處理後的影像
        cv2.imshow('filters', frame)
        # 讀取下一個frame
        ret, frame = cap.read()


cap.release()
cv2.destroyAllWindows()