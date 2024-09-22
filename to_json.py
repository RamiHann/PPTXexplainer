import json
import os

def save_to_json(presentation_path, slides_contents, explanations):
    """
    Save explanations to a JSON file.

    Args:
        presentation_path (str): Path to the PowerPoint presentation file.
        slides_contents (list): List of original slide contents.
        explanations (list): List of explanations for each slide.

    Returns:
        str: Path to the output JSON file.
    """
    # Extract the base name of the presentation file
    base_name = os.path.splitext(os.path.basename(presentation_path))[0]

    # Create the output file name by adding ".json" to the base name
    output_file = f"{base_name}.json"

    # Structure the data to be saved in JSON format
    slides_data = [
        {
            "slide_number": i + 1,
            "content": content,
            "explanation": explanation
        }
        for i, (content, explanation) in enumerate(zip(slides_contents, explanations))
    ]

    # Write the structured data to the JSON file
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(slides_data, file, indent=4)

    return output_file
