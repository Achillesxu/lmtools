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
import streamlit as st

from rembg import remove, new_session
import cv2

ModelDict = {
    '通用': 'u2net',
    '人类': 'u2net_human_seg',
    '衣服': 'u2net_cloth_seg',
    '通用小': 'silueta',
    '通用新': 'isnet-general-use',
}

def get_model_session(m_name:str):
    new_session(model_name=ModelDict[m_name], )

# side
with st.sidebar:
    model_select = st.selectbox(
        '选择模型',
        [v for v in ModelDict.values()],
        index=0,
        help='选择合适的模型去背景'
    )

# main
upload_rbg_img = st.file_uploader(
    "上传图片",
    key='upload_rbg_img_lm_tool',
    accept_multiple_files=False,
    type=["png", "jpg", "jpeg"],
    help='上传单张图片, 支持图片格式: png，jpg，jpeg'
)

if upload_rbg_img is not None:
    st.image(upload_rbg_img.read(), caption='原始图片')

    with st.spinner('AI is doing the magic!'):
        output = remove(upload_rbg_img.read(), )

    st.image(output, caption='去背景图片')

