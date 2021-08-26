#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import numpy as np
import pandas as pd
import d8
from d8.image_classification import Dataset as ImgClsDataset
from d8.object_detection import Dataset as ObjDetDataset


# In[ ]:


# root is the destination of written images
ROOT = '/tmp/efficient_autocv_benchmark'


# ### Image Classification Public Set

# In[ ]:


url = 'https://raw.githubusercontent.com/zhreshold/efficient-autocv-benchmark/master/benchmark/img_cls_public.txt'
df = pd.read_csv(url, header=None)


# In[ ]:


def prepare_images_classification(dataset):
    ds = ImgClsDataset.get(dataset)
    new_root = os.path.join(ROOT, dataset)
    os.makedirs(new_root, exist_ok=True)
    f = ds.df.columns.get_loc('file_path')
    l = ds.df.columns.get_loc('class_name')
    size = len(ds.df)
    f_format = "{:0" + str(int(np.ceil(np.log10(size))) + 1) + "d}"
    for element in ds.df.iterrows():
        path = element[1][f].absolute()
        new_name = f_format.format(int(element[0])) + path.suffix
        new_path = os.path.join(new_root, new_name)
        new_relative = os.path.join(dataset, new_name)
        with open(new_path, 'wb') as fout:
            fout.write(ds.reader.open(element[1][f]).read())


# In[ ]:


for i, (dataset,) in df.iterrows():
    print('processing:', dataset, '->', i+1, '/', len(df))
    prepare_images_classification(dataset)


# ### Object Detection Public Set

# In[ ]:


url = 'https://raw.githubusercontent.com/zhreshold/efficient-autocv-benchmark/master/benchmark/obj_det_public.txt'
df = pd.read_csv(url, header=None)


# In[ ]:


def prepare_images_detection(dataset):
    ds = ObjDetDataset.get(dataset)
    new_root = os.path.join(ROOT, dataset)
    os.makedirs(new_root, exist_ok=True)
    unique_images = ds.df.groupby('file_path')
    size = len(unique_images)
    f_format = "{:0" + str(int(np.ceil(np.log10(size))) + 1) + "d}"
    for i, element in enumerate(unique_images):
        path = element[0]
        suffix = '.' + path.split('.')[-1]
        new_name = f_format.format(int(i)) + suffix
        assert suffix.lower() in ('.png', '.jpg', '.jpeg', '.gif'), suffix
        new_path = os.path.join(new_root, new_name)
        new_relative = os.path.join(dataset, new_name)
        with open(new_path, 'wb') as fout:
            fout.write(ds.reader.open(element[0]).read())


# In[ ]:


for i, (dataset,) in df.iterrows():
    print('processing:', dataset, '->', i+1, '/', len(df))
    prepare_images_detection(dataset)


# In[ ]:




