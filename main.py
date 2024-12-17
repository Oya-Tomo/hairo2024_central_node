import socket
import pprint

import pigpio

from state import unpack_state, SystemState, FooterState, ArmState, CollectionState
from nodes import left_footer, right_footer, collection

pi = pigpio.pi()
if not pi.connected:
    print("pigpio not connected!")
    exit()
else:
    print("pigpio connected!")


left_footer_node_handle = left_footer.get_handle(pi)
right_footer_node_handle = right_footer.get_handle(pi)
collection_node_handle = collection.get_handle(pi)


PORT = 5000
SERVER = "0.0.0.0"
ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
server.listen()


system_state: SystemState = SystemState(
    is_running=False,
)
footer_state: FooterState = FooterState(
    left_speed=0.0,
    right_speed=0.0,
    left_front_flipper=0.0,
    left_back_flipper=0.0,
    right_front_flipper=0.0,
    right_back_flipper=0.0,
)
arm_state: ArmState = ArmState(
    base_angle=0.0,
    mid_angle=0.0,
    tip_angle=0.0,
    rotate=0.0,
    gripper_speed=0.0,
)
collection_state: CollectionState = CollectionState(
    speed=0.0,
    angle=0.0,
)

try:
    while True:
        try:
            server.settimeout(1)
            client, addr = server.accept()
            data = client.recv(1024)

            if data == b"":  # Disconnected
                client.close()
                continue

            system_state, footer_state, arm_state, collection_state = unpack_state(data)

            pprint.pprint(system_state)
            pprint.pprint(footer_state)
            pprint.pprint(arm_state)
            pprint.pprint(collection_state)

            client.sendall("ok".encode("utf-8"))
            client.close()
            server.settimeout(None)
        except socket.timeout:
            print("timeout")

        try:
            left_footer.send_state(
                pi,
                left_footer_node_handle,
                system_state.is_running,
                footer_state.left_speed,
                footer_state.left_front_flipper,
                footer_state.left_back_flipper,
            )
        except Exception as e:
            print("left_footer disconnected")

        try:
            right_footer.send_state(
                pi,
                right_footer_node_handle,
                system_state.is_running,
                footer_state.right_speed,
                footer_state.right_front_flipper,
                footer_state.right_back_flipper,
            )
        except Exception as e:
            print("right_footer disconnected")

        try:
            collection.send_state(
                pi,
                collection_node_handle,
                system_state.is_running,
                arm_state.base_angle,
                arm_state.mid_angle,
                arm_state.tip_angle,
                arm_state.rotate,
                arm_state.gripper_speed,
                collection_state.speed,
                collection_state.angle,
            )
        except Exception as e:
            print("collection disconnected")


except KeyboardInterrupt as e:
    print("Finished!")

finally:
    server.shutdown(socket.SHUT_RDWR)
    server.close()
    print("Server closed")

    left_footer.close_handle(pi, left_footer_node_handle)
