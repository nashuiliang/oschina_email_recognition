#!/usr/bin/env python
# coding=utf-8

# import logging
import os
import random

import matplotlib.pyplot as plt
import scipy.misc
import numpy as np


base_path = os.path.dirname(__file__)


def get_image_binaryzation(image):
    return (image > 0).astype(np.int16)


def get_image_segmentation(image):
    """
    :params image numpy.ndarray

    :returns list: [((x_start, x_end), image), ((x_start, x_end), image)]
    """

    segmentation = list()
    seg_start = False

    for column_no, column in enumerate(image.T):
        seg_end = np.count_nonzero(column) is not 0
        if seg_end != seg_start:
            segmentation.append(column_no)
        seg_start = seg_end
    return [((x_start, x_end), image[:, x_start:x_end])
            for x_start, x_end in zip(segmentation[0:][::2], segmentation[1:][::2])]


def get_all_template_image(path):
    """
    :params path string

    :returns dict: {"image_text": (image_shape, image)}
    """
    all_tempalte_image = {}
    for image_name in os.listdir(path):
        image_text = ".".join(image_name.split(".")[:-1])[2:]
        image = scipy.misc.imread(os.path.join(path, image_name))
        all_tempalte_image[image_text] = (image.shape, get_image_binaryzation(image))
    return all_tempalte_image


def get_most_similarity_text(image, all_tempalte_image, max_distance=3):
    """
    :params image numpy.ndarray: raw image
    :params all_tempalte_image dict: {"image_text": (image_shape, image)}
    :params max_distance integer: max distance

    :returns string/None
    """
    image_shape = image.shape
    distance_list = []
    for image_text, data in all_tempalte_image.iteritems():
        if image_shape == data[0]:
            distance = np.sqrt(np.sum((image - data[1]) ** 2))
            if distance <= max_distance:
                distance_list.append((distance, image_text))
    if distance_list:
        sorted_distance_list = sorted(distance_list, key=lambda x: x[0])
        return sorted_distance_list[0][1]


def render_image(image, marks, **args):
    """ render image
    :params image numpy.ndarray: render image
    :params marks list: [(x_coord, mark_text), (x_coord, mark_text)]
    """
    fig = plt.figure()
    ax = fig.add_subplot(111)

    if args and "title" in args:
        plt.title(args["title"])

    for index, data in enumerate(marks):
        mark_x_coord, mark_text = data
        color = "white"
        if not mark_text:
            mark_text = "?"
            color = "red"
        ax.text(mark_x_coord, 25, mark_text, bbox={'facecolor': color})
        ax.text(mark_x_coord, -6, index, bbox={'facecolor': color})
    plt.imshow(image, cmap='Greys', interpolation='nearest')
    plt.show()


def save_template_image(image, path, gray_value=140):
    """ Beautify the template image

    :params image numpy.ndarray: save image
    :params path string: image save path
    :params gray_value int: gray value (1 => gray_value)
    """
    save_image = np.ones(image.shape, dtype=np.int16) * gray_value * image
    scipy.misc.imsave(path, save_image)


def main():
    all_tempalte_image = get_all_template_image(os.path.join(base_path, "t"))

    all_image_name = os.listdir(os.path.join(base_path, "oschina_all_gif"))
    while True:
        image_name = random.choice(all_image_name)
        base_image_path = os.path.join(base_path, "oschina_all_gif", image_name)
        image = scipy.misc.imread(base_image_path)

        # :returns list: [((x_start, x_end), image), ((x_start, x_end), image)]
        image_segmentation = get_image_segmentation(get_image_binaryzation(image))

        # get marks
        marks_list = []
        for image_seg_item in image_segmentation:
            marks_list.append(
                (image_seg_item[0][0],
                 get_most_similarity_text(image_seg_item[1], all_tempalte_image)))

        # render image
        render_image(image, marks_list, title=image_name)

        for text_item in raw_input("Yes/is: ").split():
            image_index, view_text = text_item.split(",")
            image_index = int(image_index)
            view_text = view_text.strip()

            modify_image = image_segmentation[image_index][1]
            all_tempalte_image[view_text] = modify_image
            save_template_image(
                modify_image, os.path.join(base_path, "t", "t_{}.gif".format(view_text)))


def test():
    all_tempalte_image = get_all_template_image(os.path.join(base_path, "t"))

    image_name = "838.gif"
    base_image_path = os.path.join(base_path, "oschina_all_gif", image_name)
    image = scipy.misc.imread(base_image_path)

    # :returns list: [((x_start, x_end), image), ((x_start, x_end), image)]
    image_segmentation = get_image_segmentation(get_image_binaryzation(image))

    # get marks
    marks_list = []
    for image_seg_item in image_segmentation:
        marks_list.append(
            (image_seg_item[0][0],
                get_most_similarity_text(image_seg_item[1], all_tempalte_image)))

    # render image
    render_image(image, marks_list, title=image_name)

    for text_item in raw_input("Yes/is: ").split():
        image_index, view_text = text_item.split(",")
        image_index = int(image_index)
        view_text = view_text.strip()

        modify_image = image_segmentation[image_index][1]
        all_tempalte_image[view_text] = modify_image
        save_template_image(
            modify_image, os.path.join(base_path, "t", "t_{}.gif".format(view_text)))

if __name__ == "__main__":
    # test()
    main()
