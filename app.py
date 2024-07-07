#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@license : (C) Copyright 2022-2025.
@Project : lmtools
@Time : 2024 6月 29 11:05
@Author : xushiyin
@Mobile : 18682193124
@File : main.py
@desc :
"""
import streamlit as st
from pathlib import Path

st.set_page_config(layout="wide")

pages = {
    '图像处理': [
        st.Page(Path('spages/images_remove_object.py'), title='删除图像对象', icon='🆑'),
        st.Page(Path('spages/empty.py'), title='', icon='🆑')
    ]
}

pg = st.navigation(pages)
pg.run()
