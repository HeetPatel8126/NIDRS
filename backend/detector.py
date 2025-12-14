from sklearn.ensemble import IsolationForest
import numpy as np
from collections import deque

model = IsolationForest(
    contamination=0.05,
    random_state=42
)

trained = False
buffer = deque(maxlen=200)

def process(features):
    global trained

    buffer.append(features)

    if len(buffer) < 50:
        return "LEARNING"

    X = np.array(buffer)

    if not trained:
        model.fit(X)
        trained = True
        return "MODEL_TRAINED"

    prediction = model.predict([features])[0]
    return "ANOMALY" if prediction == -1 else "NORMAL"
