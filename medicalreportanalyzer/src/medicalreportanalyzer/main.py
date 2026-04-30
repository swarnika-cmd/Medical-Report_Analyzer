#!/usr/bin/env python
import sys
import os
import warnings

# Fix Windows console encoding for Unicode output
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from medicalreportanalyzer.crew import Medicalreportanalyzer

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    # Get image path from command line argument or prompt the user
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        image_path = input("\nEnter the path to your medical report image: ").strip()

    # Clean up the path (remove surrounding quotes if any)
    image_path = image_path.strip('"').strip("'")
    image_path = os.path.abspath(image_path)

    # Validate the file exists
    if not os.path.exists(image_path):
        print(f"\n[ERROR] File not found: {image_path}")
        print("   Please check the file path and try again.")
        sys.exit(1)

    # Validate file type
    valid_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.webp', '.pdf'}
    ext = os.path.splitext(image_path)[1].lower()
    if ext not in valid_extensions:
        print(f"\n[ERROR] Unsupported file format '{ext}'")
        print(f"   Supported formats: {', '.join(valid_extensions)}")
        sys.exit(1)

    print(f"\n{'='*60}")
    print(f"  MEDICAL REPORT ANALYZER")
    print(f"{'='*60}")
    print(f"  File: {os.path.basename(image_path)}")
    print(f"  Path: {image_path}")
    print(f"{'='*60}")
    print(f"\n  Analyzing your report... This may take a minute.\n")

    inputs = {
        'image_path': image_path,
    }

    try:
        result = Medicalreportanalyzer().crew().kickoff(inputs=inputs)
        print(f"\n{'='*60}")
        print(f"  Analysis Complete!")
        print(f"  Report saved to: health_report.md")
        print(f"{'='*60}\n")
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "image_path": "sample_report.jpg",
    }
    try:
        Medicalreportanalyzer().crew().train(
            n_iterations=int(sys.argv[1]),
            filename=sys.argv[2],
            inputs=inputs
        )
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        Medicalreportanalyzer().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "image_path": "sample_report.jpg",
    }

    try:
        Medicalreportanalyzer().crew().test(
            n_iterations=int(sys.argv[1]),
            eval_llm=sys.argv[2],
            inputs=inputs
        )
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")


def run_with_trigger():
    """
    Run the crew with trigger payload.
    """
    import json

    if len(sys.argv) < 2:
        raise Exception(
            "No trigger payload provided. Please provide JSON payload as argument."
        )

    try:
        trigger_payload = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        raise Exception("Invalid JSON payload provided as argument")

    inputs = {
        "crewai_trigger_payload": trigger_payload,
        "image_path": "",
    }

    try:
        result = Medicalreportanalyzer().crew().kickoff(inputs=inputs)
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the crew with trigger: {e}")
