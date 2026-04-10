import os, sys
try:
    from google import genai
except ImportError:
    print("Library missing. Run: pip install google-genai")
    sys.exit(1)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Simple client setup - AI Studio key handles everything
client = genai.Client(api_key=GEMINI_API_KEY)

def main():
    if not os.path.exists("Images/"):
        print("Images folder missing!"); sys.exit(1)
        
    images = [f for f in os.listdir("Images/") if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    if not images:
        print("No images found in Images/ folder."); sys.exit(0)

    img_path = os.path.join("Images/", images[0])
    print(f"--- Attempting to analyze: {img_path} ---")

    try:
        # Standard stable model call
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=[
                "Analyze this Krishna image. Output format: Quote: [Hindi Quote] | Title: [Title]",
                genai.types.Part.from_bytes(
                    data=open(img_path, "rb").read(),
                    mime_type="image/jpeg" if img_path.endswith((".jpg", ".jpeg")) else "image/png"
                )
            ]
        )
        
        if response.text:
            with open("metadata.txt", "w", encoding="utf-8") as f:
                f.write(f"{img_path}\n{response.text}")
            print(f"Success! Metadata saved for: {img_path}")
        else:
            print("Empty response from Gemini."); sys.exit(1)
            
    except Exception as e:
        print(f"Gemini API Error: {e}")
        # Agar ye fail hua, toh humein pata chal jayega ki key sahi hai ya nahi
        sys.exit(1)

if __name__ == "__main__":
    main()
