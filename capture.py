import math
import numpy as np
import cv2
import tkinter as tk
from PIL import ImageGrab





if __name__ == "__main__":
    root = tk.Tk()
    width, height = math.ceil(root.winfo_screenwidth() * (2/3)), math.ceil(root.winfo_screenheight() * (2/3))
    print(width, height)
    
    while True:
        image = ImageGrab.grab()
        image = np.array(image)
        #image = cv2.resize(image, (width, height))
        cv2.namedWindow("Video", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("Video",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
        cv2.imshow("Video", image)
        #cv2.imshow("Video", image)
        if cv2.waitKey(1) == 27:
            break

    cv2.destroyAllWindows()