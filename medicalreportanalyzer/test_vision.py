import os
from google import genai
from google.genai import types

# 1. Setup (Put your brand new working API key here)
api_key = "AIzaSyBKlgwunT_OeufJvPjN5A7QiYJj9oMArNw"

# Initialize the modern client
client = genai.Client(api_key=api_key)

# 2. EXACT path to your image
image_path = r"C:\Users\somva\first program\Report_Analyzer\medicalreportanalyzer\sample_blood_report.png"

print(f"Testing file at: {image_path}")

if not os.path.exists(image_path):
    print("❌ ERROR: File does not exist!")
    exit()
else:
    print("✅ File found successfully.")

# 3. Try sending to Gemini using the new SDK
try:
    print("⏳ Sending to Gemini 2.5 Flash...")
    
    with open(image_path, "rb") as f:
        image_bytes = f.read()
        
    # The new SDK uses types.Part to handle images securely
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=[
            "Just reply 'Image received' if you can clearly see this.",
            types.Part.from_bytes(data=image_bytes, mime_type="image/png")
        ]
    )
    
    print("✅ Gemini Response:", response.text)
    print("🎉 SUCCESS! No more warnings, no more crashes.")

except Exception as e:
    print("\n❌ GEMINI API CRASHED!")
    print(f"Exact Error Details: {str(e)}")