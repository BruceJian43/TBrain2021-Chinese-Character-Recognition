# Generate Fake Handwriting Images Using CycleGAN
There are three steps to generate fake handwriting images:
1. [Use Computer Fonts to Generate Images](#Use-Computer-Fonts-to-Generate-Images)
2. [Train CycleGAN](#Train-CycleGAN)
2. [Transfer Style of Images From Computer Fonts to Handwriting](#Transfer-Style-of-Images-From-Computer-Fonts-to-Handwriting)

## Requirements

Python3

Pip:

```bash
pip install numpy pillow fonttools
```

OpenCV-Python: check out [OpenCV: Introduction to OpenCV](https://docs.opencv.org/4.5.2/da/df6/tutorial_py_table_of_contents_setup.html) or [opencv-contrib-python](https://pypi.org/project/opencv-python/).

## Use Computer Fonts to Generate Images
Download all Chinese fonts we used.
```bash
bash download_fonts.sh
``` 
Before generate images, you need to create a dictionary file and one directory containing backgrounds:

```
usage: generate.py [-h] --dic DIC --background BACKGROUND

optional arguments:
  -h, --help            show this help message and exit
  --dic DIC             text file containing characters to generate.One
                        character per line
  --background BACKGROUND
                        path of the directory containing backgrounds for
                        generated images.
``` 

## Train CycleGAN
The source codes of cycleGAN and the instructions below in this repository are modified from [PyTorch-CycleGAN](https://github.com/aitorzip/PyTorch-CycleGAN).\
(In the testing part, we transfer domain A (ComputerFonts) to domain B (Handwriting) only)\
(Besides, we change the output filename with the first character of the filename being the generated character)

You should put the generated and handwriting images like the structure below.

    .
    ├── datasets                   
    |   ├── <dataset_name>         # i.e. ComputerFonts2Handwriting
    |   |   ├── train              # Training
    |   |   |   ├── A              # Contains domain A images (i.e. ComputerFonts)
    |   |   |   └── B              # Contains domain B images (i.e. Handwriting)
    |   |   └── test               # Testing
    |   |   |   ├── A              # Contains domain A images (i.e. ComputerFonts)
    |   |   |   └── B              # Contains domain B images (i.e. Handwriting)

Start to train
```
usage: ./Pytorch-CycleGAN/train [-h] [--epoch EPOCH] [--n_epochs N_EPOCHS] [--batchSize BATCHSIZE] [--dataroot DATAROOT] [--lr LR]
             [--decay_epoch DECAY_EPOCH] [--size SIZE] [--input_nc INPUT_NC] [--output_nc OUTPUT_NC] [--cuda] [--n_cpu N_CPU]

optional arguments:
  -h, --help            show this help message and exit
  --epoch EPOCH         starting epoch
  --n_epochs N_EPOCHS   number of epochs of training
  --batchSize BATCHSIZE
                        size of the batches
  --dataroot DATAROOT   root directory of the dataset
  --lr LR               initial learning rate
  --decay_epoch DECAY_EPOCH
                        epoch to start linearly decaying the learning rate to 0
  --size SIZE           size of the data crop (squared assumed)
  --input_nc INPUT_NC   number of channels of input data
  --output_nc OUTPUT_NC
                        number of channels of output data
  --cuda                use GPU computation
  --n_cpu N_CPU         number of cpu threads to use during batch generation

```
    
## Transfer Style of Images From Computer Fonts to Handwriting
```
usage: ./Pytorch-CycleGAN/test [-h] [--batchSize BATCHSIZE] [--dataroot DATAROOT] [--input_nc INPUT_NC] [--output_nc OUTPUT_NC] [--size SIZE] [--cuda]
            [--n_cpu N_CPU] [--generator_A2B GENERATOR_A2B] [--generator_B2A GENERATOR_B2A]

optional arguments:
  -h, --help            show this help message and exit
  --batchSize BATCHSIZE
                        size of the batches
  --dataroot DATAROOT   root directory of the dataset
  --input_nc INPUT_NC   number of channels of input data
  --output_nc OUTPUT_NC
                        number of channels of output data
  --size SIZE           size of the data (squared assumed)
  --cuda                use GPU computation
  --n_cpu N_CPU         number of cpu threads to use during batch generation
  --generator_A2B GENERATOR_A2B
                        A2B generator checkpoint file
  --generator_B2A GENERATOR_B2A
                        B2A generator checkpoint file
```
## Resources
### Font
* [genyo-font](https://github.com/ButTaiwan/genyo-font)
* [gensen-font](https://github.com/ButTaiwan/gensen-font)
* [genwan-font](https://github.com/ButTaiwan/genwan-font)
* [genseki-font](https://github.com/ButTaiwan/genseki-font)
* [Janson Handwriting](https://github.com/jasonhandwriting)