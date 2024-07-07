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
import io
import os
from copy import deepcopy

import numpy as np
import streamlit as st
from PIL import Image  # noqa
from streamlit_drawable_canvas import st_canvas

from st_paint import paint_process


def image_download_button(pil_image, filename: str, fmt: str, label="Download"):
    if fmt not in ["jpg", "png"]:
        raise Exception(f"Unknown image format (Available: {fmt} - case sensitive)")

    pil_format = "JPEG" if fmt == "jpg" else "PNG"
    file_format = "jpg" if fmt == "jpg" else "png"
    mime = "image/jpeg" if fmt == "jpg" else "image/png"

    buf = io.BytesIO()
    pil_image.save(buf, format=pil_format)

    return st.download_button(
        label=label,
        data=buf.getvalue(),
        file_name=f'{filename}.{file_format}',
        mime=mime,
    )


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

st_cols = st.columns(2)

with st_cols[0]:
    upload_img = st.file_uploader(
        "上传图片",
        key='upload_img_lm_tool',
        accept_multiple_files=False,
        type=["png", "jpg", "jpeg"],
        help='上传单张图片, 支持图片格式: png，jpg，jpeg'
    )

with st_cols[1]:
    stroke_width = st.slider("工具刷", 5, 50, 25, 5)

st.divider()
st.write("**没错！现在请用刷子（或涂抹工具）涂抹你想去除的图像部分.**")

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
        update_streamlit=True,
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
        im[background] = [0, 0, 0, 255]
        im[drawing] = [0, 0, 0, 0]  # RGBA

        submit_btn = st.button('Submit')

        if submit_btn:
            with st.spinner('AI is doing the magic!'):
                output = paint_process(np.array(img_input), np.array(im))
                img_output = Image.fromarray(output).convert("RGB")

            st.write("AI has finished the job!")
            st.image(img_output)

            uploaded_name = os.path.splitext(upload_img.name)[0]

            image_download_button(
                label="Download Image",
                pil_image=img_output,
                filename=uploaded_name,
                fmt="jpg",
            )
            st.info("**提示**: 如果结果不完美，你可以先下载它，然后上传，再删除这些瑕疵")
