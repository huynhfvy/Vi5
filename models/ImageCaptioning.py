from transformers import VisionEncoderDecoderModel, ViTFeatureExtractor, AutoTokenizer
import torch
from googletrans import Translator
from PIL import Image
import cv2

model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
feature_extractor = ViTFeatureExtractor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

max_length = 16
num_beams = 4
gen_kwargs = {"max_length": max_length, "num_beams": num_beams}

class ImageCaption:
    def __init__(self, image):
        self.image = image
    def imageCaption(self):
        images = []
        i_image = self.image
        i_image = Image.fromarray(cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB))
        if i_image.mode != "RGB":
          i_image = i_image.convert(mode="RGB")

        images.append(i_image)

        pixel_values = feature_extractor(images=images, return_tensors="pt").pixel_values
        pixel_values = pixel_values.to(device)

        output_ids = model.generate(pixel_values, **gen_kwargs)

        preds = tokenizer.batch_decode(output_ids, skip_special_tokens=True)
        preds = [pred.strip() for pred in preds]

        translator = Translator()
        vi_text = []
        for text in preds:
            vi_text.append(translator.translate(text, dest='vi').text)

        return vi_text

# path = r"D:\STUDY\DHSP\NCKH-2023-With my idol\Doc\Paper\image4.jpg"
# img = cv2.imread(path)
# print(ImageCaption(img).imageCaption())