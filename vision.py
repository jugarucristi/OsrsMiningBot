import cv2 as cv
import numpy as np



class Vision:
    TRACKBAR_WINDOW = "Trackbars"

    needle_img = None
    needle_w = 0
    needle_h = 0
    method = None

    # constructor
    def __init__(self, needle_img_path, method=cv.TM_CCOEFF_NORMED):
        if needle_img_path:
            self.needle_img = cv.imread(needle_img_path, cv.IMREAD_UNCHANGED)

            self.needle_w = self.needle_img.shape[1]
            self.needle_h = self.needle_img.shape[0]

        # TM_CCOEFF, TM_CCOEFF_NORMED, TM_CCORR, TM_CCORR_NORMED, TM_SQDIFF, TM_SQDIFF_NORMED
        self.method = method

    def find(self, haystack_img, threshold=0.5, max_results=10):

        result = cv.matchTemplate(haystack_img, self.needle_img, self.method)


        locations = np.where(result >= threshold)
        locations = list(zip(*locations[::-1]))
        # print(locations)


        if not locations:
            return np.array([], dtype=np.int32).reshape(0, 4)


        rectangles = []
        for loc in locations:
            rect = [int(loc[0]), int(loc[1]), self.needle_w, self.needle_h]
            rectangles.append(rect)
            rectangles.append(rect)

        rectangles, weights = cv.groupRectangles(rectangles, groupThreshold=1, eps=0.5)

        if len(rectangles) > max_results:
            rectangles = rectangles[:max_results]

        return rectangles

    def get_click_points(self, rectangles):
        points = []

        for (x, y, w, h) in rectangles:
            center_x = x + int(w / 2)
            center_y = y + int(h / 2)
            points.append((center_x, center_y))

        return points

    def draw_rectangles(self, haystack_img, rectangles):
        line_color = (0, 255, 0)
        line_type = cv.LINE_4

        for (x, y, w, h) in rectangles:
            top_left = (x, y)
            bottom_right = (x + w, y + h)
            cv.rectangle(haystack_img, top_left, bottom_right, line_color, lineType=line_type)

        return haystack_img


    def draw_crosshairs(self, haystack_img, points):
        marker_color = (255, 0, 255)
        marker_type = cv.MARKER_CROSS

        for (center_x, center_y) in points:

            cv.drawMarker(haystack_img, (center_x, center_y), marker_color, marker_type)

        return haystack_img



    def match_keypoints(self, original_image, patch_size=32):
        min_match_count = 5

        orb = cv.ORB_create(edgeThreshold=0, patchSize=patch_size)
        keypoints_needle, descriptors_needle = orb.detectAndCompute(self.needle_img, None)
        orb2 = cv.ORB_create(edgeThreshold=0, patchSize=patch_size, nfeatures=2000)
        keypoints_haystack, descriptors_haystack = orb2.detectAndCompute(original_image, None)

        FLANN_INDEX_LSH = 6
        index_params = dict(algorithm=FLANN_INDEX_LSH,
                            table_number=6,
                            key_size=12,
                            multi_probe_level=1)

        search_params = dict(checks=50)

        try:
            flann = cv.FlannBasedMatcher(index_params, search_params)
            matches = flann.knnMatch(descriptors_needle, descriptors_haystack, k=2)
        except cv.error:
            return None, None, [], [], None

        good = []
        points = []

        for pair in matches:
            if len(pair) == 2:
                if pair[0].distance < 0.7 * pair[1].distance:
                    good.append(pair[0])

        if len(good) > min_match_count:
            print('match %03d, kp %03d' % (len(good), len(keypoints_needle)))
            for match in good:
                points.append(keypoints_haystack[match.trainIdx].pt)
            # print(points)

        return keypoints_needle, keypoints_haystack, good, points

    def centeroid(self, point_list):
        point_list = np.asarray(point_list, dtype=np.int32)
        length = point_list.shape[0]
        sum_x = np.sum(point_list[:, 0])
        sum_y = np.sum(point_list[:, 1])
        return [np.floor_divide(sum_x, length), np.floor_divide(sum_y, length)]
