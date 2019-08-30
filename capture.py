import math
import numpy as np
import cv2
import tkinter as tk
from PIL import ImageGrab, Image





if __name__ == "__main__":
    root = tk.Tk()
    width, height = math.ceil(root.winfo_screenwidth() * (2/3)), math.ceil(root.winfo_screenheight() * (2/3))
    print(width, height)
    
    while True:
        image = ImageGrab.grab()
        width, height = image.size
        img_bytes = image.tobytes()
        img_convert = Image.frombytes('RGBA', (width, height), ya)
        img = np.array(img_convert)

        #image = cv2.resize(image, (width, height))
        # cv2.namedWindow("Video", cv2.WND_PROP_FULLSCREEN)
        # cv2.setWindowProperty("Video",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
        # cv2.imshow("Video", image)
        cv2.imshow("Video", img)
        if cv2.waitKey(1) == 27:
            break

    cv2.destroyAllWindows()