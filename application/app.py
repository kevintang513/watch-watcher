import gradio as gr
from fastai.vision.all import *
import fastai
from fastbook import *
import fastbook

def label_func(file_name):
    return file_name.name.split('-')[0]

def label_func_regression(file_name):
    return float(file_name.name.split('-')[2].split('.')[0])

classifier = load_learner('watch-classifier.pkl')
regression = load_learner('price-estimator.pkl')

labels = classifier.dls.vocab

def predict(img):
    img = PILImage.create(img)
    pred, pred_idx, probs = classifier.predict(img)
    pricepred = regression.predict(img)
    return [{labels[i]: float(probs[i]) for i in range(len(labels))}, round(pricepred[0][0], 2)]


title = 'Watch Classifier and Price Estimator'
desc = "A watch brand-recognizer and price-estimator for 15 popular watch brands. Trained on data scraped from chrono24.com. Brands included are Rolex, Omega, TAG Heuer, Seiko, Patek Philippe, Cartier, IWC, Jaeger Lecoultre, Vacheron Constantin, Hamilton, Oris, Audemars Piguet, Tudor, Logines, and Richard Mille."
ghlink = "<p style='text-align: center'><a href='https://github.com/kevintang513/watch-watcher' target='_blank'>Kevin's GitHub</a></p>"
examples = ['rolex-example.jpg']

gr.Interface(title = title,
             description = desc,
             article = ghlink,
             examples = examples,
             fn=predict, 
             inputs=gr.inputs.Image(label = 'Watch Image', shape=(512,512)),
             outputs = [gr.outputs.Label(label='Brand Prediction:', num_top_classes=3), gr.Number(label = 'Price Prediction')],
             enable_queue=True,
             allow_flagging='never'
            ).launch()
