from contextlib import contextmanager
import random

import numpy as np
import tensorflow as tf


@contextmanager
def reproducible_context(seed: int = 1, op_determinism: bool = False) -> None:
    # Set the seed using keras.utils.set_random_seed. This will set:
    # 1) `numpy` seed
    # 2) `tensorflow` random seed
    # 3) `python` random seed
    # https://keras.io/examples/keras_recipes/reproducibility_recipes/

    np_state = np.random.get_state()
    python_state = random.getstate()
    tf_state = tf.random.get_global_generator().state

    # This will make TensorFlow ops as deterministic as possible, but it will
    # affect the overall performance, so it's not enabled by default.
    # `enable_op_determinism()` is introduced in TensorFlow 2.9.
    if op_determinism:
        tf_determinism_state = tf.config.deterministic_ops_enabled()
        tf.config.experimental.enable_op_determinism()

    try:
        yield
    finally:
        # Restore the saved state
        np.random.set_state(np_state)
        random.setstate(python_state)
        tf.random.get_global_generator().reset_from_seed(tf_state[0])
        if op_determinism and not tf_determinism_state:
            tf.config.experimental.enable_op_determinism(False)
