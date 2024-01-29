import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

generation_config = {
  "temperature": 0,
  "top_k": 1,
  "max_output_tokens": 4000,
}


class LLM:
    def __init__(self, model_name) -> None:
        self.model_name = model_name
        self.model = self.create_model(model_name)

    def create_model(self, model_name):
        match model_name:
            case "GeminiVision":
                genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
                return genai.GenerativeModel('gemini-pro-vision')
            case "Gemini":
                genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
                return genai.GenerativeModel(
                    'gemini-pro',generation_config=generation_config)
  
            case _:
                print("Not Implemented")
          
    def __call__(self, prompt, image=None):
        if self.model_name == 'GeminiVision':
            response = self.model.generate_content(
                [image, prompt]
            )
        elif self.model_name == "Gemini":
            response = self.model.generate_content(
                prompt)
            # print(response.text)
            return response.text
        
        elif self.model_name == 'openai':
            res = self.model.chat.completions.create(
                model="gpt-3.5-turbo-1106",
                response_format={"type": "json_object"},
                messages=[
                    # {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": f"{prompt}"},
                ],
                # seed=10,
                temperature=0
            )
            return res.choices[0].message.content