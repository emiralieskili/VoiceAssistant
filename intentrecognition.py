import os
import pickle
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

class IntentRecognition:
    def __init__(self, model_path="intent_model.pkl", intents_path="intents.json", threshold=0.2):
        base_dir = os.path.dirname(__file__)  # bu dosyanın bulunduğu klasör
        self.model_path = os.path.join(base_dir, model_path)
        self.intents_path = os.path.join(base_dir, intents_path)
        self.threshold = threshold

        try:
            with open(self.model_path, "rb") as f:
                self.model, self.vectorizer = pickle.load(f)
        except:
            self.train()  # model yoksa eğit

    def load_intents(self):
        with open(self.intents_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def train(self):
        intents = self.load_intents()

        # dataset hazırla
        X, y = [], []
        for intent, examples in intents.items():
            for ex in examples:
                X.append(ex)
                y.append(intent)

        # TF-IDF vektörizer
        self.vectorizer = TfidfVectorizer(ngram_range=(1,2))
        X_vec = self.vectorizer.fit_transform(X)

        # ML modeli
        self.model = LogisticRegression(max_iter=1000)
        self.model.fit(X_vec, y)

        # kaydet
        with open(self.model_path, "wb") as f:
            pickle.dump((self.model, self.vectorizer), f)

    def get_intent(self, text: str) -> str:
        """
        Kullanıcının söylediği metinden intent tahmin eder.
        Eğer en yüksek olasılık threshold'un altındaysa "bilinmiyor" döner.
        """
        X = self.vectorizer.transform([text])
        probs = self.model.predict_proba(X)[0]
        max_prob = max(probs)
        if max_prob < self.threshold:
            return "bilinmiyor"
        return self.model.classes_[probs.argmax()]

    def learn_new_phrase(self, text: str, learning_threshold=None) -> str:
        """
        Kullanıcının söylediği yeni varyasyonu intent'e ekler
        ve intents.json'u günceller.
        learning_threshold: min olasılık ile öğrenme eşik değeri
        """
        if learning_threshold is None:
            learning_threshold = self.threshold

        X = self.vectorizer.transform([text])
        probs = self.model.predict_proba(X)[0]
        max_prob = max(probs)
        intent_pred = self.model.classes_[probs.argmax()]

        # Eğer max_prob learning_threshold'tan yüksekse öğren
        if max_prob >= learning_threshold:
            # JSON yükle
            with open(self.intents_path, "r", encoding="utf-8") as f:
                intents = json.load(f)

            # Aynı intent varsa listeye ekle, yoksa oluştur
            if intent_pred in intents:
                if text not in intents[intent_pred]:
                    intents[intent_pred].append(text)
            else:
                intents[intent_pred] = [text]

            # JSON kaydet
            with open(self.intents_path, "w", encoding="utf-8") as f:
                json.dump(intents, f, ensure_ascii=False, indent=4)

            # Modeli tekrar eğit
            self.train()
            return intent_pred
        else:
            return "bilinmiyor"


def add_command(intent_name, phrase):
    """
    Yeni bir intent ekler ya da mevcut intent'e varyasyon olarak kaydeder.
    """
    base_dir = os.path.dirname(__file__)  # bu dosyanın bulunduğu klasör
    intents_path = os.path.join(base_dir, "intents.json")

    # intents.json yükle
    with open(intents_path, "r", encoding="utf-8") as f:
        intents = json.load(f)

    if intent_name in intents:
        # Varyasyon olarak ekle
        if phrase not in intents[intent_name]:
            intents[intent_name].append(phrase)
            print(f"'{phrase}' cümlesi '{intent_name}' intentine varyasyon olarak eklendi.")
    else:
        # Yeni intent oluştur
        intents[intent_name] = [phrase]
        print(f"'{intent_name}' adında yeni intent oluşturuldu. İlk varyasyon: '{phrase}'")

    # intents.json güncelle
    with open(intents_path, "w", encoding="utf-8") as f:
        json.dump(intents, f, ensure_ascii=False, indent=4)