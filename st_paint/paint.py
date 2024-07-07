# -*- coding: utf-8 -*-
"""
@Time : 2024 7月 01 20:47
@Author : xushiyin
@Mobile : 18682193124
@desc :
"""
import time

import cv2  # noqa
import numpy as np
import torch

device = torch.device("cuda")
model_path = "./assets/big-lama.pt"
model = torch.jit.load(model_path, map_location=device)
model = model.to(device)
model.eval()


def norm_img(np_img):
    if len(np_img.shape) == 2:
        np_img = np_img[:, :, np.newaxis]
    np_img = np.transpose(np_img, (2, 0, 1))
    np_img = np_img.astype("float32") / 255
    return np_img


def resize_max_size(
        np_img, size_limit: int, interpolation=cv2.INTER_CUBIC
) -> np.ndarray:
    # Resize image's longer size to size_limit if longer size larger than size_limit
    h, w = np_img.shape[:2]
    if max(h, w) > size_limit:
        ratio = size_limit / max(h, w)
        new_w = int(w * ratio + 0.5)
        new_h = int(h * ratio + 0.5)
        return cv2.resize(np_img, dsize=(new_w, new_h), interpolation=interpolation)
    else:
        return np_img


def ceil_modulo(x, mod):
    if x % mod == 0:
        return x
    return (x // mod + 1) * mod


def pad_img_to_modulo(img, mod):
    channels, height, width = img.shape
    out_height = ceil_modulo(height, mod)
    out_width = ceil_modulo(width, mod)
    return np.pad(
        img,
        ((0, 0), (0, out_height - height), (0, out_width - width)),
        mode="symmetric",
    )


def run(image, mask):
    """
    image: [C, H, W]
    mask: [1, H, W]
    return: BGR IMAGE
    """
    origin_height, origin_width = image.shape[1:]
    image = pad_img_to_modulo(image, mod=8)
    mask = pad_img_to_modulo(mask, mod=8)

    mask = (mask > 0) * 1
    image = torch.from_numpy(image).unsqueeze(0).to(device)
    mask = torch.from_numpy(mask).unsqueeze(0).to(device)

    start = time.time()
    with torch.no_grad():
        inpainted_image = model(image, mask)

    print(f"process time: {(time.time() - start) * 1000}ms")
    cur_res = inpainted_image[0].permute(1, 2, 0).detach().cpu().numpy()
    cur_res = cur_res[0:origin_height, 0:origin_width, :]
    cur_res = np.clip(cur_res * 255, 0, 255).astype("uint8")
    cur_res = cv2.cvtColor(cur_res, cv2.COLOR_BGR2RGB)
    return cur_res


def paint_process(image, mask):
    image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
    original_shape = image.shape
    interpolation = cv2.INTER_CUBIC

    size_limit = max(image.shape)

    print(f"Origin image shape: {original_shape}")
    image = resize_max_size(image, size_limit=size_limit, interpolation=interpolation)
    print(f"Resized image shape: {image.shape}")
    image = norm_img(image)

    mask = 255 - mask[:, :, 3]

    mask = resize_max_size(mask, size_limit=size_limit, interpolation=interpolation)
    mask = norm_img(mask)

    res_np_img = run(image, mask)

    return cv2.cvtColor(res_np_img, cv2.COLOR_BGR2RGB)
