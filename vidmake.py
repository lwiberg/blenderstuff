import cv2
import os
import argparse

def images_to_video(image_folder, frame_rate):
    try:
        images = [img for img in os.listdir(image_folder) if img.lower().endswith(('.jpg', '.jpeg', '.png'))]
        
        if not images:
            print("No JPEG or PNG images found in the specified folder.")
            return
        
        frame = cv2.imread(os.path.join(image_folder, images[0]))
        height, width, _ = frame.shape
    
        print(f"Found {len(images)} images in the folder.")
    
        video_name = os.path.join(image_folder, f"{os.path.basename(image_folder)}_{frame_rate}fps.mp4")
        print(f"Output video will be saved as: {video_name}")
    
        video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'mp4v'), frame_rate, (width, height))
    
        for image in images:
            video.write(cv2.imread(os.path.join(image_folder, image)))
    
        video.release()
        print("Video creation complete.")
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    #Method 1:
    #Navigate to folder with images. 
    #Shift + RMB -> Open powershell here
    #vidmake

    #Method 2: 
    #vidmake image_folder

    parser = argparse.ArgumentParser(description='Convert images in a folder to an MP4 video.')
    parser.add_argument('image_folder', type=str, nargs='?', default='.', help='Path to the folder containing images (default: current directory)')
    parser.add_argument('--framerate', type=int, default=24, help='Frame rate of the output video (default: 24)')
    
    args = parser.parse_args()
    
    image_folder = os.path.abspath(args.image_folder)
    images_to_video(image_folder, args.framerate)
