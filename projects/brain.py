import torch
from transformers import AutoTokenizer, AutoModelForQuestionAnswering

# Load pre-trained model and tokenizer
model_name = "distilbert-base-cased-distilled-squad"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForQuestionAnswering.from_pretrained(model_name)

# Define a function to generate an answer for a given question and context
def generate_answer(question, context):
    # Tokenize the input text and get input IDs and attention masks
    encoding = tokenizer.encode_plus(question, context, return_tensors="pt", max_length=512, truncation=True)
    input_ids = encoding["input_ids"]
    attention_mask = encoding["attention_mask"]
    
    # Get the start and end logits from the model
    with torch.no_grad():
        inputs = {"input_ids": input_ids, "attention_mask": attention_mask}
        outputs = model(**inputs)
        start_logits, end_logits = outputs.start_logits, outputs.end_logits

    # Find the start and end indices of the answer span
    start_index = torch.argmax(start_logits)
    end_index = torch.argmax(end_logits)

    # Get the answer span and return it
    answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(input_ids[0][start_index:end_index+1]))
    return answer


# Define a function to handle user input and generate responses
def chat():
    print("Hello! I'm ChatBot. How can I help you?")
    while True:
        # Get user input
        user_input = input("You: ")
        
        # Check if the user wants to end the conversation
        if user_input.lower() in ['bye', 'goodbye']:
            print("ChatBot: Goodbye!")
            break
        
        # If this is the first input, assume it's the context for future questions
        if not "conversation" in locals():
            conversation = user_input
            print("ChatBot: What can I help you with?")
        
        # Otherwise, generate an answer to the user's question based on the context
        else:
            answer = generate_answer(user_input, conversation)
            if answer:
                print("ChatBot:", answer)
                conversation += f" {user_input} {answer}"
            else:
                print("ChatBot: I'm sorry, I don't know the answer.")
        
# Start the conversation
chat()
