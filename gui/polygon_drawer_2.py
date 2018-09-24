import numpy as np
import cv2

CANVAS_SIZE = (800, 800)

FINAL_LINE_COLOR= (255, 0, 255)
WORKING_LINE_COLOR = (127, 127, 127)
POLYGON_COLOR = FINAL_LINE_COLOR
POLYGONS_WANTED = 3

# ==============================

class Drawer(object):
    def __init__(self, window_name, size_x = CANVAS_SIZE[0], size_y = CANVAS_SIZE[1]):
        self.window_name = window_name
        self.done = False
        self.poly_done = False
        self.current = (0,0)
        self.polygons = []
        self.inverted_polygons = []
        self.current_poly_points = []
        self.current_polygon = None
        self.current_poly_counter = 0
        CANVAS_SIZE = (size_x, size_y)

    def on_mouse(self, event, x, y, buttons, user_param):

        if self.poly_done or self.done:
            return #will be handled out of here
        
        if event == cv2.EVENT_MOUSEMOVE:
            self.current = (x,y)
        elif event == cv2.EVENT_LBUTTONDOWN:
            self.current_poly_points.append((x,y))
        elif event == cv2.EVENT_RBUTTONDOWN:
            self.current_poly_points.append(self.current_poly_points[0])
            self.poly_done = True
            
            if self.current_poly_counter == POLYGONS_WANTED -1:
                self.done = True
                self.polygons.append(self.current_poly_points)
            else:
                self.polygons.append(self.current_poly_points)
                self.poly_done = False
                self.current = (0,0)
                self.current_poly_points = []
                self.current_polygon = None
                self.current_poly_counter = self.current_poly_counter + 1

            


    def run(self):
        cv2.namedWindow(self.window_name)
        cv2.imshow(self.window_name, np.zeros(CANVAS_SIZE, np.uint8))
        cv2.waitKey(1)
        cv2.setMouseCallback(self.window_name, self.on_mouse)

        while(not self.done):
            self.draw_polygon()
            self.current_poly_counter = self.current_poly_counter + 1
            self.poly_done = True
        return
            
    def draw_polygon(self):
        while(not self.poly_done):
            canvas = np.zeros(CANVAS_SIZE, np.uint8)

            if len(self.polygons) > 0:
                for p in self.polygons:
                    if(len(p) > 0):
                        cv2.fillPoly(canvas, np.array([p]), POLYGON_COLOR)
                        cv2.imshow(self.window_name, canvas)

            if(len(self.current_poly_points) > 0):
                cv2.polylines(canvas, np.array([self.current_poly_points]), False, FINAL_LINE_COLOR, 1)
                cv2.line(canvas, self.current_poly_points[-1], self.current, WORKING_LINE_COLOR)

            cv2.imshow(self.window_name, canvas)
            if cv2.waitKey(50) == 27:
                pass
        # User finished entering the polygon points. Let's draw and clean or exit
        
        
        self.poly_done = True

    def get_inverted_y_to_fit_TRC(self):
        for polygon in self.polygons:
            current = []
            for point_tuple in polygon:
                current.append((point_tuple[0], 800 - point_tuple[1]))
            self.inverted_polygons.append(current)
        return self.inverted_polygons
        
        

if __name__ == '__main__':
    d = Drawer("Polygon Drawer 2.0")
    d.run()
    print(d.polygons)