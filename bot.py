import os
import pickle
import random
import google.generativeai as genai
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import subprocess

# --- CONFIGURATION ---
# GitHub Secrets se API Key uthayega
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

def get_gemini_content(image_path):
    print(f"--- Gemini is analyzing: {image_path} ---")
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Image upload to Gemini
    img_file = genai.upload_file(image_path)
    
    prompt = """Analyze this image of Lord Krishna. 
    1. Write a beautiful, short devotional Hindi quote (max 10-12 words) for a reel.
    2. Suggest a catchy YouTube Short title with hashtags.
    Output format exactly like this: Quote: [Hindi Quote] | Title: [Title]"""
    
    response = model.generate_content([prompt, img_file])
    return response.text

def render_video(image_path, audio_path, quote):
    output_video = "final_reel.mp4"
    print(f"--- Rendering Video with FFmpeg ---")
    
    # FFmpeg Command: 
    # 1. Image ko 9:16 (1080x1920) mein scale karega.
    # 2. Text ko center mein wrap karega.
    # 3. Audio add karega (5 seconds).
    
    # Simple Text Overlay (Hindi fonts support ke liye GitHub Actions pe default font use karega)
    font_settings = "drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='{0}':fontcolor=white:fontsize=50:x=(w-text_w)/2:y=(h-text_h)/2:box=1:boxcolor=black@0.6:boxborderw=10"
    clean_quote = quote.replace("'", "") # Single quotes hatao taaki command na fate
    
    cmd = [
        'ffmpeg', '-y', '-loop', '1', '-i', image_path, '-i', audio_path,
        '-vf', f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,{font_settings.format(clean_quote)}",
        '-t', '5', '-pix_fmt', 'yuv420p', '-shortest', output_video
    ]
    
    subprocess.run(cmd, check=True)
    return output_video

def upload_to_youtube(video_file, title):
    print(f"--- Uploading to YouTube: {title} ---")
    if not os.path.exists('token.pickle'):
        raise FileNotFoundError("token.pickle not found! Please run auth_setup.py locally first.")

    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
    
    youtube = build('youtube', 'v3', credentials=creds)
    
    request_body = {
        'snippet': {
            'title': title[:100], # YouTube limit
            'description': 'Daily Devotional Krishna Status #krishna #shorts #spiritual',
            'categoryId': '22'
        },
        'status': {
            'privacyStatus': 'public', 
            'selfDeclaredMadeForKids': False
        }
    }
    
    media = MediaFileUpload(video_file, chunksize=-1, resumable=True)
    youtube.videos().insert(part='snippet,status', body=request_body, media_body=media).execute()
    print("Video Uploaded Successfully!")

def main():
    # Folder Paths
    IMG_DIR = "Images/"
    BGM_DIR = "BGM/"
    USED_DIR = "Used/"

    # Check if folders exist
    for d in [IMG_DIR, BGM_DIR, USED_DIR]:
        if not os.path.exists(d): os.makedirs(d)

    # 1. Pick an Image
    images = [f for f in os.listdir(IMG_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    if not images:
        print("No images found in Images/ folder!")
        return

    selected_img_name = images[0]
    selected_img_path = os.path.join(IMG_DIR, selected_img_name)

    # 2. Get Quote
    try:
        raw_data = get_gemini_content(selected_img_path)
        # Parsing "Quote: XXX | Title: YYY"
        parts = raw_data.split("|")
        quote = parts[0].replace("Quote:", "").strip()
        title = parts[1].replace("Title:", "").strip()
    except Exception as e:
        print(f"Gemini Error: {e}")
        return

    # 3. Pick Music
    bgms = [f for f in os.listdir(BGM_DIR) if f.lower().endswith('.mp3')]
    selected_bgm = os.path.join(BGM_DIR, random.choice(bgms)) if bgms else None

    if not selected_bgm:
        print("No BGM found!")
        return

    # 4. Render & Upload
    try:
        video_path = render_video(selected_img_path, selected_bgm, quote)
        upload_to_youtube(video_path, title)
        
        # 5. Cleanup: Move image to Used folder
        os.rename(selected_img_path, os.path.join(USED_DIR, selected_img_name))
        print(f"Done! {selected_img_name} moved to Used folder.")
        
    except Exception as e:
        print(f"Process Error: {e}")

if __name__ == "__main__":
    main()
