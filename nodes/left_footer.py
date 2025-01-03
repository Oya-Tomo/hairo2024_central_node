import math
import pigpio

from utils import map_to_int8t, int_to_uint8t

LEFT_FOOTER_I2C_ADDR = 0x10

IS_RUNNING_BYTE = 0x00

SPEED_BYTE = 0x01

FRONT_ANGLE_BYTE = 0x02
BACK_ANGLE_BYTE = 0x03


handle = None


def get_handle(pi: pigpio.pi):
    return pi.i2c_open(1, LEFT_FOOTER_I2C_ADDR)


def close_handle(pi: pigpio.pi):
    global handle
    if handle != None:
        pi.i2c_close(handle)
        handle = None


def send_state(
    pi: pigpio.pi,
    is_running: bool,
    speed: float,
    front_angle: float,
    back_angle: float,
) -> bool:
    global handle
    try:
        if handle == None:
            handle = get_handle(pi)

        pi.i2c_write_byte_data(handle, IS_RUNNING_BYTE, int(is_running))
        pi.i2c_write_byte_data(
            handle, SPEED_BYTE, int_to_uint8t(map_to_int8t(speed, -1.0, 1.0))
        )
        pi.i2c_write_byte_data(
            handle,
            FRONT_ANGLE_BYTE,
            int_to_uint8t(
                map_to_int8t(
                    front_angle,
                    -math.pi / 2,
                    math.pi / 2,
                ),
            ),
        )
        pi.i2c_write_byte_data(
            handle,
            BACK_ANGLE_BYTE,
            int_to_uint8t(
                map_to_int8t(
                    back_angle,
                    -math.pi / 2,
                    math.pi / 2,
                ),
            ),
        )
        return True
    except Exception as e:
        handle = None
        return False
