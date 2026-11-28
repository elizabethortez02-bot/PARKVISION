"""Una sola conexión a DroidCam, con reconexión automática."""
import cv2, os, time
class Camara:
    def __init__(self,indice): self.indice=indice; self.cap=None
    def read(self):
        if self.cap is None:
            self.cap=cv2.VideoCapture(self.indice,cv2.CAP_MSMF if os.name=='nt' else cv2.CAP_ANY)
        ok,frame=self.cap.read()
        if not ok or frame is None:
            self.close();raise RuntimeError('DroidCam desconectada; reconectando')
        return frame
    def close(self):
        if self.cap is not None:self.cap.release();self.cap=None
