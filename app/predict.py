from urllib.request import urlopen
from datetime import datetime

import tensorflow as tf

from PIL import Image
import numpy as np

filename = "model.pb"
labels_filename = "labels.txt"

# network_input_size = 0

output_layer = "loss:0"
input_node = "Placeholder:0"

# graph_def = tf.GraphDef()
graph_def = tf.compat.v1.GraphDef()
labels = []


def initialize():
    print("Loading model...", end=""),
    with tf.io.gfile.GFile(filename, "rb") as f:
        graph_def.ParseFromString(f.read())
        tf.import_graph_def(graph_def, name="")

    # Retrieving 'network_input_size' from shape of 'input_node'
    with tf.compat.v1.Session() as sess:
        input_tensor_shape = sess.graph.get_tensor_by_name(input_node).shape.as_list()

    assert len(input_tensor_shape) == 4
    assert input_tensor_shape[1] == input_tensor_shape[2]

    global network_input_size
    network_input_size = input_tensor_shape[1]

    print("Success!")
    print("Loading labels...", end="")
    with open(labels_filename, "rt") as lf:
        global labels
        labels = [label.strip() for label in lf.readlines()]

    tf.compat.v1.reset_default_graph()
    tf.import_graph_def(graph_def, name="")

    print(len(labels), "found. Success!")


def log_msg(msg):
    print("{}: {}".format(datetime.now(), msg))


def crop_center(img, cropx, cropy):
    h, w = img.shape[:2]
    startx = max(0, w // 2 - (cropx // 2))
    starty = max(0, h // 2 - (cropy // 2))
    log_msg(
        "crop_center: " + str(w) + "x" + str(h) + " to " + str(cropx) + "x" + str(cropy)
    )
    return img[starty : starty + cropy, startx : startx + cropx]


def resize_down_to_1600_max_dim(image):
    w, h = image.size
    if h < 1600 and w < 1600:
        return image

    new_size = (1600 * w // h, 1600) if (h > w) else (1600, 1600 * h // w)
    log_msg(
        "resize: "
        + str(w)
        + "x"
        + str(h)
        + " to "
        + str(new_size[0])
        + "x"
        + str(new_size[1])
    )
    if max(new_size) / max(image.size) >= 0.5:
        method = Image.BILINEAR
    else:
        method = Image.BICUBIC
    return image.resize(new_size, method)


def predict_url(imageUrl):
    log_msg("Predicting from url: " + imageUrl)
    with urlopen(imageUrl) as testImage:
        image = Image.open(testImage)
        return predict_image(image)


def convert_to_nparray(image):
    # RGB -> BGR
    log_msg("Convert to numpy array")
    image = np.array(image)
    return image[:, :, (2, 1, 0)]


def update_orientation(image):
    exif_orientation_tag = 0x0112
    if hasattr(image, "_getexif"):
        exif = image._getexif()
        if exif != None and exif_orientation_tag in exif:
            orientation = exif.get(exif_orientation_tag, 1)
            log_msg("Image has EXIF Orientation: " + str(orientation))
            # orientation is 1 based, shift to zero based and flip/transpose based on 0-based values
            orientation -= 1
            if orientation >= 4:
                image = image.transpose(Image.TRANSPOSE)
            if (
                orientation == 2
                or orientation == 3
                or orientation == 6
                or orientation == 7
            ):
                image = image.transpose(Image.FLIP_TOP_BOTTOM)
            if (
                orientation == 1
                or orientation == 2
                or orientation == 5
                or orientation == 6
            ):
                image = image.transpose(Image.FLIP_LEFT_RIGHT)
    return image


def predict_image(image):

    log_msg("Predicting image")
    try:
        if image.mode != "RGB":
            log_msg("Converting to RGB")
            image = image.convert("RGB")

        w, h = image.size
        log_msg("Image size: " + str(w) + "x" + str(h))

        # Update orientation based on EXIF tags
        image = update_orientation(image)

        # If the image has either w or h greater than 1600 we resize it down respecting
        # aspect ratio such that the largest dimention is 1600
        image = resize_down_to_1600_max_dim(image)

        # Convert image to numpy array
        image = convert_to_nparray(image)

        # Crop the center square and resize that square down to 256x256
        # resized_image = extract_and_resize_to_256_square(image)
        resized_image = tf.image.resize(image, [256, 256])

        # Crop the center for the specified network_input_Size
        cropped_image = crop_center(
            resized_image, network_input_size, network_input_size
        )

        with tf.compat.v1.Session() as sess:
            prob_tensor = sess.graph.get_tensor_by_name(output_layer)
            (predictions,) = sess.run(prob_tensor, {input_node: [cropped_image]})

            result = []
            for p, label in zip(predictions, labels):
                truncated_probablity = np.float64(round(p, 8))
                if truncated_probablity > 1e-8:
                    result.append(
                        {
                            "tagName": label,
                            "probability": truncated_probablity,
                            "tagId": "",
                            "boundingBox": None,
                        }
                    )

            response = {
                "id": "",
                "project": "",
                "iteration": "",
                "created": datetime.utcnow().isoformat(),
                "predictions": result,
            }

            log_msg("Results: " + str(response))
            return response

    except Exception as e:
        log_msg(str(e))
        return "Error: Could not preprocess image for prediction. " + str(e)

