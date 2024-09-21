import cv2
import socket
import struct
import pickle

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_ip = '192.168.1.100'  # Gerçek IP adresi ile değiştir
server_port = 8000  # Uygun bir port numarası ile değiştir
client_socket.connect((server_ip, server_port))

# Kamerayı başlat
cam = cv2.VideoCapture(0)

# Kamerayı 640x480 çözünürlüğe ayarla
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

img_counter = 0

# JPEG kalite parametresi
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
class Video():

    def client(self):
        try:
            while True:
                ret, frame = cam.read()
                if not ret:
                    print("Kamera okuma hatası")
                    break

                # Görüntüyü JPEG formatında kodla
                result, frame = cv2.imencode('.jpg', frame, encode_param)
                if not result:
                    print("Görüntü kodlama hatası")
                    continue

                # Görüntüyü serileştir
                data = pickle.dumps(frame, 0)
                size = len(data)

                print(f"{img_counter}: {size} byte")

                # Görüntü boyutunu ve verisini gönder
                try:
                    client_socket.sendall(struct.pack(">L", size) + data)
                except Exception as e:
                    print(f"Veri gönderme hatası: {e}")
                    break

                img_counter += 1
        except KeyboardInterrupt:
            print("Çıkış yapılıyor...")
        finally:
            cam.release()
            client_socket.close()

video=Video()
while True:
    video.client()