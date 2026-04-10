import os, sys, pickle
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def main():
    if not os.path.exists("final_reel.mp4"):
        print("Uploader Error: Video file missing!"); sys.exit(1)

    with open("metadata.txt", "r", encoding="utf-8") as f:
        title = f.readlines()[1].split("|")[1].replace("Title:", "").strip()

    with open('token.pickle', 'rb') as t:
        creds = pickle.load(t)
    
    try:
        service = build('youtube', 'v3', credentials=creds)
        request = service.videos().insert(
            part="snippet,status",
            body={'snippet': {'title': title[:100], 'categoryId': '22'}, 'status': {'privacyStatus': 'public'}},
            media_body=MediaFileUpload("final_reel.mp4")
        )
        request.execute()
        print("Uploader Success: Video is LIVE.")
    except Exception as e:
        print(f"Uploader Error: {e}"); sys.exit(1)

if __name__ == "__main__":
    main()
