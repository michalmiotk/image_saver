import webbrowser
from threading import Timer

from flask import Flask, render_template, Response
import cv2
import numpy as np

from mail import send_mail
from secret import sender_mail, sender_pass

app = Flask(__name__)
camera = cv2.VideoCapture(0)


def is_pixel_in_threshold(pixel1, pixel2, percentage_diff):
    ratio = np.sum(pixel1) / np.sum(pixel2)
    up_threshold = 1+percentage_diff/100
    down_threshold = 1 - percentage_diff/100
    return down_threshold <= ratio <= up_threshold


def get_pixel_interval(img_prev_gray_shape,*, steps_width, steps_height):
    return {'height': int(img_prev_gray_shape[0]/steps_height), 'width':int(img_prev_gray_shape[1]/steps_width)}

def calculate_percent_of_different_pixels(counter, steps_width, steps_height):
    return counter/(steps_height*steps_width)*100

def are_two_images_different(img_prev, img_actual):
    assert img_prev.shape == img_actual.shape
    steps_width, steps_height =100, 100

    different_pixels_counter = 0
    interval = get_pixel_interval(img_prev.shape, steps_width=steps_width, steps_height=steps_height)
    different_percent_threshold = 30
    for y in range(img_prev.shape[0]):
        for x in range(img_prev.shape[1]):

            if y % interval['height'] == 0 and x % interval['width'] == 0:
                if not is_pixel_in_threshold(img_prev[y][x], img_actual[y][x], different_percent_threshold):
                    different_pixels_counter += 1
    thres_percent_of_classified_different_pixels = 20

    #print('different_pixels_counter', different_pixels_counter)
    #print('percent', calculate_percent_of_different_pixels(different_pixels_counter, steps_width, steps_height))
    if calculate_percent_of_different_pixels(different_pixels_counter, steps_width, steps_height) >= thres_percent_of_classified_different_pixels:
        return True
    else:
        return False


def generate_frames():
    prev_frame = None
    frame_counter = 0
    while True:

        ## read the camera frame
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            img_m = buffer.tostring()
            buffer_bytes = buffer.tobytes()
            frame_counter+=1
            if frame_counter % 10 == 0:
                if prev_frame is not None:
                    if are_two_images_different(frame, prev_frame):
                        #cv2.imwrite(str(frame_counter)+'.jpg', frame)
                        send_mail(sender_mail, sender_pass, img_m)
                prev_frame = frame
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer_bytes + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')


if __name__ == "__main__":
    Timer(1, open_browser).start();
    app.run(debug=True)