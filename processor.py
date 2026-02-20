import subprocess
import os

class VideoProcessor:
    def __init__(self, output_path="processed"):
        self.output_path = output_path
        if not os.path.exists(output_path):
            os.makedirs(output_path)

    def process_video(self, input_path):
        filename = os.path.basename(input_path)
        output_file = os.path.join(self.output_path, f"unique_{filename}")
        
        # FFmpeg command to make video unique:
        # 1. Slight scale/crop (zoom in 2%)
        # 2. Slight brightness/hue shift
        # 3. Slight speed increase (1.01x)
        
        command = [
            'ffmpeg', '-y', '-i', input_path,
            '-vf', "scale=iw*1.02:-1,crop=iw/1.02:ih/1.02,eq=brightness=0.01:saturation=1.05,setpts=0.98*PTS",
            '-af', "atempo=1.02",
            '-c:v', 'libx264', '-crf', '18', '-preset', 'veryfast',
            output_file
        ]
        
        print(f"Processing video to bypass copyright: {input_path}")
        result = subprocess.run(command, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"FFmpeg Error: {result.stderr}")
            raise Exception(f"Failed to process video: {result.stderr}")
            
        print(f"Video processed successfully: {output_file}")
        return output_file

if __name__ == "__main__":
    # Test
    # processor = VideoProcessor()
    # processor.process_video("downloads/test.mp4")
    pass
