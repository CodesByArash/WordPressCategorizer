import requests
import json
from requests.exceptions import RequestException, Timeout, ConnectionError
import time

class OllamaError(Exception):
    pass

class ModelNotAvailableError(OllamaError):
    pass

class OllamaServerError(OllamaError):
    pass

def check_model_availability(model_name="llama3"):

    try:
        r = requests.get(f"http://localhost:11434/api/tags", timeout=10)
        r.raise_for_status()
        models = r.json().get("models", [])
        if not any(model["name"] == model_name for model in models):
            raise ModelNotAvailableError(f"Model '{model_name}' is not installed. Please install it using: ollama pull {model_name}")
        return True
    except ConnectionError:
        raise OllamaServerError("Cannot connect to Ollama server. Make sure it's running (ollama serve)")
    except Exception as e:
        raise OllamaServerError(f"Error checking model availability: {e}")

def get_category_from_ollama(text, max_retries=3, timeout=30, model_name="llama3"):

    check_model_availability(model_name)

    retry_count = 0
    last_error = None
    
    while retry_count < max_retries:
        try:
            r = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": model_name,
                    "prompt": f"Suggest an appropriate English category name for the following blog post content:\n\n{text}\n\nOnly return the category name, nothing else."
                },
                timeout=timeout
            )
            r.raise_for_status()
            
            for line in r.iter_lines():
                if not line:
                    continue
                    
                try:
                    data = json.loads(line)
                    if 'error' in data:
                        error_msg = data['error'].lower()
                        if "model not found" in error_msg:
                            raise ModelNotAvailableError(f"Model '{model_name}' is not installed. Please install it using: ollama pull {model_name}")
                        elif "model is currently loading" in error_msg:
                            print(f"Model '{model_name}' is still loading, waiting...")
                            time.sleep(5)
                            continue
                        else:
                            raise OllamaServerError(f"Ollama error: {data['error']}")
                            
                    if 'response' in data:
                        return data['response'].strip()
                except json.JSONDecodeError as e:
                    raise OllamaServerError(f"Error parsing Ollama response: {e}")
                    
            raise OllamaServerError("No valid response from Ollama")
            
        except (ConnectionError, Timeout) as e:
            last_error = OllamaServerError(f"Connection error with Ollama server: {e}")
        except RequestException as e:
            last_error = OllamaServerError(f"Request to Ollama failed: {e}")
        except OllamaError as e:
            raise e
        except Exception as e:
            last_error = OllamaServerError(f"Unexpected error with Ollama: {e}")
            
        retry_count += 1
        if retry_count < max_retries:
            wait_time = 2 ** retry_count
            print(f"Retry attempt {retry_count}/{max_retries} failed. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
    
    raise last_error or OllamaServerError("All retry attempts failed") 
