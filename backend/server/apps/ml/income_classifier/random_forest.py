import joblib
import pandas as pd


class RandomForestClassifier:
    def __init__(self):
        path_to_artifacts = "../../research/"

        self.values_fill_missing = joblib.load(path_to_artifacts + "train_mode.joblib")
        self.encoders = joblib.load(path_to_artifacts + "encoders.joblib")
        self.model = joblib.load(path_to_artifacts + "random_forest.joblib")

    def preprocessing(self, input_data):
        input_data = pd.DataFrame(input_data, index=[0])
        input_data.fillna(self.values_fill_missing)
        for col in [
            "workclass",
            "education",
            "marital-status",
            "occupation",
            "relationship",
            "race",
            "sex",
            "native-country",
        ]:
            categorical_convert = self.encoders[col]
            input_data[col] = categorical_convert.transform(input_data[col])

        return input_data

    def predict(self, input_data):
        return self.model.predict_proba(input_data)

    def postprocessing(self, input_data):
        label = "<=50k"
        if input_data[1] > 0.5:
            label = ">50k"
        return {"probability": input_data[1], "label": label, "status": "OK"}

    def compute_prediction(self, input_data):
        try:
            input_data = self.preprocessing(input_data)
            prediction = self.predict(input_data)[0]
            prediction = self.postprocessing(prediction)
        except Exception as e:
            return {"status": "Error", "message": str(e)}
        return prediction
