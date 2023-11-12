import typing

import numpy as np
import tensorflow as tf
from tensorflow.keras.datasets import mnist as keras_mnist
from tensorflow.keras.utils import to_categorical as keras_to_categorical


def load_mnist() -> (
    typing.Tuple[
        typing.Tuple[np.ndarray, np.ndarray],
        typing.Tuple[np.ndarray, np.ndarray],
        typing.Tuple[int, int, int],
    ]
):
    # adapted from https://github.com/ruslangrimov/mnist-minimal-model/blob/37935b520ae8d59df67a23151d0516a54aca6913/keras_cnn_test.py
    img_rows, img_cols = 28, 28
    num_classes = 10
    (x_train, y_train), (x_test, y_test) = keras_mnist.load_data()

    if tf.keras.backend.image_data_format() == "channels_first":
        x_train = x_train.reshape(x_train.shape[0], 1, img_rows, img_cols)
        x_test = x_test.reshape(x_test.shape[0], 1, img_rows, img_cols)
        input_shape = (1, img_rows, img_cols)
    else:
        x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)
        x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)
        input_shape = (img_rows, img_cols, 1)

    x_train = x_train.astype("float32") / 255
    x_test = x_test.astype("float32") / 255

    y_train = keras_to_categorical(y_train, num_classes)
    y_test = keras_to_categorical(y_test, num_classes)

    return (x_train, y_train), (x_test, y_test), input_shape
