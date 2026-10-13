import cv2
import os

video = cv2.VideoCapture('Original-Pokemon-Theme-SnapYT.App.mp4')
output_dir = "./frames"

os.makedirs(output_dir,exist_ok=True)
frame_number=0

fps = video.get(cv2.CAP_PROP_FPS)
total_frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
interval_seconds = int(total_frames/fps)
frame_interval = int(fps * interval_seconds)

for sec in range(0, interval_seconds, 5):
    target_frame = int(round(sec * fps))
    video.set(cv2.CAP_PROP_POS_FRAMES, target_frame),
    ret, frame = video.read()
    if not ret:
        break
    filename = os.path.join(output_dir,f"frame_{sec:04d}.jpg")
    cv2.imwrite(filename=filename,img=frame)

# while True:
#     ret, frame = video.read()
#     if not ret:
#         break
#     if frame_number % frame_interval == 0 : 
#         timestamp_sec = frame_number / fps
#         filename = os.path.join(output_dir, f"frame_{round(timestamp_sec):04d}.jpg")
#         cv2.imwrite(filename=filename, img=frame)
#     frame_number+=1
video.release()
