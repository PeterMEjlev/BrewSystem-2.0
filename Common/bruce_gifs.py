#bruce_gifs.py

def start_gif(gif):
    if gif is not None:
        gif.show()
        gif.start_gif()

def stop_gif(gif):
    if gif is not None:
        gif.stop_gif()
        gif.hide()
