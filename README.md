<h1 align="center">LmTools</h1>
<p align="center">A free and open-source toolbox for Liu Meng</p>


## Feature
- Completely free and open-source, fully self-hosted, only GPU
  1. image object remove (github [model](https://github.com/advimman/lama?tab=readme-ov-file))

## Quick Start

### Start lmtools

In order to use GPU, install cuda version of pytorch first.
pip3 install torch==2.3.1 torchvision==0.18.1 --index-url https://download.pytorch.org/whl/cu121

```bash
# In order to use GPU, install cuda version of pytorch first.
# pip3 install torch==2.3.1 torchvision==0.18.1 --index-url https://download.pytorch.org/whl/cu121

git clone https://github.com/Achillesxu/lmtools/tree/master
cd assets
# downloads model 
git lfs pull

pyenv virtualenv 3.10.12 lmtools
source .../.virtualenvs/lmtools/bin/activate
python -m pip install requirements.txt

streamlit run app.py
```
That's it, you can start using lmtools by visiting http://localhost:8501 in your web browser.
