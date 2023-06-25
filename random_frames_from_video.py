import cv2
import random

# запрашиваем у пользователя имя файла видео и папки сохранения
video_file = input("Введите имя файла видео: ")
save_folder = input("Введите имя папки сохранения: ")

vidcap = cv2.VideoCapture(video_file)
fps = int(vidcap.get(cv2.CAP_PROP_FPS))
frame_count = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))

# создаем список всех возможных номеров кадров
frame_numbers = list(range(int(frame_count*0.7), frame_count))
# перемешиваем список
random.shuffle(frame_numbers)

# выбираем первые 10 уникальных номеров кадров
selected_frames = set()
while len(selected_frames) < 500:
  selected_frames.add(frame_numbers.pop())

# извлекаем выбранные кадры и сохраняем их
for i, frame_number in enumerate(selected_frames):
  vidcap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
  success, image = vidcap.read()
  cv2.imwrite(os.path.join(save_folder, "frame%d.jpg" % i), image)
