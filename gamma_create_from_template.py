import requests
from pathlib import Path
import json
import os


def generate_content_from_template(cards_path, config, api_config_file):
    api_key_path = Path(config["api_key_path"])
    api_key = api_key_path.read_text(encoding="utf-8").strip()

    # Prepare headers with API key
    headers = api_config["headers"]
    headers["X-API-KEY"] = api_key

    # Read instructions and cards
    instructions_path = Path(config["instructions_path"])
    cards_path = Path(cards_path)

    instrucoes_md = instructions_path.read_text(encoding="utf-8").strip()
    cards_md = cards_path.read_text(encoding="utf-8").strip()

    # Concatenate instructions and cards
    prompt_final = instrucoes_md + "\n\n" + cards_md

    # Prepare request body
    body = api_config["body"]
    body["prompt"] = prompt_final

    # Make API request
    response = requests.post(config["url"], headers=headers, data=json.dumps(body))

    with open("saida.txt", "w") as fp:
        fp.write(f"Código: {response.status_code}")
        fp.write(response.text)
        fp.write("\n")

    # Print and return response
    print("Status:", response.status_code)
    print(response.text)
    return response


# Example usage
if __name__ == "__main__":
    with open("api_config.json", "r", encoding="utf-8") as api_config_file:
        api_config = json.load(api_config_file)

    with open("config.json", "r", encoding="utf-8") as config_file:
        config = json.load(config_file)

    cards_path = config["cards_path"]
    for file in os.listdir(
        "cards_exemplo",
    ):
        if file.endswith(".md"):
            generate_content_from_template(
                os.path.join("cards_exemplo", file), config, api_config_file
            )
