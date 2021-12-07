import argparse
from video.io import Folder2Vid
entry_point = {'folder2vid':Folder2Vid()}
parser = argparse.ArgumentParser(description='CV tool:')
parser.add_argument('task')
temp_args, _ = parser.parse_known_args()
entry_point[temp_args.task].parse_argument(parser)
args = parser.parse_args()
entry_point[args.task](args)

