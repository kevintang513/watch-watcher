import gradio as gr
from fastai.vision.all import *
import skimage


def label_func(file_name):
    return file_name.name.split('-')[0]


learner = load_learner('watch-classifier.pkl')

labels = learner.dls.vocab


def predict(img):
    img = PILImage.create(img)
    pred, pred_idx, probs = learner.predict(img)
    return {labels[i]: float(probs[i]) for i in range(len(labels))}


title = 'Watch Classifier and Price Estimator'
desc = "A watch brand recognizer and price estimator for 15 of the world's most popular luxury watch brands. Trained on data scraped from chrono24.com."
ghlink = "<p style='text-align: center'><a href='https://github.com/kevintang513/watch-watcher' target='_blank'>Kevin's GitHub</a></p>"

examples = ['rolex-tester.jpg']


gr.Interface(title=title,
             description=desc,
             article=ghlink,
             examples=examples,
             fn=predict,
             inputs=gr.inputs.Image(shape=(512, 512)),
             outputs=gr.outputs.Label(num_top_classes=3),
             enable_queue=True,
             allow_flagging='never'
             ).launch()
