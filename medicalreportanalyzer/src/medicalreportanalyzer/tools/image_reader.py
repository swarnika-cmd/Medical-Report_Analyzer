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

        # Validate file exists
        image_path = image_path.strip().strip('"').strip("'")
        if not os.path.exists(image_path):
            return f"Error: File not found at '{image_path}'. Please check the path."

        # Validate file type
        ext = os.path.splitext(image_path)[1].lower()
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
            with open(image_path, "rb") as f:
                image_data = f.read()

            # Use Gemini Vision to extract medical data
            model = genai.GenerativeModel('gemini-2.5-flash-preview-04-17')

            extraction_prompt = """You are a medical report data extraction expert. 
Analyze this medical report image with extreme precision and extract ALL information visible.

Please extract and organize into these categories:

## PATIENT INFORMATION
- Name, Age, Gender, Patient ID, Date of Birth (whatever is visible)

## REPORT DETAILS  
- Lab/Hospital Name, Report Date, Sample Collection Date, Report ID/Number

## TEST RESULTS
For EACH and EVERY test found in the report, extract:
| Test Name | Measured Value | Unit | Reference Range | Status |

Status should be:
- HIGH - if value is above the reference range
- LOW - if value is below the reference range  
- NORMAL - if value is within the reference range

IMPORTANT RULES:
- Extract EVERY single test result visible - do not skip any
- If a test has sub-components (e.g., Differential Count under CBC), extract each one
- If reference ranges vary by age/gender, note the applicable range
- If any value is partially visible or unclear, note it as "unclear"
- Include any doctor's notes or comments if visible

Be exhaustive - missing even one test result is not acceptable."""

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
                return "Error: Gemini returned an empty response. The image may be unclear or not a medical report."

        except Exception as e:
            return f"Error processing the image: {str(e)}"
