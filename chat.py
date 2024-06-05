import random
import json
import torch
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize_russian

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('intents.json', 'r', encoding='utf-8') as json_data:
    intents = json.load(json_data)

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_Multiplier = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_Multiplier).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "МГКИТ"

def save_unanswered_question(question):
    try:
        with open('questions.json', 'r+', encoding='utf-8') as file:
            data = json.load(file)
            data["questions"].append({"question": question})
            file.seek(0)
            json.dump(data, file, ensure_ascii=False, indent=4)
            file.truncate()
    except FileNotFoundError:
        with open('questions.json', 'w', encoding='utf-8') as file:
            json.dump({"questions": [{"question": question}]}, file, ensure_ascii=False, indent=4)

def get_response(msg):
    sentence = tokenize_russian(msg)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                return random.choice(intent['responses'])
            
    save_unanswered_question(msg)
    return "Простите, я Вас не понял..."


if __name__ == "__main__":
    print("Давайте общаться! (напишите 'Выход' для окончания диалога)")
    while True:
    
        sentence = input("Вы: ")
        if sentence == "Выход":
            break

        resp = get_response(sentence)
        print(resp)
