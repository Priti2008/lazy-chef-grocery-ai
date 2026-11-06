import os
def analyze_fridge(image_path):
    model = os.getenv("OLLAMA_MODEL", "llama3.2-vision")
    return f"Analyzed using {model}"
