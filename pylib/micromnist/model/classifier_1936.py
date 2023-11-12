"""Adapted from https://github.com/ruslangrimov/mnist-minimal-model."""

import numpy as np
import tensorflow as tf
from tensorflow.keras.datasets import mnist
from tensorflow.keras.layers import (
    Activation,
    Conv2D,
    Dense,
    Dropout,
    GlobalAveragePooling2D,
    Input,
    LayerNormalization,
    MaxPooling2D,
    SeparableConv2D,
)
from tensorflow.keras.models import Model as keras_Model

from ...auxlib import load_mnist, reproducible_context
from ..train import loss_classify_digits_ignore_junk
from ..train import generate_training_set_incl_junk


def _dw_block(sh_l, prev_l) -> tf.Tensor:
    l = sh_l(prev_l)
    l = Activation(activation="relu")(l)
    l = LayerNormalization()(l)
    l = Dropout(rate=0.1)(l)
    return l


@reproducible_context()
def configured() -> keras_Model:
    num_classes = 10
    __, __, input_shape = load_mnist()

    inputs = Input(shape=input_shape)
    l = inputs

    l = Conv2D(8, (3, 3), padding="same")(l)
    l = Activation("relu")(l)
    l = LayerNormalization()(l)
    l = MaxPooling2D((2, 2))(l)
    l = Dropout(0.1)(l)

    l = SeparableConv2D(26, (3, 3), padding="same", depth_multiplier=1)(l)
    l = Activation("relu")(l)
    l = LayerNormalization()(l)
    l = Dropout(0.1)(l)

    sh_l = SeparableConv2D(26, (3, 3), padding="same", depth_multiplier=1)

    for n in range(3):
        l = _dw_block(sh_l, l)

    l = GlobalAveragePooling2D()(l)

    l = Dense(16, activation="relu")(l)
    l = LayerNormalization()(l)
    l = Dropout(0.1)(l)
    l = Dense(num_classes, activation="softmax")(l)

    return keras_Model(inputs, l)


@reproducible_context()
def compiled() -> keras_Model:
    model = configured()
    model.compile(
        optimizer="adam",
        loss=loss_classify_digits_ignore_junk,
        metrics=["accuracy"],
    )
    return model


# TODO: add persistent caching?
@reproducible_context()
def trained(num_epochs: int = 5) -> keras_Model:
    model = compiled()

    # must pretrain model to prevent nan loss
    print(f"conditioning model")
    ((x_train, y_train), _test, __) = load_mnist()
    if num_epochs == 0:  # for testing
        x_train, y_train = x_train[:100], y_train[:100]
    model.fit(x_train, y_train, epochs=2, batch_size=32)

    print(f"training model")

    for epoch in range(max(num_epochs, 1)):
        print(f"epoch {epoch} / {num_epochs}")
        x_train_, y_train_ = generate_training_set_incl_junk(n=50000)
        # Shuffle the training data
        indices = np.arange(len(x_train_))
        np.random.shuffle(indices)
        x_train_, y_train_ = x_train_[indices], y_train_[indices]

        if num_epochs == 0:  # for testing
            x_train_, y_train_ = x_train_[:100], y_train_[:100]

        model.fit(
            x_train_,
            y_train_,
            epochs=num_epochs,
            batch_size=32,
        )
