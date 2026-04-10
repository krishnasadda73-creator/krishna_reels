import os, sys
try:
    from google import genai
except ImportError:
    print("Missing library. Please run: pip install google-genai")
    sys.exit(1)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

# List of models to try (Lightest to most powerful)
MODELS_TO_TRY = [
    "gemini-1.5-flash",        # Sabse fast aur low cost
    "gemini-1.5-flash-latest", # Latest flash
    "gemini-1.5-pro",          # Zyada smart par thoda slow
    "gemini-2.0-flash-exp"     # Experimental (Agar available ho)
]

def main():
    images = [f for f in os.listdir("Images/") if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    if not images:
        print("No images found."); sys.exit(0)

    img_path = os.path.join("Images/", images[0])
    img_data = open(img_path, "rb").read()
    mime_type = "image/png" if img_path.endswith(".png") else "image/jpeg"

    success = False
    for model_name in MODELS_TO_TRY:
        try:
            print(f"--- Trying Model: {model_name} ---")
            response = client.models.generate_content(
                model=model_name,
                contents=[
                    "Analyze this Krishna image. Output: Quote: [Hindi Quote] | Title: [Title]",
                    genai.types.Part.from_bytes(data=img_data, mime_type=mime_type)
                ]
            )
            
            if response.text:
                with open("metadata.txt", "w", encoding="utf-8") as f:
                    f.write(f"{img_path}\n{response.text}")
                print(f"Success with {model_name}!")
                success = True
                break # Agar ek model chal gaya toh loop khatam
        except Exception as e:
            print(f"Model {model_name} failed: {e}")
            continue # Agle model pe jao

    if not success:
        print("CRITICAL: All Gemini models failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
