import keras
import tensorflow as tf
import pickle


class classif:
    def __init__(self):
        self.model = tf.keras.models.load_model("Models/command_classifire.h5")
        with open(r'Models/tokenizer.pickle', 'rb') as handle:
            self.tokenizer = pickle.load(handle)
        with open(r'Models/attribute_dict.pickle', 'rb') as handle:
            self.attribute_dict = pickle.load(handle)

    def predict(self, text):
        u_text = []
        attribute = -1
        u_text.append(text.split())

        # Преобразуем текст в формат, который понимает модель
        x = self.tokenizer.texts_to_matrix(u_text)

        # Предсказание модели
        label_probs = self.model.predict(x)
        label_corr = label_probs.argmax()
        label_x = label_probs[0][label_corr]

        # Если вероятность предсказания меньше 0.85, вернуть -1
        if label_x < 0.85:
            label_corr = -1
            attribute = -1
        else:
            for i in u_text[0]:
                if i in self.attribute_dict:
                    attribute = self.attribute_dict[i]

        return label_corr, attribute
