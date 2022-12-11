import cv2
import os
from math import floor
import argparse
from PIL import Image
import datetime

def save_frames_for_file(full_video_path, pics, collage):
    folder_for_video_save = f'{full_video_path}_images'
    os.makedirs(folder_for_video_save, exist_ok=True)
    cap = cv2.VideoCapture(full_video_path)
    frames_num = floor(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    pics_at_sec = floor(float(frames_num) / int(pics))
    start_at = 0
    raw_width = round(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    raw_height = round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    counter = 1
    while pics > 0:
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_at)
        ret, frame = cap.read()
        if not ret:
            break
        image_name = f'{folder_for_video_save}/{counter}.jpg'
        cv2.imwrite(image_name, frame)
        start_at += pics_at_sec
        pics -= 1
        counter += 1
    if collage:
        collage_maker(folder_for_video_save, raw_width, raw_height)


def video_to_frames(video_path, pics, collage):
    full_video_path = video_path
    if os.path.isdir(video_path):
        videos = os.listdir(video_path)
        # create directory for images
        if not os.path.isdir(f'{video_path}/screens'):
            os.mkdir(f'{video_path}/screens')
        
        for _, video_file in enumerate(videos):
            full_video_path = f'{video_path}/{video_file}'
            
            if not os.path.isdir(full_video_path) and (video_file.endswith('.mp4') or video_file.endswith('.mkv') or video_file.endswith('.avi')):
                check = video_file.split('.')[0] + '.jpg'
                if check in os.listdir(f'{video_path}/screens'):
                    print(f'video {video_file} already converted, skipping')
                    continue
                save_frames_for_file(full_video_path, pics, collage)
                print(f'video {video_file} done, remaining: {len(videos) - _ - 1}')
              
def collage_maker(path, raw_width, raw_height):
    folder = path    
    if 'images' in folder:
        images = os.listdir(folder)
        folder_name = folder.split('/')[1].split('.')[0]
        per_row = 5
        canva_size_x = raw_width * per_row
        canva_size_y = 0
        x_size = canva_size_x / per_row
        y_size = raw_height
        x_pos = 0
        y_pos = 0
        for _ in range(0, len(images), per_row):
            canva_size_y += y_size
        img_sheet = Image.new('RGB', (canva_size_x, canva_size_y))
        images = sorted([int(x.split('.')[0]) for x in images]) 
        images = [f'{x}.jpg' for x in images]
        
        for image in images:
            img = Image.open(f'{folder}/{image}')
            img = img.resize((int(x_size), int(y_size)))
            img_sheet.paste(img, (int(x_pos), int(y_pos)))
            x_pos += x_size
            if x_pos >= canva_size_x:
                x_pos = 0
                y_pos += y_size
        img_sheet.save(f'{folder}/../screens/{folder_name}.jpg')
        for image in images:
            if image != f'{folder}/{folder_name}.jpg':
                os.remove(f'{folder}/{image}')
        print('collage saved')
        os.rmdir(folder)
        
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, help='Path to folder with videos', default='videos')
    parser.add_argument('--pics', type=int, help='Number of pics to extract', default=30)
    parser.add_argument('--collage', type=bool, help='Create collage and exclude images', default=True)
    args = parser.parse_args()
    if os.path.isdir(args.path):
        video_to_frames(args.path, pics=args.pics, collage=args.collage)
    else:
        os.makedirs(args.path, exist_ok=True)
        print('Directory created, please put videos in it and run script again')
    
    
if __name__ == '__main__':
    main()
    
