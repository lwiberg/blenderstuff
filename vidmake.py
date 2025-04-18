import cv2
import os
from PIL import Image
import argparse

def images_to_video(image_folder, frame_rate, filetype, repeats):
    try:
        images = [img for img in os.listdir(image_folder) if img.lower().endswith(('.jpg', '.jpeg', '.png'))]
        
        if not images:
            print("No JPEG or PNG images found in the specified folder.")
            return

        print(f"Found {len(images)} images in the folder.")       

        frame = cv2.imread(os.path.join(image_folder, images[0]))
        height, width, _ = frame.shape

        video_name = os.path.join(image_folder, f"{os.path.basename(image_folder)}_{frame_rate}fps.{filetype}")

        print(f"Output video will be saved as: {video_name}")
        
        if filetype == 'mov' or filetype == 'mp4':
            
            codec = 'mp4v'
            video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*codec), frame_rate, (width, height))
        
            for _ in range(repeats):
                for image in images:
                    video.write(cv2.imread(os.path.join(image_folder, image)))
            
            video.release()
            print("Video creation complete.")
        
        if filetype == 'gif':
            # Use Pillow for GIF creation
            frames = [Image.open(os.path.join(image_folder, img)) for img in images]
            duration = int(1000 / frame_rate)  # Duration per frame in milliseconds

            frames = [frame.resize((width // 2, height // 2), Image.Resampling.LANCZOS) for frame in frames]
            frames = [frame.convert("P", palette=Image.ADAPTIVE) for frame in frames]
            
            extended_frames = frames * repeats

            frames[0].save(
                video_name,
                save_all=True,
                append_images=frames[1:],
                duration=duration,
                loop=0,  # 0 means infinite loop
                optimize=True
            )
            print("GIF creation complete.")
        
        if filetype == 'webp':
            # Load the images as frames
            frames = [Image.open(os.path.join(image_folder, img)) for img in images]

            # Calculate duration per frame in milliseconds
            duration = int(1000 / frame_rate)

            # Resize and convert frames
            frames = [frame.resize((width // 2, height // 2), Image.Resampling.LANCZOS) for frame in frames]
            frames = [frame.convert("RGBA") for frame in frames]  # Convert to RGBA for webp compatibility

            # Extend frames for the desired number of repeats
            extended_frames = frames * repeats

            # Save the frames as an animated webp
            frames[0].save(
                video_name,
                save_all=True,
                append_images=frames[1:],
                duration=duration,
                loop=0  # 0 means infinite loop
            )

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
    parser.add_argument('--filetype', type=str, default='mov', help='File type, mov gif or mp4')
    parser.add_argument('--repeats', type=int, default=1)
    
    args = parser.parse_args()
    
    image_folder = os.path.abspath(args.image_folder)
    images_to_video(image_folder, args.framerate, args.filetype, args.repeats)
