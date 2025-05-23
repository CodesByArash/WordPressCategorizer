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

class OllamaClient:
    def __init__(self, model_name="llama3:latest", base_url="http://localhost:11434"):
        """
        Initialize Ollama client
        
        Args:
            model_name (str): Name of the model to use (default: "llama3:latest")
            base_url (str): Base URL for Ollama API (default: "http://localhost:11434")
        """
        self.model_name = model_name
        self.base_url = base_url.rstrip('/')
        self.check_model_availability()

    def check_model_availability(self):
        """Check if the specified model is available"""
        try:
            r = requests.get(f"{self.base_url}/api/tags", timeout=10)
            r.raise_for_status()
            models = r.json().get("models", [])
            model_exists = any(
                model["name"] == self.model_name or
                model["name"].startswith(f"{self.model_name.split(':')[0]}:")
                for model in models
            )
            if not model_exists:
                raise ModelNotAvailableError(
                    f"Model '{self.model_name}' is not installed. "
                    f"Please install it using: ollama pull {self.model_name}"
                )
            return True
        except ConnectionError:
            raise OllamaServerError(
                f"Cannot connect to Ollama server at {self.base_url}. "
                "Make sure it's running (ollama serve)"
            )
        except Exception as e:
            raise OllamaServerError(f"Error checking model availability: {e}")

    def get_category(self, text, max_retries=3, timeout=30):
        """
        Get category suggestion from Ollama
        
        Args:
            text (str): The text to get category for
            max_retries (int): Maximum number of retry attempts
            timeout (int): Request timeout in seconds
            
        Returns:
            str: Suggested category name
            
        Raises:
            ModelNotAvailableError: If the model is not installed
            OllamaServerError: If there are issues with Ollama server
        """
        retry_count = 0
        last_error = None
        
        while retry_count < max_retries:
            try:
                r = requests.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.model_name,
                        "prompt": (
                            f"Suggest an appropriate English category name for "
                            f"the following blog post content:\n\n{text}\n\n"
                            "Only return the category name, nothing else."
                        )
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
                                raise ModelNotAvailableError(
                                    f"Model '{self.model_name}' is not installed. "
                                    f"Please install it using: ollama pull {self.model_name}"
                                )
                            elif "model is currently loading" in error_msg:
                                print(f"Model '{self.model_name}' is still loading, waiting...")
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