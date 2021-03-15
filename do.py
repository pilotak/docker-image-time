import os
import time
import io
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime
from PIL import Image, ImageDraw, ImageFile, ImageFont
ImageFile.LOAD_TRUNCATED_IMAGES = True

WATCH_PATH = os.getenv('WATCH_PATH', '.')
SAVE_DIR = os.getenv('SAVE_DIR', None)
FONT_SIZE = int(os.getenv('FONT_SIZE', '25'))
FONT_COLOR = os.getenv('FONT_COLOR', '#ffffff')
TEXT_OFFSET = int(os.getenv('TEXT_OFFSET', '50'))
TEXT_POSITION = os.getenv('TEXT_POSITION', 'bottom-right')

to_process = []
font = ImageFont.truetype("/font.ttf", FONT_SIZE)
font_color = FONT_COLOR.lstrip('#')
font_color = tuple(
    int(font_color[i:i+2], 16) for i in (0, 2, 4))

print("Watching path: %s" % WATCH_PATH)


class MyHandler(FileSystemEventHandler):
    def __init__(self):
        self.src_path = ''

    def on_modified(self, event):
        if self.src_path == event.src_path:
            return
        else:
            self.src_path = event.src_path

        if event.is_directory == False:
            now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

            # event is triggered at the start of modification, delay until everything is saved
            time.sleep(1)

            to_process.append({"file": self.src_path, "time": now})


event_handler = MyHandler()
observer = Observer()
observer.schedule(event_handler, path=WATCH_PATH, recursive=False)
observer.start()

try:
    while True:
        if len(to_process):
            for x in to_process:
                print(x)

                with open(x['file'], 'rb') as f:
                    image = Image.open(io.BytesIO(f.read()))
                    width, height = image.size
                    fx = 0
                    fy = 0

                    draw = ImageDraw.Draw(image)
                    fw, fh = draw.textsize(x['time'], font)

                    position = TEXT_POSITION.split('-')

                    if position[0] == 'bottom':
                        fy = height - TEXT_OFFSET - fh
                    elif position[0] == 'top':
                        fy = TEXT_OFFSET
                    elif position[0] == 'center':
                        fy = height/2 - fh/2

                    if position[1] == 'right':
                        fx = width - TEXT_OFFSET - fw
                    elif position[1] == 'left':
                        fx = TEXT_OFFSET
                    elif position[1] == 'center':
                        fx = width/2 - fw/2

                    draw.text((fx, fy), x['time'],
                              font_color, font=font)

                    image.save(os.path.join(
                        SAVE_DIR, os.path.basename(x['file'])), "JPEG")

            to_process.clear()

        time.sleep(0.5)
except KeyboardInterrupt:
    observer.stop()

observer.join()
