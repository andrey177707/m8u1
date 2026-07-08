from keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np

trash = {"стекло\n":"text/glass.txt", 
"пластик\n":"text/plastic.txt", 
"батарейки\n":"text/battery.txt",
"аккамуляторы\n":"text/accamulator.txt",
"алюминий\n":"text/aluminum.txt",
"бумага и картон\n":"text/paper_cardboard.txt"
}

def detect_trash(img, model, label):

  np.set_printoptions(suppress=True)

  model = load_model(model, compile=False)

  class_names = open(label, "r", encoding='utf-8').readlines()

  data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

  image = Image.open(img).convert("RGB")

  size = (224, 224)
  image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

  image_array = np.asarray(image)

  normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

  data[0] = normalized_image_array

  prediction = model.predict(data)
  index = np.argmax(prediction)
  class_name = class_names[index][2:]
  confidence_score = prediction[0][index]
  path = trash[class_name]
  print(path)
  with open(trash[class_name], 'r', encoding='utf-8') as class_trash:
    content = class_trash.read()

  return class_name, confidence_score, content
