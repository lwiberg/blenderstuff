# folderconvert.py
import os
import sys
import subprocess

def convert_to_hap(folder_path):
    output_folder = os.path.join(folder_path, 'hap_converted')
    os.makedirs(output_folder, exist_ok=True)

    supported_extensions = ('.mp4', '.mov')

    for file in os.listdir(folder_path):
        if file.lower().endswith(supported_extensions):
            input_path = os.path.join(folder_path, file)
            filename_wo_ext = os.path.splitext(file)[0]
            output_path = os.path.join(output_folder, f"{filename_wo_ext}.mov")

            print(f"🔄 Converting: {file} → {output_path}")

            command = [
                "ffmpeg",
                "-i", input_path,
                "-c:v", "hap",
                "-format", "hap_q",  # Use hap_q or change to hap_alpha, etc.
                "-y",
                output_path
            ]

            try:
                print('command: ',command)
                subprocess.run(command, check=True)
                print(f"✅ Done: {output_path}")
            except subprocess.CalledProcessError as e:
                print(f"❌ Error converting {file}: {e}")

    print("🎉 All conversions complete.")

if __name__ == "__main__":
    if "--hap" in sys.argv:
        folder = os.getcwd()
        convert_to_hap(folder)
    else:
        print("Usage: folderconvert --hap")
