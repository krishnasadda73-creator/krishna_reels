import os, sys, google.generativeai as genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

def main():
    images = [f for f in os.listdir("Images/") if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    if not images:
        print("No images found."); sys.exit(0)

    img_path = os.path.join("Images/", images[0])
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    
    try:
        img_file = genai.upload_file(img_path)
        prompt = "Analyze this Krishna image. Output: Quote: [Hindi Quote] | Title: [Title]"
        response = model.generate_content([prompt, img_file])
        
        # Data ko save kar rahe hain taaki agli script use kar sake
        with open("metadata.txt", "w", encoding="utf-8") as f:
            f.write(f"{img_path}\n{response.text}")
        print(f"Brain Success: Image analyzed.")
    except Exception as e:
        print(f"Brain Error: {e}"); sys.exit(1)

if __name__ == "__main__":
    main()
