#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@license : (C) Copyright 2022-2025.
@Project : lmtools
@Time : 2024 6月 29 11:42
@Author : xushiyin
@Mobile : 18682193124
@File : empty.py
@desc :
"""
import io

from streamlit_extras.grid import grid
import streamlit as st
from PIL import Image
from loguru import logger
from rembg import remove, new_session

ModelDict = {
    '通用': 'u2net',
    '人类': 'u2net_human_seg',
    '衣服': 'u2net_cloth_seg',
    '通用新': 'isnet-general-use',
}


def get_model_session(m_name: str):
    return new_session(model_name=m_name)


# side
with st.sidebar:
    model_select = st.selectbox(
        '选择模型',
        [v for v in ModelDict.keys()],
        index=0,
        help='选择合适的模型去背景'
    )

# main
layout_grid = grid(2,1,1, gap='medium', vertical_align='center')


upload_rbg_img = layout_grid.file_uploader(
    "上传图片",
    key='upload_rbg_img_lm_tool',
    accept_multiple_files=False,
    type=["png", "jpg", "jpeg"],
    help='上传单张图片, 支持图片格式: png, jpg, jpeg'
)

start_btn = layout_grid.button(label='去背景', use_container_width=True)


if upload_rbg_img is not None:
    layout_grid.image(upload_rbg_img.read(), caption='原始图片')

if start_btn and upload_rbg_img is not None:
    with st.spinner('AI is doing the magic!'):
        model_name = ModelDict[model_select]
        logger.info(f'select model: {model_name}')
        sess = get_model_session(m_name=model_name)
        img_input = Image.open(io.BytesIO(upload_rbg_img.getvalue()))
        pil_img = remove(img_input, session=sess, model_path=f'./assets/rm_bg/{model_name}.onnx')

    layout_grid.image(pil_img, caption='去背景图片')

    img_path_parts = upload_rbg_img.name.rsplit('.', maxsplit=1)

    rbg_name = img_path_parts[0] + '_rbg.png'

    logger.info(f'rbg name: {rbg_name}')

    pil_img.save(rbg_name, format='PNG')

    # layout_grid.download_button(
    #     label='图片下载',
    #     data=pil_img.tobytes('JPEG'),
    #     key='download_rbg_img_lm_tool',
    #     file_name=rbg_name,
    #     fmt="jpg",
    #     use_container_width=True
    # )
