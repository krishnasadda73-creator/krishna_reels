import os
import sys
from google import genai

# ================== CONFIG ==================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("❌ API key missing! Set GEMINI_API_KEY")
    sys.exit(1)

client = genai.Client(api_key=GEMINI_API_KEY)

# ================== MAIN ==================
def main():
    folder = "Images"

    if not os.path.exists(folder):
        print("❌ Images folder missing!")
        sys.exit(1)

    images = [f for f in os.listdir(folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    if not images:
        print("⚠️ No images found in Images/")
        sys.exit(0)

    print(f"📸 Found {len(images)} images\n")

    for img in images:
        img_path = os.path.join(folder, img)
        print(f"👉 Processing: {img}")

        try:
            # Read image safely
            with open(img_path, "rb") as f:
                img_bytes = f.read()

            # Gemini request
            response = client.models.generate_content(
                model="gemini-2.0-flash",   # ✅ latest working model
                contents=[
                    "Generate a short emotional Krishna quote in Hindi and a viral YouTube Shorts title. Format: Quote: ... | Title: ...",
                    genai.types.Part.from_bytes(
                        data=img_bytes,
                        mime_type="image/jpeg" if img.lower().endswith((".jpg", ".jpeg")) else "image/png"
                    )
                ]
            )

            if response.text:
                with open("metadata.txt", "a", encoding="utf-8") as f:
                    f.write(f"{img}\n{response.text}\n\n")

                print(f"✅ Done: {img}")

            else:
                print(f"⚠️ Empty response: {img}")

        except Exception as e:
            print(f"❌ Error in {img}: {e}")

    print("\n🎉 All images processed!")

# ================== RUN ==================
if __name__ == "__main__":
    main()
