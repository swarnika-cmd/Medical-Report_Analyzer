from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import os


class MedicalReportImageReaderInput(BaseModel):
    """Input schema for MedicalReportImageReader."""
    image_path: str = Field(
        ...,
        description="The absolute file path to the medical report image (JPG, PNG, PDF, etc.)"
    )


class MedicalReportImageReader(BaseTool):
    name: str = "Medical Report Image Reader"
    description: str = (
        "Reads a medical report image (blood test, lab report, health checkup, etc.) "
        "and extracts all text, test names, values, units, and reference ranges from it. "
        "Input MUST be the absolute file path to the image file."
    )
    args_schema: Type[BaseModel] = MedicalReportImageReaderInput

    def _run(self, image_path: str) -> str:
        """Process the medical report image using Gemini Vision API."""
        try:
            import google.generativeai as genai
        except ImportError:
            return (
                "Error: google-generativeai package is not installed. "
                "Please install it with: pip install google-generativeai"
            )

        # Get API key
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            return "Error: GEMINI_API_KEY not found in environment variables."

        # Debug and clean the Windows file path
        print(f"\n[DEBUG] Raw path from agent: {image_path}")
        clean_path = image_path.strip().strip('"').strip("'").replace('\\\\', '\\')
        
        # Validate file exists using the cleaned path
        if not os.path.exists(clean_path):
            print(f"[DEBUG] File DOES NOT EXIST at: {clean_path}")
            return f"Error: File not found at '{clean_path}'. Please check the path."
            
        print(f"[DEBUG] File successfully found!")

        # Validate file type using the cleaned path
        ext = os.path.splitext(clean_path)[1].lower()
        mime_types = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.bmp': 'image/bmp',
            '.webp': 'image/webp',
            '.pdf': 'application/pdf',
        }
        mime_type = mime_types.get(ext)
        if not mime_type:
            return f"Error: Unsupported file format '{ext}'. Supported: {', '.join(mime_types.keys())}"

        try:
            # Configure Gemini
            genai.configure(api_key=api_key)

            # Read the image file
            with open(clean_path, "rb") as f:
                image_data = f.read()

            # Use Gemini Vision to extract medical data
            model = genai.GenerativeModel('gemini-2.5-flash')

            extraction_prompt = """You are a medical report data extraction expert. 
Analyze this medical report image and extract ALL information into a STRICT JSON format.

Do NOT wrap the response in markdown blocks (like ```json). Return ONLY the raw JSON object.

Use this exact JSON schema:
{
  "patient_information": {
    "name": "",
    "age": "",
    "gender": "",
    "date_of_birth": ""
  },
  "report_details": {
    "hospital_name": "",
    "report_date": ""
  },
  "test_results": [
    {
      "test_name": "",
      "measured_value": "",
      "unit": "",
      "reference_range": "",
      "status": "HIGH / LOW / NORMAL"
    }
  ]
}

IMPORTANT RULES:
- Extract EVERY single test result visible.
- If a value is unclear or missing, use "null" or "unclear".
Be exhaustive and output valid JSON only."""

            response = model.generate_content([
                extraction_prompt,
                {
                    "mime_type": mime_type,
                    "data": image_data
                }
            ])

            if response.text:
                return response.text
            else:
                return "Error: Gemini returned an empty response. The image may be unclear."

        except Exception as e:
            print(f"\n[CRITICAL TOOL ERROR] MedicalReportImageReader failed: {str(e)}\n")
            return f"Error processing the image: {str(e)}"