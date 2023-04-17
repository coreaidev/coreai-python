# Core AI
Core training & inference utilities

# Google Colab Quickstart
This library is intended for use within Google Colab.  An example involving the loading of a dataset
can be found here: 
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1zzHewvLl79HmEBtCqA-A_Aa44dpLi_xZ?usp=sharing)

## Create Core AI Environment
Install the library, create a new CoreAI Environment within Google Colab, and activate the environment.
This will display a blue activate button, click the link to activate on coreai.dev, and then close the window
when you're done.

```python
!pip install -i https://pypi.coreai.dev coreai
from coreai import *
environment = CoreAI.create_environment(EnvironmentType.GOOGLE_COLAB, 0.5)
environment.activate()
```

## Render ten images from the dataset
```python
import random
import urllib
from matplotlib import pyplot as plt

# Load the images from the coreai
dataset = environment.datasets.sample.dragons

dataset.select(1)

# Select 10 random images from the dataset
images = [dataset.select(random.randrange(0,len(dataset))) for x in range(0,10)]

# Plot the images
fig, axs = plt.subplots(1, len(images), figsize=(20, 20))
for i, image in enumerate(images):
    axs[i].imshow(image)
    axs[i].axis('off')
```

