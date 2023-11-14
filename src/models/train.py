import os
import numpy as np
from keras.callbacks import TensorBoard
from keras.layers import LSTM, Dense
from keras.models import Sequential
from sklearn.metrics import multilabel_confusion_matrix, accuracy_score
from ..utils.index import actions
from ..data.preprocess import X_train, y_train, X_test, y_test, X_val, y_val

log_dir = os.path.join('Logs')
tb_callback = TensorBoard(log_dir)

model = Sequential([
    LSTM(64, return_sequences=True, input_shape=(30, 1662)),
    LSTM(64),
    Dense(3, activation='softmax')
])

model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['categorical_accuracy'])
# Including validation data in training
model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_val, y_val), callbacks=[tb_callback])
model.summary()

res = model.predict(X_test)
print(actions[np.argmax(res[4])])
print(actions[np.argmax(y_test[4])])

model.save('model')

yhat = model.predict(X_test)
ytrue = np.argmax(y_test, axis=1).tolist()
yhat = np.argmax(yhat, axis=1).tolist()

print(multilabel_confusion_matrix(ytrue, yhat))
print(accuracy_score(ytrue, yhat))