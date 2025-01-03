import math
import pigpio

from utils import map_to_int8t, int_to_uint8t

COLLECTION_I2C_ADDR = 0x30

IS_RUNNING_BYTE = 0x00

BASE_ANGLE_BYTE = 0x01
MID_ANGLE_BYTE = 0x02
TIP_ANGLE_BYTE = 0x03
ROTATE_BYTE = 0x04
GRIPPER_SPEED_BYTE = 0x05

BELT_SPEED_BYTE = 0x06
COLLECTOR_ANGLE_BYTE = 0x07

handle = None


def get_handle(pi: pigpio.pi):
    return pi.i2c_open(1, COLLECTION_I2C_ADDR)


def close_handle(pi: pigpio.pi):
    if handle != None:
        pi.i2c_close(handle)
        handle = None


def send_state(
    pi: pigpio.pi,
    is_running: bool,
    base_angle: float,
    mid_angle: float,
    tip_angle: float,
    rotate: float,
    gripper_speed: float,
    belt_speed: float,
    angle: float,
) -> bool:
    global handle
    try:
        if handle == None:
            handle = get_handle(pi)

        pi.i2c_write_byte_data(handle, IS_RUNNING_BYTE, int(is_running))

        pi.i2c_write_byte_data(
            handle,
            BASE_ANGLE_BYTE,
            int_to_uint8t(map_to_int8t(base_angle, -math.pi, math.pi)),
        )
        pi.i2c_write_byte_data(
            handle,
            MID_ANGLE_BYTE,
            int_to_uint8t(map_to_int8t(mid_angle, -math.pi, math.pi)),
        )
        pi.i2c_write_byte_data(
            handle,
            TIP_ANGLE_BYTE,
            int_to_uint8t(map_to_int8t(tip_angle, -math.pi, math.pi)),
        )
        pi.i2c_write_byte_data(
            handle,
            ROTATE_BYTE,
            int_to_uint8t(map_to_int8t(rotate, -math.pi, math.pi)),
        )
        pi.i2c_write_byte_data(
            handle,
            GRIPPER_SPEED_BYTE,
            int_to_uint8t(map_to_int8t(gripper_speed, -1.0, 1.0)),
        )
        pi.i2c_write_byte_data(
            handle,
            BELT_SPEED_BYTE,
            int_to_uint8t(map_to_int8t(belt_speed, -1.0, 1.0)),
        )
        pi.i2c_write_byte_data(
            handle,
            COLLECTOR_ANGLE_BYTE,
            int_to_uint8t(map_to_int8t(angle, -math.pi / 4, math.pi / 4)),
        )
        return True
    except Exception as e:
        handle = None
        return False
