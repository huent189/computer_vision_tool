import glob, os
import cv2, imageio
class Folder2Vid():
    def __init__(self) -> None:
        pass
    def folder2vid(self, input_folder, name, fps):
        images = glob.glob(os.path.join(input_folder, '*.*'), recursive=True)
        images.sort()
        ims = [cv2.imread(p)[:,:,::-1] for p in images]
        test_im = ims[0]
        if test_im.shape[2] % 2 == 1 or test_im.shape[1] % 2 == 1:
            tgt_size = (test_im.shape[1] // 2 * 2, test_im.shape[0] // 2 * 2)
            ims = [cv2.resize(im, tgt_size) for im in ims]
        imageio.mimwrite(name[:-1] + '.mp4', ims, fps=fps, macro_block_size=1, quality=5)

    def parse_argument(self, parser):
        parser.add_argument('input_folder', type=str, default=None)
        parser.add_argument('output', type=str, default=None)
        parser.add_argument('--fps', type=str, default=24)
    def __call__(self, args):
        vids = glob.glob(args.input_folder + '*/')
        if not os.path.exists(args.output):
            os.makedirs(args.output)
        for vid in vids:
            self.folder2vid(vid, vid.replace(args.input_folder, args.output), args.fps)

