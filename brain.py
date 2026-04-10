import os, sys
try:
    from google import genai
    from google.genai import types
except ImportError:
    print("Missing library. Please run: pip install google-genai")
    sys.exit(1)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Client setup with EXPLICIT API VERSION
# Hum v1 use karenge taaki v1beta ka error na aaye
client = genai.Client(
    api_key=GEMINI_API_KEY,
    http_options={'api_version': 'v1'} 
)

# Stable models ki list
MODELS_TO_TRY = [
    "gemini-1.5-flash",
    "gemini-1.5-pro"
]

def main():
    if not os.path.exists("Images/"):
        print("Images folder missing!"); sys.exit(1)
        
    images = [f for f in os.listdir("Images/") if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    if not images:
        print("No images found."); sys.exit(0)

    img_path = os.path.join("Images/", images[0])
    img_data = open(img_path, "rb").read()

    success = False
    for model_name in MODELS_TO_TRY:
        try:
            print(f"--- Trying Model: {model_name} (Forcing v1 API) ---")
            
            response = client.models.generate_content(
                model=model_name,
                contents=[
                    "Analyze this Krishna image. Output: Quote: [Hindi Quote] | Title: [Title]",
                    types.Part.from_bytes(
                        data=img_data, 
                        mime_type="image/jpeg" if img_path.endswith((".jpg", ".jpeg")) else "image/png"
                    )
                ]
            )
            
            if response.text:
                with open("metadata.txt", "w", encoding="utf-8") as f:
                    f.write(f"{img_path}\n{response.text}")
                print(f"Success with {model_name}!")
                success = True
                break
        except Exception as e:
            print(f"Model {model_name} failed: {e}")
            continue

    if not success:
        print("CRITICAL: All models failed even on v1 API!")
        sys.exit(1)

if __name__ == "__main__":
    main()
