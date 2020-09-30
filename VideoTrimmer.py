import os

# Class to trim video in samples of interval duration in sec # FIXME The problem is the min duration is 6 sec
# __init__ get a path to raw video directory
# ffmpeg mast be installed and be visible
import cv2
from tqdm import tqdm


class VideoTrimmer(object):
    def __init__(self, path, interval=2, frameRate=25):
        self.path = path
        self.interval = interval
        self.frameRate = frameRate

    def trim(self):
        path = self.path
        if not os.path.exists(path.rstrip(".mp4")):
            self.prepareFrameRate()
            print("Trimming...")
            os.makedirs(path.rstrip(".mp4"))
            vidcapture = cv2.VideoCapture(path)
            fps = vidcapture.get(cv2.CAP_PROP_FPS)
            totalNoFrames = vidcapture.get(cv2.CAP_PROP_FRAME_COUNT);
            duration = int(float(totalNoFrames) / float(fps))
            for i in tqdm(range(int(duration / self.interval))):
                os.system("ffmpeg -i " + path + " -ss " + str(i * self.interval) + " -t " + str(self.interval) + " " + path.rstrip(
                    ".mp4") + "/" + str(i + 1) + ".mp4")
        else:
            print("File already trimmed!")
        print("Done!")

    # def trim(self):
    #     file = self.path
    #     if not os.path.exists(file.rstrip(".mp4")):
    #         self.prepareFrameRate()
    #         print("Trimming...")
    #         os.makedirs(file.rstrip(".mp4"))
    #         request = "ffmpeg -i " + '"' + file + '"' + " -c copy -segment_time " + str(self.interval) + \
    #                   " -reset_timestamps 1 -f segment " + '"' + file.rstrip(".mp4") + "/output_%05d.mp4" + '"'
    #         os.system(request)
    #         os.remove(file)
    #     else:
    #         print("File already trimmed!")
    #     print("Done!")

    # function prepare frame rate of video to 25 fps as in LRW dataset described in article
    def prepareFrameRate(self):
        print("Preparing frame rate")
        file = self.path
        fr = self.frameRate
        video = cv2.VideoCapture(file)
        fps = video.get(cv2.CAP_PROP_FPS)

        if fps != fr:
            tmp = '"' + file.rstrip(
                ".mp4") + "_fps" + str(
                fr) + ".mp4" + '"'

            request = "ffmpeg -i " + '"' + file + '"' + " -r " + str(fr) + " " + tmp
            os.system(request)
            os.remove(file)
            os.rename(file.rstrip(
                ".mp4") + "_fps" + str(
                fr) + ".mp4", file)
        else:
            print("Video already prepared!")
