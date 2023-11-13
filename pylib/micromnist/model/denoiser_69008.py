# adapted from https://github.com/wikibook/keras/blob/bce4a014097f7ed3fb5bb63ce3b29a50a47f914c/chapter3-autoencoders/denoising-autoencoder-mnist-3.3.1.py
"""Trains a denoising autoencoder on MNIST dataset.

Denoising is one of the classic applications of autoencoders.
The denoising process removes unwanted noise that corrupted the
true signal.

Noise + Data ---> Denoising Autoencoder ---> Data

Given a training dataset of corrupted data as input and
true signal as output, a denoising autoencoder can recover the
hidden structure to generate clean data.

This example has modular design. The encoder, decoder and autoencoder
are 3 models that share weights. For example, after training the
autoencoder, the encoder can be used to generate latent vectors
of input data for low-dim visualization like PCA or TSNE.
"""

from PIL import Image
from keras.layers import (
    Conv2D,
    Conv2DTranspose,
    Dense,
    Flatten,
    Input,
    Reshape,
)
from keras.models import Model as keras_Model
from keras import backend as keras_backend
from keras.datasets import mnist
import numpy as np
from matplotlib import pyplot as plt

from ...auxlib import load_mnist, reproducible_context
from ..train import generate_training_set_corrupted


@reproducible_context()
def configured() -> keras_Model:
    # network parameters
    image_size = 28
    input_shape = (image_size, image_size, 1)
    kernel_size = 3
    latent_dim = 16
    # encoder/decoder number of CNN layers and filters per layer
    layer_filters = [32, 64]

    # build the autoencoder model
    # first build the encoder model
    inputs = Input(shape=input_shape, name="encoder_input")
    x = inputs
    # stack of Conv2D(32)-Conv2D(64)
    for filters in layer_filters:
        x = Conv2D(
            filters=filters,
            kernel_size=kernel_size,
            strides=2,
            activation="relu",
            padding="same",
        )(x)

    # shape info needed to build decoder model so we don't do hand computation
    # the input to the decoder's first Conv2DTranspose will have this shape
    # shape is (7, 7, 64) which can be processed by the decoder back to (28, 28, 1)
    shape = keras_backend.int_shape(x)

    # generate the latent vector
    x = Flatten()(x)
    latent = Dense(latent_dim, name="latent_vector")(x)

    # instantiate encoder model
    encoder = keras_Model(inputs, latent, name="encoder")

    # build the decoder model
    latent_inputs = Input(shape=(latent_dim,), name="decoder_input")
    # use the shape (7, 7, 64) that was earlier saved
    x = Dense(shape[1] * shape[2] * shape[3])(latent_inputs)
    # from vector to suitable shape for transposed conv
    x = Reshape((shape[1], shape[2], shape[3]))(x)

    # stack of Conv2DTranspose(64)-Conv2DTranspose(32)
    for filters in layer_filters[::-1]:
        x = Conv2DTranspose(
            filters=filters,
            kernel_size=kernel_size,
            strides=2,
            activation="relu",
            padding="same",
        )(x)

    # reconstruct the denoised input
    outputs = Conv2DTranspose(
        filters=1,
        kernel_size=kernel_size,
        padding="same",
        activation="sigmoid",
        name="decoder_output",
    )(x)

    # instantiate decoder model
    decoder = keras_Model(latent_inputs, outputs, name="decoder")

    # autoencoder = encoder + decoder
    # instantiate autoencoder model
    autoencoder = keras_Model(
        inputs, decoder(encoder(inputs)), name="autoencoder"
    )

    return autoencoder


@reproducible_context()
def compiled() -> keras_Model:
    model = configured()
    # Mean Square Error (MSE) loss function, Adam optimizer
    model.compile(loss="mse", optimizer="adam")
    return model


def train(model: keras_Model, num_epochs: int = 10) -> None:
    for epoch in range(max(num_epochs, 1)):
        print(f"epoch {epoch} / {num_epochs}")
        x_train, x_train_noisy = generate_training_set_corrupted()
        if num_epochs == 0:  # for testing
            x_train, x_train_noisy = x_train[:100], x_train_noisy[:100]
        model.fit(
            x_train_noisy,
            x_train,
            epochs=num_epochs,
            batch_size=32,
        )


@reproducible_context()
def trained(num_epochs: int = 5) -> keras_Model:
    model = compiled()
    train(model, num_epochs)
    return model


def demonstrate(model: keras_Model) -> None:
    x_train, x_train_noisy = generate_training_set_corrupted()

    # predict the autoencoder output from corrupted test images
    x_decoded = model.predict(x_train_noisy)

    # 3 sets of images with 9 MNIST digits
    # 1st rows - original images
    # 2nd rows - images corrupted by noise
    # 3rd rows - denoised images
    rows, cols = 3, 9
    image_size = 28
    num = rows * cols
    imgs = np.concatenate([x_train[:num], x_train_noisy[:num], x_decoded[:num]])
    imgs = imgs.reshape((rows * 3, cols, image_size, image_size))
    imgs = np.vstack(np.split(imgs, rows, axis=1))
    imgs = imgs.reshape((rows * 3, -1, image_size, image_size))
    imgs = np.vstack([np.hstack(i) for i in imgs])
    imgs = (imgs * 255).astype(np.uint8)

    plt.figure()
    plt.axis("off")
    plt.title(
        "Original images: top rows, "
        "Corrupted Input: middle rows, "
        "Denoised Input:  third rows"
    )
    plt.imshow(imgs, interpolation="none", cmap="gray")
    Image.fromarray(imgs).save("corrupted_and_denoised.png")
    plt.show()
