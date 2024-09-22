import os
import asyncio
import pytest
import json
from main import execute_main


@pytest.fixture
def sample_presentation_path():
    path = os.path.abspath("sample_data/demo_presentation.pptx")
    assert os.path.exists(path), f"Sample presentation file does not exist at {path}"
    return path


@pytest.fixture
def output_json_path():
    path = os.path.abspath("sample_data/demo_presentation.json")
    print(f"Expected output JSON path: {path}")
    return path


@pytest.mark.asyncio
async def test_gpt_explainer(sample_presentation_path, output_json_path):
    # Ensure the output file does not exist before the test
    if os.path.exists(output_json_path):
        os.remove(output_json_path)

    print(f"Running main function with presentation path: {sample_presentation_path}")

    # Run the main function and check for exceptions
    try:
        await execute_main(sample_presentation_path)
    except Exception as e:
        pytest.fail(f"execute_main raised an exception: {e}")

    print("Main function executed successfully")

    # Verify the output file is created
    if not os.path.exists(output_json_path):
        # Print the current directory contents for debugging
        print("Current directory contents:")
        print(os.listdir(os.path.dirname(output_json_path)))

        # Check if the file was saved in the current working directory
        current_dir = os.getcwd()
        print(f"Current working directory: {current_dir}")
        print(f"Contents of the current working directory: {os.listdir(current_dir)}")

    assert os.path.exists(output_json_path), "Output JSON file was not created."

    # Verify the contents of the JSON file
    with open(output_json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        assert isinstance(data, list), "Output JSON does not contain a list."
        assert len(data) > 0, "Output JSON list is empty."
        assert all(isinstance(item, str) for item in data), "Output JSON list items are not strings."

    print("Output JSON file verified successfully")

    # Clean up by removing the output file
    os.remove(output_json_path)


if __name__ == "__main__":
    pytest.main()
