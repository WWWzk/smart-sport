class TimeLimiter(object):

    def __init__(self, time_limit, video_fps=25):
        self.time_limit = time_limit
        self.video_fps = video_fps
        self.start_stamp = None

    def set_start_time(self, frame_id):
        self.start_stamp = frame_id

    def if_continue(self, frame_id):
        return self.start_stamp is None or (frame_id - self.start_stamp) / self.video_fps < self.time_limit
