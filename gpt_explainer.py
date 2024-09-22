import openai
import asyncio

def generate_prompt(slide_content):
    """
    Generate a prompt for the OpenAI API based on the slide content.

    Args:
        slide_content (str): The content of the slide.

    Returns:
        str: The generated prompt.
    """
    introduction = "Please provide a detailed explanation for the following slide content, starting with the slide number:\n\n"
    prompt = introduction + slide_content
    return prompt

async def fetch_explanation(client, prompt):
    """
    Fetch an explanation for a given prompt using the OpenAI API.

    Args:
        client (openai.AsyncOpenAI): The OpenAI client to use for fetching the explanation.
        prompt (str): The prompt to send to the OpenAI API.

    Returns:
        str: The explanation provided by the OpenAI API.
    """
    system_message = {"role": "system", "content": "You are an assistant specialized in explaining presentation slides."}
    user_message = {"role": "user", "content": prompt}

    messages = []
    messages.append(system_message)
    messages.append(user_message)
    response = await client.chat.completions.create(
        messages=messages,
        model="gpt-3.5-turbo",
    )
    explanation = response.choices[0].message.content.strip()
    return explanation

async def process_all_slides(client, slides_contents):
    """
    Process all slides to fetch explanations for each one using the OpenAI API.

    Args:
        client (openai.AsyncOpenAI): The OpenAI client to use for fetching the explanations.
        slides_contents (list of str): A list of slide contents to process.

    Returns:
        list of str: A list of explanations for each slide.
    """
    tasks = [fetch_explanation(client, generate_prompt(content)) for content in slides_contents]
    explanations = await asyncio.gather(*tasks)
    return explanations
