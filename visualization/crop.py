import glob, os
import cv2, imageio
#TODO: test code 
def save_image(im, p):
    base_dir = os.path.split(p)[0]
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    cv2.imwrite(p, im)
def read_im(p):
    im = cv2.imread(p)
    assert im is not None, p
    dim = max(im.shape[0], im.shape[1])
    if dim > 1908:
        scale = 1908 / dim
        im = cv2.resize(im, (int(im.shape[1] * scale), int(im.shape[0] * scale)))
    return im
class BulkCrop():
    def __init__(self) -> None:
        self.fixed_size = None
        self.image = None
        self.refPt = None
        self.cropping = None
    def check_no_duplicate(self, a_list):
        a_set = set(a_list)
        no_dup = len(a_list) == len(a_set)
        return no_dup
    def generate_unique_name(self, paths):
        splited = [p.split('/') for p in paths]
        unique_level = -1
        while abs(unique_level) <= len(splited[0]):
            names = [p[unique_level] for p in splited]
            if self.check_no_duplicate(names):
                break
            unique_level -= 1
        if unique_level != -1:
            for i, n in enumerate(names):
                names[i] = n + splited[i][-1]
        return names
    def click_and_crop(self, event, x, y, flags, param):
        # grab references to the global variables
        # if the left mouse button was clicked, record the starting
        # (x, y) coordinates and indicate that cropping is being
        # performed
        if event == cv2.EVENT_LBUTTONDOWN:
            self.refPt = [(x, y)]
            self.cropping = True
        # check to see if the left mouse button was released
        elif event == cv2.EVENT_LBUTTONUP:
            # record the ending (x, y) coordinates and indicate that
            # the cropping operation is finished
            self.refPt.append((x, y))
            self.cropping = False
            # draw a rectangle around the region of interest
            cv2.rectangle(self.image, self.refPt[0], self.refPt[1], (0, 0, 255), self.stroke_size)
            cv2.imshow("image", self.image)
    def draw_and_crop(self, im_path, refPt, name):
        im = read_im(im_path)
        assert im is not None, im_path
        im = cv2.resize(im, (self.fixed_size[1], self.fixed_size[0]))
        roi = im[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]].copy()
        cv2.rectangle(im, refPt[0], refPt[1], (0, 0, 255), self.stroke_size)
        print(os.path.join('crop', name))
        save_image(roi, os.path.join(self.prefix_crop, name))
        save_image(im, os.path.join(self.prefix_rect, name))
        

    
    def __call__(self, args):
        self.prefix_rect = args.prefix_rect
        self.prefix_crop = args.prefix_crop
        self.stroke_size = args.stroke_size
        paths = args.inputs
        self.image = read_im(paths[-1])
        self.fixed_size = self.image.shape
        clone = self.image.copy()
        cv2.namedWindow("image")
        cv2.setWindowProperty("image",cv2.WINDOW_NORMAL,cv2.WINDOW_FULLSCREEN)
        cv2.setMouseCallback("image", self.click_and_crop)
        while True:
        # display the image and wait for a keypress
            cv2.imshow("image", self.image)
            key = cv2.waitKey(1) & 0xFF
            # if the 'r' key is pressed, reset the cropping region
            if key == ord("r"):
                self.image = clone.copy()
            # if the 'c' key is pressed, break from the loop
            elif key == ord("c"):
                break
        # if there are two reference points, then crop the region of interest
        # from teh image and display it
        if len(self.refPt) == 2:
            print(self.refPt)
            # roi = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
            # cv2.imshow("ROI", roi)
            # cv2.waitKey(0)
            names = self.generate_unique_name( paths)
            for i, p in enumerate(paths):
                self.draw_and_crop(p, self.refPt, names[i])
        # close all open windows
        cv2.destroyAllWindows()

    def parse_argument(self, parser):
        parser.add_argument('--inputs', type=str, nargs='+', default=None)
        parser.add_argument('--prefix_crop', type=str, default='crop')
        parser.add_argument('--prefix_rect', type=str, default='rect')
        parser.add_argument('--stroke_size', type=int, default=15)