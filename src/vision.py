"""Ocupación calibrada, estabilidad y movimiento entre imágenes."""
import cv2
from deteccion_maqueta import clasificar_espacios_maqueta, ESPACIOS
class Vision:
    def __init__(self): self.last=None;self.count=0;self.previous=None
    def reset(self): self.last=None;self.count=0;self.previous=None
    def process(self,img):
        states=clasificar_espacios_maqueta(img)
        self.count=self.count+1 if states==self.last else 1;self.last=states
        gray=cv2.GaussianBlur(cv2.cvtColor(img,cv2.COLOR_BGR2GRAY),(5,5),0)
        motion=0
        if self.previous is not None:
            delta=cv2.absdiff(gray,self.previous);motion=round(100*cv2.countNonZero(cv2.threshold(delta,25,255,cv2.THRESH_BINARY)[1])/delta.size,1)
        self.previous=gray
        return states,self.count>=2,motion
    def annotate(self,img,spaces):
        for s,(x,y,w,h) in zip(spaces,ESPACIOS):
            color=(40,40,230) if s['occupied'] else (130,130,130) if s['blocked'] else (230,130,40) if s['visit'] else (40,220,40)
            cv2.rectangle(img,(x,y),(x+w,y+h),color,2);cv2.putText(img,f"P{s['id']:02}",(x,y+20),cv2.FONT_HERSHEY_SIMPLEX,.5,color,2)
        return img