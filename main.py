import struct
import time
import argparse
from pathlib import Path
import time
import logging


## A: import additions
import serial
import time
PORT = "COM4" # change to your QT Py port
BAUD = 115200
ser = serial.Serial(PORT, BAUD, timeout=1)
##

import threading

from pybravo import BravoDriver, PacketID, DeviceID, Packet

which_joint = DeviceID.LINEAR_JAWS
data_file = None

class BravoPoller:

    def __init__(self, bravo, packet, dt=0.1):
        self._bravo = bravo
        self._packet = packet

        self.dt = dt

        self._running = False
        # Create a thread to poll for incoming packets
        self._poll_t = threading.Thread(target=self._poll)
        self._poll_t.daemon = True

        self._running = True
        self._poll_t.start()
    
    def stop(self):
        self._running = False
        self._poll_t.join()

    def _poll(self):

        while self._running:
            self._bravo.send(self._packet)
            time.sleep(self.dt)



def example_joint_positions_cb(packet: Packet) -> None:
    """Read the joint positions from the Bravo 7.

    Args:
        packet: The joint position packet.
    """
    position: float = struct.unpack("<f", packet.data)[0]
    # print(
    #     f"The current joint position of joint {packet.device_id} is {position}"
    # )

    data_file.write(f'{time.time()},POS,{packet.device_id},{position}\n')

def example_joint_modes_cb(packet: Packet) -> None:
    """Read the joint Mode from the Bravo 7.

    Args:
        packet: The joint position packet.
    """
    # position: float = struct.unpack("<f", packet.data)[0]
    # print(
    #     f"The current joint position of joint {packet.device_id} is {position}"
    # )
    pass

def example_joint_velocity_cb(packet: Packet) -> None:
    """Read the joint Mode from the Bravo 7.

    Args:
        packet: The joint position packet.
    """
    velocity: float = struct.unpack("<f", packet.data)[0]
    # print(
    #     f"The current joint velocity of joint {packet.device_id} is {velocity}"
    # )
    data_file.write(f'{time.time()},VEL,{packet.device_id},{velocity}\n')

    pass

def example_joint_current_cb(packet: Packet) -> None:
    """Read the joint Mode from the Bravo 7.

    Args:
        packet: The joint position packet.
    """
    current: float = struct.unpack("<f", packet.data)[0]
    # print(
    #     f"The current joint current joint {packet.device_id} is {current}"
    # )
    data_file.write(f'{time.time()},CUR,{packet.device_id},{current}\n')

    pass

def example_joint_request_cb(packet: Packet) -> None:
    """Read the joint Mode from the Bravo 7.

    Args:
        packet: The joint position packet.
    """
    # position: float = struct.unpack("<f", packet.data)[0]
    # print(
    #     f"The current joint position of joint {packet.device_id} is {position}"
    # )
    pass


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Calculate the square of a given number.")
    parser.add_argument("data_file", type=Path, help="Location for gripper data")
    parser.add_argument("--joint", type=int, default=DeviceID.LINEAR_JAWS, help="Joint to log (1-7)")
    args = parser.parse_args()

    data_file = open(args.data_file,'a+')

    which_joint = args.joint

    bravo = BravoDriver()

    # Attempt to establish a connection with the Bravo
    bravo.connect()

    # Attach a callback to be executed when a packet with the POSITION ID is
    # received
    bravo.attach_callback(PacketID.POSITION, example_joint_positions_cb)
    bravo.attach_callback(PacketID.CURRENT, example_joint_current_cb)
    bravo.attach_callback(PacketID.VELOCITY, example_joint_velocity_cb)
    

    
    ##A: write to data file here
    sensor_pressures = ser.readline().decode().strip()
    data_file.write(f'{time.time()}, SENSORS,{sensor_pressures}\n')



    bravo.attach_callback(PacketID.MODE, example_joint_modes_cb)
    bravo.attach_callback(PacketID.REQUEST, example_joint_request_cb)

    # Create a request for the current joint positions
    request = Packet(
        which_joint, PacketID.REQUEST, bytes([PacketID.POSITION.value,PacketID.VELOCITY.value,PacketID.CURRENT.value])
    )

    poller = BravoPoller(bravo, request)

    # Send the request
    bravo.send(request)

    done = False
    
    while not done:

        cmd = input("(P)osition, (V)elocity, (C)urrent, (N)ote, (S)top or (Q)uit? ")

        cmd = cmd.lower()[0]

        if cmd == 'p':
            pos = input("Position? ")
            request = Packet( which_joint, PacketID.POSITION, struct.pack("<f", float(pos) )) #updating struct.pack("<f", pos) to float(pos)
            bravo.send(request)

        elif cmd == 'v':
            vel = input("Velocity? ")
            request = Packet( which_joint, PacketID.VELOCITY, struct.pack("<f", float(vel)) )
            bravo.send(request)
            pass
        elif cmd=='c':
            cur = input("Current? ")
            request = Packet( which_joint, PacketID.CURRENT, struct.pack("<f", float(cur)) )
            bravo.send(request)
            pass
        elif cmd == 'n':
            note = input("Note? ")
            data_file.write(f'{time.time()} {"Note: ", note}\n')
            pass
        elif cmd=='s':
            request = Packet( which_joint, PacketID.CURRENT, struct.pack("<f", float(0.0)) )
            bravo.send(request)

        elif cmd == 'q':
            done = True
    


    poller.stop()
    bravo.disconnect()