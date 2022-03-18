from flask import Flask, render_template, Response, stream_with_context, request
import cv2
from server.AppModule import App
from fps.fps import FPS

host = "0.0.0.0"
port = 8080

flask = Flask(__name__)
app = App()
fps = FPS()

@flask.route('/api/stream/frame/<side>')
def video_feed(side):
    def gen_frames(getFrame):
        fps.start()
        while True:
            frame = getFrame()
            if frame is not None:
                fps.update()
                if (fps._numFrames % 100) == 0:
                    fps.stop()
                    print(fps.fps())
                    fps.start()
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    def gen_frames2(getFrame):
        while True:
            frame = getFrame()
            if frame is not None:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    if side == 'left':
        return Response(gen_frames(app.getLeftFrame), mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        pass
        return Response(gen_frames2(app.getRightFrame), mimetype='multipart/x-mixed-replace; boundary=frame')

# @app.route('/stream')
# def streamed_response():
#     def generate():
#         # yield 'Hello '
#         # yield request.args['name']
#         # yield '!'
#         i = 0
#         while i < 300000000:
#             i += 1
#             if i % 10000 == 0:
#                 yield str(i) + ','
#     return app.response_class(stream_with_context(generate()))


@flask.route('/')
def index():
    return render_template('index.html')

flask.run(debug=False, host=host, port=port)
