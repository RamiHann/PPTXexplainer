import asyncio
import os
import logging
from openai import AsyncOpenAI
from dotenv import load_dotenv
from extract_txt import extract_text_from_presentation
from to_json import save_to_json
from gpt_explainer import process_all_slides

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def load_env_vars():
    """
    Load environment variables from a .env file.

    Uses the `load_dotenv` function from the `dotenv` module to load environment variables
    and logs the action.
    """
    load_dotenv()
    logging.info("Environment variables loaded.")


def get_api_key():
    """
    Retrieve the OpenAI API key from the environment variables.

    Returns:
        str: The OpenAI API key if it is found in the environment variables.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        logging.info("API key retrieved successfully.")
    return api_key


def validate_api_key(api_key):
    """
    Validate the OpenAI API key.

    Args:
        api_key (str): The OpenAI API key to validate.

    Raises:
        ValueError: If the API key is not provided.

    Returns:
        str: The validated API key.
    """
    if not api_key:
        logging.error("API key is missing. Please set the OPENAI_API_KEY in the .env file.")
        raise ValueError("API key is missing. Please set the OPENAI_API_KEY in the .env file.")
    logging.info("API key validated.")
    return api_key


def create_openai_client(api_key):
    """
    Create an OpenAI client using the provided API key.

    Args:
        api_key (str): The OpenAI API key.

    Returns:
        AsyncOpenAI: An instance of the AsyncOpenAI client.
    """
    client = AsyncOpenAI(api_key=api_key)
    logging.info("OpenAI client initialized.")
    return client


def extract_slide_texts(presentation_path):
    """
    Extract text from each slide in a PowerPoint presentation.

    Args:
        presentation_path (str): The file path to the PowerPoint presentation.

    Returns:
        list of str: A list of texts extracted from each slide in the presentation.
    """
    slides_text = extract_text_from_presentation(presentation_path)
    logging.info(f"Extracted text from presentation: {presentation_path}")
    return slides_text


async def fetch_slide_explanations(client, slide_texts):
    """
    Fetch explanations for each slide's text using the OpenAI client.

    Args:
        client (AsyncOpenAI): The OpenAI client to use for fetching explanations.
        slide_texts (list of str): A list of texts extracted from each slide.

    Returns:
        list of str: A list of explanations for each slide's text.
    """
    logging.info("Fetching explanations for slides...")
    explanations = await process_all_slides(client, slide_texts)
    logging.info("Explanations fetched successfully.")
    return explanations


def save_explanations(presentation_path, explanations):
    """
    Save the explanations to a JSON file.

    Args:
        presentation_path (str): The file path to the PowerPoint presentation.
        explanations (list of str): A list of explanations for each slide's text.

    Returns:
        str: The file path to the saved JSON file.
    """
    output_file = save_to_json(presentation_path, explanations)
    logging.info(f"Explanations saved to JSON file: {output_file}")
    return output_file


def display_output_path(output_file):
    """
    Display the path to the output JSON file.

    Args:
        output_file (str): The file path to the saved JSON file.
    """
    logging.info(f"Explanations saved to {output_file}")
    print(f"Explanations saved to {output_file}")


async def execute_main(presentation_path):
    """
    Execute the main logic for extracting, processing, and saving slide explanations.

    Args:
        presentation_path (str): The file path to the PowerPoint presentation.
    """
    try:
        load_env_vars()

        api_key = get_api_key()

        valid_api_key = validate_api_key(api_key)

        client = create_openai_client(valid_api_key)

        slide_texts = extract_slide_texts(presentation_path)

        explanations = await fetch_slide_explanations(client, slide_texts)

        output_file = save_explanations(presentation_path, explanations)

        display_output_path(output_file)
    except Exception as e:
        logging.error(f"An error occurred: {e}")


# Example usage
if __name__ == "__main__":
    # Set presentation path
    presentation_path = os.path.abspath("sample_data/demo_presentation.pptx")

    # Run main function
    asyncio.run(execute_main(presentation_path))
