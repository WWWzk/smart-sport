import cv2
import os

class VideoSource(object):

    def __init__(self,
                 addr=None,
                 webcam=True,
                 frame_interval=1):
        self.rtsp_addr = addr
        self.video_path = addr
        self.webcam = webcam
        self.frame_interval = frame_interval

    def __iter__(self):
        if self.webcam:
            print("Using webcam ")
            self.vdo = cv2.VideoCapture(self.rtsp_addr)
            ret, frame = self.vdo.read()
            assert ret, "Error: Camera error"
            self.im_width = frame.shape[0]
            self.im_height = frame.shape[1]
        else:
            self.vdo = cv2.VideoCapture()
            assert os.path.isfile(self.video_path), "Path error"
            self.vdo.open(self.video_path)
            self.im_width = int(self.vdo.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.im_height = int(self.vdo.get(cv2.CAP_PROP_FRAME_HEIGHT))
            assert self.vdo.isOpened()
        self.fps = self.vdo.get(cv2.CAP_PROP_FPS)
        self.idx_frame = -1
        return self

    def __next__(self):
        while True:
            idx = self.vdo.grab()
            if self.webcam and not idx:
                rec = self._reconnect()
                if not rec:
                    break
            elif not idx:
                break
            self.idx_frame += 1
            if self.idx_frame % self.frame_interval == 0:
                ref, ori_img = self.vdo.retrieve()
                return ori_img, self.idx_frame
        self.vdo.release()
        raise StopIteration()

    def get_name(self):
        return self.video_path.split('/')[-1]

    def _reconnect(self):
        retry = 3
        i = 1
        while True:
            i += 1
            self.vdo = cv2.VideoCapture(self.rtsp_addr)
            if self.vdo.isOpened():
                return True
            if i > retry:
                return False

if __name__ == '__main__':
    vs = VideoSource(video_path='../002.mkv', webcam=False)
    i = 0
    for ret, ori_img in vs:
        i += 1
        if i % 100 == 0:
            print(i)
    print(vs.fps)