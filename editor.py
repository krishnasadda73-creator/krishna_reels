import os, sys, subprocess, random

def main():
    if not os.path.exists("metadata.txt"):
        print("Editor Error: No metadata found!"); sys.exit(1)

    with open("metadata.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
        img_path = lines[0].strip()
        content = lines[1].strip()

    quote = content.split("|")[0].replace("Quote:", "").strip().replace("'", "")
    bgms = [f for f in os.listdir("BGM/") if f.endswith('.mp3')]
    bgm_path = os.path.join("BGM/", random.choice(bgms))
    
    cmd = [
        'ffmpeg', '-y', '-loop', '1', '-i', img_path, '-i', bgm_path,
        '-vf', f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='{quote}':fontcolor=white:fontsize=55:x=(w-text_w)/2:y=(h-text_h)/2:box=1:boxcolor=black@0.6:boxborderw=15",
        '-t', '5', '-pix_fmt', 'yuv420p', '-shortest', 'final_reel.mp4'
    ]
    
    if subprocess.run(cmd).returncode != 0:
        print("Editor Error: FFmpeg failed!"); sys.exit(1)
    print("Editor Success: Video rendered.")

if __name__ == "__main__":
    main()
