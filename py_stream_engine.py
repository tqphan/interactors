import ctypes
from ctypes import c_int, c_void_p, c_char, c_char_p, c_longlong, c_float
from ctypes import create_string_buffer, byref, WinDLL, Structure
from ctypes import cast, sizeof, memmove, addressof, POINTER, CFUNCTYPE
from enum import Enum

# class tobii_error_t(IntEnum):
#     TOBII_ERROR_NO_ERROR = 0
#     TOBII_ERROR_INTERNAL = 1
#     TOBII_ERROR_INSUFFICIENT_LICENSE = 2
#     TOBII_ERROR_NOT_SUPPORTED = 3
#     TOBII_ERROR_NOT_AVAILABLE = 4
#     TOBII_ERROR_CONNECTION_FAILED = 
#     TOBII_ERROR_TIMED_OUT,
#     TOBII_ERROR_ALLOCATION_FAILED,
#     TOBII_ERROR_INVALID_PARAMETER,
#     TOBII_ERROR_CALIBRATION_ALREADY_STARTED,
#     TOBII_ERROR_CALIBRATION_NOT_STARTED,
#     TOBII_ERROR_ALREADY_SUBSCRIBED,
#     TOBII_ERROR_NOT_SUBSCRIBED,
#     TOBII_ERROR_OPERATION_FAILED,
#     TOBII_ERROR_CONFLICTING_API_INSTANCES,
#     TOBII_ERROR_CALIBRATION_BUSY,
#     TOBII_ERROR_CALLBACK_IN_PROGRESS,
#     TOBII_ERROR_TOO_MANY_SUBSCRIBERS

tobii_stream_engine = 'tobii_stream_engine.dll'

class tobii_gaze_point_t(Structure):
    _fields_ = [('timestamp_us', c_longlong), 
                ('validity', c_int), 
                ('position_xy', c_float * 2)]

class tobii_gaze_origin_t(Structure):
    _fields_ = [('timestamp_us', c_longlong), 
                ('left_validity', c_int), 
                ('left_xyz', c_float * 3),
                ('right_validity', c_int), 
                ('right_xyz', c_float * 3)]


tse_dll = WinDLL(tobii_stream_engine)

tobii_api_create = tse_dll.tobii_api_create
tobii_api_create.argtypes = [POINTER(c_void_p), c_int, c_int]
tobii_api_create.restype = c_int

tobii_api_destroy = tse_dll.tobii_api_destroy
tobii_api_destroy.argtypes = [c_void_p]
tobii_api_destroy.restype = c_int

tobii_device_create = tse_dll.tobii_device_create
tobii_device_create.argtypes = [c_void_p, c_char_p, POINTER(c_void_p)]
tobii_device_create.restype = c_int

tobii_device_destroy = tse_dll.tobii_device_destroy
tobii_device_destroy.argtypes = [c_void_p]
tobii_device_destroy.restype = c_int

URLRECEIVER = CFUNCTYPE(None, c_char_p, c_void_p)
GPCALLBACK = CFUNCTYPE(None, POINTER(tobii_gaze_point_t), c_void_p)

tobii_enumerate_local_device_urls = tse_dll.tobii_enumerate_local_device_urls
tobii_enumerate_local_device_urls.argtypes = [c_void_p, URLRECEIVER, c_void_p]
tobii_enumerate_local_device_urls.restype = c_int

tobii_gaze_point_subscribe = tse_dll.tobii_gaze_point_subscribe
tobii_gaze_point_subscribe.argtypes = [c_void_p, GPCALLBACK, c_void_p]
tobii_gaze_point_subscribe.restype = c_int

tobii_gaze_point_unsubscribe = tse_dll.tobii_gaze_point_unsubscribe
tobii_gaze_point_unsubscribe.argtypes = [c_void_p]
tobii_gaze_point_unsubscribe.restype = c_int

tobii_wait_for_callbacks = tse_dll.tobii_wait_for_callbacks
tobii_wait_for_callbacks.argtypes = [c_void_p, c_int, POINTER(c_void_p)]
tobii_wait_for_callbacks.restype = c_int

tobii_device_process_callbacks = tse_dll.tobii_device_process_callbacks
tobii_device_process_callbacks.argtypes = [c_void_p]
tobii_device_process_callbacks.restype = c_int

def py_url_receiver(url, user_data):
    # user_data = cast(user_data, c_char_p)
    c = cast(user_data, POINTER(c_char))
    addr = addressof(c.contents)
    c2 = (c_char*256).from_address(addr)
    nb = min(len(url), 256-1)

    c2[:nb] = url[:nb]
    c2[nb+1] = b'\0'
    user_data = c_char_p(url)

def user_callback(x, y):
    # print(x, y)
    pass

callback = user_callback

def py_gaze_point_callback(gaze_point, user_data):
    gp = gaze_point.contents
    callback(gp.position_xy[0], gp.position_xy[1])
    # print("x : %f, y : %f" %(gp.position_xy[0], gp.position_xy[1]))

url_receiver = URLRECEIVER(py_url_receiver)
gaze_point_callback = GPCALLBACK(py_gaze_point_callback)

url = []
# callback 

# def set_callback(cb):
