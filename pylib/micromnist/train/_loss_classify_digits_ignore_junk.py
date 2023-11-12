from keras.losses import categorical_crossentropy
import tensorflow as tf
from tensorflow import Tensor


def loss_classify_digits_ignore_junk(y_true: Tensor, y_pred: Tensor) -> Tensor:
    """
    Compute a loss that penalizes digit mis-classification and all activations for non-digit images.

    Parameters
    ----------
    y_true : Tensor
        The true labels.
    y_pred : Tensor
        The predicted labels.

    Returns
    -------
    Tensor
        The calculated loss, combining regular digit classification loss and
        a separate penalty for junk images.
    """
    # Check if the label is for junk images
    is_junk = tf.reduce_all(tf.equal(y_true, 10), axis=-1)
    # Convert is_junk to a boolean tensor
    is_junk = tf.cast(is_junk, tf.bool)

    mnist_loss = categorical_crossentropy(y_true, y_pred)
    # Penalize high activations for junk images
    junk_loss = tf.reduce_max(y_pred, axis=-1)

    # Use tf.where to select the appropriate loss
    return tf.where(is_junk, junk_loss, mnist_loss)
