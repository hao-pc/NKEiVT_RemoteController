import keras
import tensorflow as tf
import pickle

class classif:
    def __init__(self):
        self.model = tf.keras.models.load_model("reshenie\Models\command_classifire.h5")
        with open(r'reshenie\Models\tokenizer.pickle', 'rb') as handle:
            self.tokenizer = pickle.load(handle)
        with open(r'reshenie\Models\attribute_dict.pickle', 'rb') as handle:
            self.attribute_dict = pickle.load(handle)
    def predict(self, text):
        u_text = []
        attribute = -1
        u_text.append(text.split())
        for i in u_text[0]:
            if i in self.attribute_dict:
                attribute = self.attribute_dict[i]
            else:
                continue
        x = self.tokenizer.texts_to_matrix(u_text)
        label = self.model.predict(x).argmax()
        return label, attribute
