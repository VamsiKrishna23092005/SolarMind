from transformers import AutoProcessor, AutoModelForCausalLM
import torch
from PIL import Image
import warnings

# Suppress unimportant huggingface warnings
warnings.filterwarnings("ignore")

class VisionModel:
    def __init__(self, model_id="microsoft/Florence-2-base"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        # Using open-source free local model
        self.model = AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True).to(self.device).eval()
        self.processor = AutoProcessor.from_pretrained(model_id, trust_remote_code=True)

    def analyze_solar_graph(self, image_path: str) -> str:
        try:
            image = Image.open(image_path).convert("RGB")
        except Exception as e:
            return f"Error loading image: {e}"
            
        task_prompt = "<MORE_DETAILED_CAPTION>"
        text_input = task_prompt + " Describe solar irradiance and efficiency trends observed in this graph."
        
        inputs = self.processor(text=text_input, images=image, return_tensors="pt").to(self.device)
        generated_ids = self.model.generate(
            input_ids=inputs["input_ids"],
            pixel_values=inputs["pixel_values"],
            max_new_tokens=1024,
            num_beams=3
        )
        generated_text = self.processor.batch_decode(generated_ids, skip_special_tokens=False)[0]
        parsed_answer = self.processor.post_process_generation(generated_text, task=task_prompt, image_size=(image.width, image.height))
        
        return str(parsed_answer)

# Lazy initialization approach to prevent loading gigabytes until needed
_vision_model_instance = None
def get_vision_model():
    global _vision_model_instance
    if _vision_model_instance is None:
        _vision_model_instance = VisionModel()
    return _vision_model_instance
