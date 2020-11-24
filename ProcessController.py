import os

import face_alignment
import pandas as pd
import torch
from facenet_pytorch.models.inception_resnet_v1 import InceptionResnetV1

from VideoChecker import VideoChecker
from VideoLoader import VideoLoader
from VideoTrimmer import VideoTrimmer
from utils import load_checkpoints


# class to wrap workflow
# noinspection PyBroadException
class ProcessController(object):

    def __init__(self, trimInterval=2):
        self.interval = trimInterval
        pd.options.mode.chained_assignment = None

    def load_and_trim(self, url, rawVideoDir):
        try:
            videoLoader = VideoLoader(url, rawVideoDir=rawVideoDir)
            videoLoader.load()
            dir_path = rawVideoDir

            dir = os.listdir(dir_path)
            for elem in dir:
                if elem.count(".mp4") == 1:
                    videoTrimmer = VideoTrimmer(dir_path + elem, interval=10)
                    videoTrimmer.pre_trim()

            dir = os.listdir(dir_path)
            for elem in dir:
                if elem.count(".mp4") == 1:
                    videoTrimmer = VideoTrimmer(dir_path + elem, interval=self.interval)
                    videoTrimmer.trim()
            return True, url
        except:
            return False, url
