import socket
import struct
import numpy as np
import cv2

class sendVideo:
    def __init__(self, server_ip='0.0.0.0', server_port=80):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind((server_ip, server_port))
        self.frame_dict = {}
        self.frame_size = {}

    def retrieve_frame(self):
        try:
            data, addr = self.server_socket.recvfrom(65536)
            frame_id, packet_index, size = struct.unpack("III", data[:12])
            frame_data = data[12:]

            if frame_id not in self.frame_dict:
                self.frame_dict[frame_id] = {}
                self.frame_size[frame_id] = size

            self.frame_dict[frame_id][packet_index] = frame_data

            if sum(len(self.frame_dict[frame_id][i]) for i in self.frame_dict[frame_id]) == self.frame_size[frame_id]:
                complete_frame = b"".join(self.frame_dict[frame_id][i] for i in sorted(self.frame_dict[frame_id].keys()))

                if len(complete_frame) == self.frame_size[frame_id]:
                    frame = np.frombuffer(complete_frame, dtype=np.uint8)
                    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
                    if frame is not None and frame.size > 0:
                        cv2.imshow('Kamikaze Frame', frame)
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            return False
                    else:
                        print("Error: Frame could not be decoded or is empty")
                else:
                    print("Error: Frame size mismatch")

                del self.frame_dict[frame_id]
                del self.frame_size[frame_id]
        except Exception as e:
            print(f"Error receiving frame: {e}")

        return True

send=sendVideo()
while True:
    send.retrieve_frame()