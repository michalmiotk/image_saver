from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)
camera = cv2.VideoCapture(0)
def check_pixel_threshold
def get_pixel_interval(img_prev_gray_shape, steps_width, steps_height):
    return img_prev_gray_shape[0]/steps_height, img_prev_gray_shape[1]/steps_width
def are_two_images_different(img_prev, img_actual):
    assert img_prev.shape == img_actual.shape
    img_prev_gray = cv2.cvtColor(img_prev, cv2.COLOR_BGR2GRAY)
    img_actual_gray = cv2.cvtColor(img_actual, cv2.COLOR_BGR2GRAY)
    steps_width, steps_height =100, 100
    interval_width, interval_height = get_pixel_interval(img_prev_gray.shape, steps_width, steps_height)
    different_percent_threshold = 20
    for y in range(img_prev_gray.shape[0]):
        for x in range(img_prev_gray.shape[1]):
            if y%interval_height == 0 and x%interval_width==0:



def generate_frames():
    while True:

        ## read the camera frame
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(debug=True)