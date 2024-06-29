#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@license : (C) Copyright 2022-2025.
@Project : lmtools
@Time : 2024 6月 29 11:20
@Author : xushiyin
@Mobile : 18682193124
@File : images_remove_object.py
@desc :
"""
from copy import deepcopy

import numpy as np
import streamlit as st
from PIL import Image  # noqa
import io

from streamlit_drawable_canvas import st_canvas

if 'reuse_image' not in st.session_state:
    st.session_state.reuse_image = None

if "button_id" not in st.session_state:
    st.session_state["button_id"] = ""

if "color_to_label" not in st.session_state:
    st.session_state["color_to_label"] = {}


def set_image(img):
    st.session_state.reuse_image = img


with st.sidebar:
    st.markdown(
        """
        想去除照片中的某个物体吗？您无需学习照片编辑技能.
        **:red[直接用笔涂抹掉照片中你想去除的部分, 我们的人工智能会帮你消除它们].**
        """
    )

upload_img = st.file_uploader(
    "上传图片",
    key='upload_img_lm_tool',
    accept_multiple_files=False,
    type=["png", "jpg", "jpeg"],
    help='上传单张图片, 支持图片格式: png，jpg，jpeg'
)

if upload_img is not None:
    if st.session_state.reuse_image is not None:
        img_input = Image.fromarray(st.session_state.reuse_image)
    else:
        bytes_data = upload_img.getvalue()
        img_input = Image.open(io.BytesIO(bytes_data)).convert("RGBA")

    # Resize the image while maintaining aspect ratio
    max_size = 2000
    img_width, img_height = img_input.size
    if img_width > max_size or img_height > max_size:
        if img_width > img_height:
            new_width = max_size
            new_height = int((max_size / img_width) * img_height)
        else:
            new_height = max_size
            new_width = int((max_size / img_height) * img_width)
        img_input = img_input.resize((new_width, new_height))

    stroke_width = st.slider("Brush size", 0, 50, 30, 5)
    st.write("**没错！现在请用刷子（或涂抹工具）涂抹你想去除的图像部分.**")

    # Canvas size logic
    canvas_bg = deepcopy(img_input)
    aspect_ratio = canvas_bg.width / canvas_bg.height
    streamlit_width = 800

    # Max width is 720. Resize the height to maintain its aspectratio.
    if canvas_bg.width > streamlit_width:
        canvas_bg = canvas_bg.resize((streamlit_width, int(streamlit_width / aspect_ratio)))

    canvas_result = st_canvas(
        stroke_color="rgba(255, 0, 255, 1)",
        stroke_width=stroke_width,
        background_image=canvas_bg,
        width=canvas_bg.width,
        height=canvas_bg.height,
        drawing_mode="freedraw",
        key="canvas_result_lm_tool",
    )

    if canvas_result.image_data is not None:
        im = np.array(Image.fromarray(canvas_result.image_data.astype(np.uint8)).resize(img_input.size))
        background = np.where(
            (im[:, :, 0] == 0) &
            (im[:, :, 1] == 0) &
            (im[:, :, 2] == 0)
        )
        drawing = np.where(
            (im[:, :, 0] == 255) &
            (im[:, :, 1] == 0) &
            (im[:, :, 2] == 255)
        )
        im[background] = [0,0,0,255]
        im[drawing] = [0,0,0,0] # RGBA

        reuse = False

        if st.button('Submit'):
            pass


