import base64
import csv
import requests
import time

API_KEY = "cae5c0a2de694b1f9086d1077af471ee"
LLM_ENDPOINT = (
    "https://development-cursor.openai.azure.com/"
    "openai/deployments/ForCursor/chat/completions?api-version=2024-02-15-preview"
)

def exponential_backoff_post(url, headers, payload, max_retries=5, initial_delay=2):
    """
    Send a POST request with exponential backoff for rate limiting and server errors.

    :param url: The endpoint URL to send the request.
    :param headers: Dictionary of request headers.
    :param payload: JSON payload for the request.
    :param max_retries: Maximum number of retries before giving up.
    :param initial_delay: Initial wait time (in seconds) before next retry.
    :return: Parsed JSON response from the server, or None if failed.
    """
    delay = initial_delay
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            status_code = response.status_code
            if status_code in [429, 500]:
                # Rate limit or server error. Retry with exponential backoff.
                print(f"Attempt {attempt}/{max_retries} failed with status {status_code}. "
                      f"Retrying in {delay} seconds...")
                time.sleep(delay)
                delay *= 2
            elif status_code == 400:
                # Typically a client-side error; no reason to retry.
                print("Client-side error (400):", response.json())
                return None
            else:
                # Some other HTTP error occurred; stop retrying.
                print(f"HTTP error {status_code} occurred: {http_err}")
                return None
        except Exception as err:
            print(f"An unexpected error occurred: {err}")
            return None

    # If all retries failed, return None
    print("Max retries reached. No successful response.")
    return None

def process_image_to_csv(image_path, output_csv_path):
    """
    Convert tabular data in an image to CSV using an Azure OpenAI model.

    :param image_path: Path to the image file to process.
    :param output_csv_path: Path where the CSV file will be saved.
    """
    def encode_image_to_base64(file_path):
        """
        Read a file in binary mode and return a base64-encoded string.

        :param file_path: The path to the image file.
        :return: Base64-encoded string of the image.
        """
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")

    base64_image = encode_image_to_base64(image_path)

    # Create the chat prompt for the Azure OpenAI model
    chat_prompt = [
        {
            "role": "system",
            "content": "You are an AI assistant that helps transcribe tabular data from images into CSV format."
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Convert this image into a CSV file. Transcribe it manually."
                },
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                }
            ],
        }
    ]

    # Prepare request headers and payload
    headers = {
        "Content-Type": "application/json",
        "api-key": API_KEY
    }
    payload = {
        "messages": chat_prompt,
        "temperature": 0.2,
        "top_p": 0.85,
        "max_tokens": 1024
    }

    # Make the POST request with exponential backoff
    response = exponential_backoff_post(LLM_ENDPOINT, headers, payload)
    if not response:
        print("No response received from the LLM. Exiting.")
        return

    # The Azure OpenAI JSON response structure
    # response['choices'][0]['message']['content'] typically contains the CSV text
    response_content = response['choices'][0]['message']['content']

    # Write the CSV
    with open(output_csv_path, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)

        # Sometimes the model might enclose the response in backticks or code blocks.
        # We can strip them out if needed.
        for line in response_content.strip().splitlines():
            cleaned_line = line.strip().strip('`')
            writer.writerow(cleaned_line.split(','))

    print(f"CSV saved at: {output_csv_path}")

if __name__ == "__main__":
    # Example usage
    IMAGE_PATH = "./example_image.jpg"    # Replace with your image path
    OUTPUT_CSV_PATH = "output_table.csv"  # Where to save the CSV
    process_image_to_csv(IMAGE_PATH, OUTPUT_CSV_PATH)
