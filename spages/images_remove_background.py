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


cols = st.columns(2)

with cols[0]:
    upload_rbg_img = st.file_uploader(
        "上传图片",
        key='upload_rbg_img_lm_tool',
        accept_multiple_files=False,
        type=["png", "jpg", "jpeg"],
        help='上传单张图片, 支持图片格式: png，jpg，jpeg'
    )

with cols[1]:
    start_btn = st.button(label='去背景')


if upload_rbg_img is not None and start_btn:
    st.image(upload_rbg_img.read(), caption='原始图片')

    with st.spinner('AI is doing the magic!'):
        model_name = ModelDict[model_select]
        logger.info(f'select model: {model_name}')
        sess = get_model_session(m_name=model_name)
        img_input = Image.open(io.BytesIO(upload_rbg_img.getvalue()))
        img_bytes = remove(img_input, session=sess, model_path=f'./assets/rm_bg/{model_name}.onnx')

    st.image(img_bytes, caption='去背景图片')

    rbg_name = upload_rbg_img.name.rsplit('.', maxsplit=1)[0] + '_rbg' + '.png'

    st.download_button(
        label='图片下载',
        data=Image.fromarray(img_bytes),
        key='download_rbg_img_lm_tool',
        file_name=rbg_name,
    )
