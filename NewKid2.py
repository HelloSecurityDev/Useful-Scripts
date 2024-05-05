# This is an attempt to bring New Kid LLM back to life in a new way but it currently does not work and is only a fraction of its former self
import torch
import torch.nn as nn
import torchvision.models as models
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import asyncio
from pyppeteer import launch

class NLST(nn.Module):
    def __init__(self, language_model):
        super(NLST, self).__init__()
        self.language_model = language_model

    def generate(self, text_input):
        output = self.language_model.generate(text_input)
        return output

class TTNN(nn.Module):
    def __init__(self, vision_model):
        super(TTNN, self).__init__()
        self.vision_model = vision_model

    def process(self, image_input):
        output = self.vision_model(image_input)
        return output

class MultimodalGenerator(nn.Module):
    def __init__(self, nlst_model, ttnn_model, input_size, hidden_size, output_size):
        super(MultimodalGenerator, self).__init__()
        self.nlst_model = nlst_model
        self.ttnn_model = ttnn_model
        combined_output_size = nlst_model.language_model.config.hidden_size + ttnn_model.vision_model.fc.out_features
        self.hidden = nn.Linear(combined_output_size, hidden_size)
        self.relu = nn.ReLU()
        self.output = nn.Linear(hidden_size, output_size)
        self.softmax = nn.Softmax(dim=1)

    def forward(self, text_input, image_input):
        text_output = self.nlst_model.generate(text_input)
        image_output = self.ttnn_model.process(image_input)
        
        # Adjust the size of the text_output tensor
        text_output = text_output[:, -1, :]  # Select the last hidden state
        
        combined_input = torch.cat((text_output, image_output), dim=1)
        x = self.hidden(combined_input)
        x = self.relu(x)
        x = self.output(x)
        x = self.softmax(x)
        return x

async def search_web(query):
    browser = await launch()
    page = await browser.newPage()

    await page.goto('https://www.google.com/')

    await page.type('input[name="q"]', query)

    await asyncio.wait([
        page.keyboard.press('Enter'),
        page.waitForNavigation()
    ])

    await page.waitForSelector('#search')

    search_results = await page.evaluate('''
        Array.from(document.querySelectorAll('h3')).map((el) => ({
            title: el.innerText,
            url: el.parentNode.href,
        }));
    ''')

    await browser.close()

    return search_results

async def main():
    # Example usage
    language_model = GPT2LMHeadModel.from_pretrained('gpt2')
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    vision_model = models.resnet50(pretrained=True)
    input_size = 768 + 1000  # GPT-2 hidden size + ResNet-50 output size
    hidden_size = 256
    output_size = 10

    nlst_model = NLST(language_model)
    ttnn_model = TTNN(vision_model)

    generator = MultimodalGenerator(nlst_model, ttnn_model, input_size, hidden_size, output_size)

    # Generate text input
    text_input = tokenizer.encode("Generate a creative story", return_tensors='pt')

    # Generate image input
    image_input = torch.randn(1, 3, 224, 224)

    # Generate output
    output = generator(text_input, image_input)

    print("Generated Output:")
    print(output)

    # Web Search
    query = input("Enter your search query: ")

    search_results = await search_web(query)

    if search_results:
        print("Search Results:")
        for result in search_results:
            print(result['title'])
            print(result['url'])
            print('---------')
    else:
        print("No web results found.")

# Run the async function using asyncio.run()
asyncio.run(main())
