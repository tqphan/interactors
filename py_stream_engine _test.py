import ctypes
from ctypes import c_int, c_void_p, c_char, c_char_p, c_longlong, c_float
from ctypes import create_string_buffer, byref, WinDLL, Structure
from ctypes import cast, sizeof, memmove, addressof, POINTER, CFUNCTYPE
from py_stream_engine import *

api = c_void_p()
device = c_void_p()
error = tobii_api_create(byref(api), 0, 0)
assert(error == 0)

ss = create_string_buffer(b'\0', 256)
error = tobii_enumerate_local_device_urls(api, url_receiver, ss)
assert(error == 0)

error = tobii_device_create(api, ss, byref(device))
assert(error == 0)

print ("\a")

def test(gaze_point, user_data):
    screen_width = 1920
    screen_height = 1080
    gp = gaze_point.contents
    x = round(gp.position_xy[0] * screen_width)
    y = round(gp.position_xy[1] * screen_height)
    print(gp.validity, x, y)

cb = GPCALLBACK(test)
error = tobii_gaze_point_subscribe(device, cb, 0)
assert(error == 0)

n = 700
while n > 0:
    n -= 1
    error = tobii_wait_for_callbacks(0, 1, byref(device))
    error = tobii_device_process_callbacks(device)


error = tobii_gaze_point_unsubscribe(device)
assert(error == 0)

error = tobii_device_destroy(device)
assert(error == 0)

error = tobii_api_destroy(api)
assert(error == 0)