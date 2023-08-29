import torch
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from IPython.display import display

processor = TrOCRProcessor.from_pretrained("microsoft/trocr-large-handwritten")
model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-large-handwritten")


def image_to_stream(img):
    inputs = processor(img, return_tensors="pt")
    generated_ids = model.generate(inputs.pixel_values, max_length=50)

    output = model(**inputs, decoder_input_ids=generated_ids)
    logits = output.logits

    probs = torch.softmax(logits, dim=-1)

    decoded_preds = processor.batch_decode(probs.argmax(dim=-1), skip_special_tokens=True)

    encoded_text = processor.tokenizer.encode(decoded_preds[0], add_special_tokens=False)
    tokens = processor.tokenizer.convert_ids_to_tokens(encoded_text)

    prob_values = []
    for j, char_idx in enumerate(probs[0, :len(tokens), :].argmax(dim=-1)):
        prob_value = probs[0, j, char_idx].item()
        prob_values.append((tokens[j], prob_value))

    return prob_values
