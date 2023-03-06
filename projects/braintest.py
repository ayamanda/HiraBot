import torch
from transformers import BartForConditionalGeneration, BartTokenizer

# Load BART model and tokenizer
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = BartForConditionalGeneration.from_pretrained('facebook/bart-base').to(device)
tokenizer = BartTokenizer.from_pretrained('facebook/bart-base')

# Set model to evaluation mode and disable gradient calculation
model.eval()
for param in model.parameters():
    param.requires_grad = False

# Initialize cache for generated responses
cache = {}

# Generate response using BART model
def generate_response(prompt):
    if prompt in cache:
        response = cache[prompt]
    else:
        input_ids = tokenizer.encode(prompt, return_tensors='pt').to(device)
        output = model.generate(input_ids, max_length=256, num_beams=5, early_stopping=True)
        response = tokenizer.decode(output[0], skip_special_tokens=True)
        cache[prompt] = response
    return response

response = generate_response("how are you?")
print(response)
