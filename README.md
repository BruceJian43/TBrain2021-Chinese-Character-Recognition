# 玉山人工智慧挑戰賽2021夏季賽

## Requirements

Python3

Pip:

```bash
pip install numpy pillow sklearn timm torch torchvision tqdm git+https://github.com/ildoonet/pytorch-randaugment
```

For Pytorch running on cpu platforms: check out [Start Locally | PyTorch](https://pytorch.org/get-started/locally/).

For api ([`api.py`](src/api.py)), additional packages are required:

OpenCV-Python: check out [OpenCV: Introduction to OpenCV](https://docs.opencv.org/4.5.2/da/df6/tutorial_py_table_of_contents_setup.html) or [opencv-contrib-python](https://pypi.org/project/opencv-python/).

Pip:

```bash
pip install flask gunicorn
```

For load balancer ([`balance.py`](src/balance.py)), also install the following:

Pip:

```bash
pip install requests
```

## Training

```
usage: train.py [-h] [--batch-size BATCH_SIZE] [--num-workers NUM_WORKERS] [--drop-last] [--seed SEED]
                [--device DEVICE] --train-dataset TRAIN_DATASET [TRAIN_DATASET ...]
                [--train-transform-name NAME [NAME ...]]
                [--validation-dataset VALIDATION_DATASET [VALIDATION_DATASET ...]]
                --validation-transform-name NAME --model-name NAME
                [--aux-logits-weight AUX_LOGITS_WEIGHT] [--label-smoothing LABEL_SMOOTHING] [--lr LR]
                [--num-epochs NUM_EPOCHS] [--log-directory DIRECTORY]

optional arguments:
  -h, --help            show this help message and exit
  --batch-size BATCH_SIZE
                        how many samples per batch to load (default: 64)
  --num-workers NUM_WORKERS
                        how many subprocesses to use for data loading (default: 8)
  --drop-last           drop the last incomplete train batch (default: False)
  --seed SEED           (default: 7122)
  --device DEVICE
  --train-dataset TRAIN_DATASET [TRAIN_DATASET ...]
  --train-transform-name NAME [NAME ...]
  --validation-dataset VALIDATION_DATASET [VALIDATION_DATASET ...]
  --validation-transform-name NAME
  --model-name NAME
  --aux-logits-weight AUX_LOGITS_WEIGHT
                        aux logits weight for inception_v3 (default: 0.4)
  --label-smoothing LABEL_SMOOTHING
                        label smoothing factor (default: 0.1)
  --lr LR               learning rate (default: 0.0001)
  --num-epochs NUM_EPOCHS
                        (default: 64)
  --log-directory DIRECTORY
                        directory to save models and logs (default: None)
```

For repvgg_b3g4 (prelim):

```bash
python3 train.py --train-dataset /path/to/train_dataset --train-transform-name crazy_train_transform --validation-dataset /path/to/validation_dataset --validation-transform val_squarepad128_transform --model-name repvgg_b3g4 --log-directory repvgg_b3g4_prelim
```

For inception_v3 (primary):

```bash
python3 train.py --train-dataset /path/to/train_dataset --train-transform-name inception_v3_train_transform --validation-dataset /path/to/validation_dataset --validation-transform inception_v3_val_transform --model-name inception_v3 --log-directory inception_v3_primary
```

For dm_nfnet_f0 (primary):

```bash
python3 train.py --train-dataset /path/to/train_dataset --train-transform-name train_squarepad128_transform --validation-dataset /path/to/validation_dataset --validation-transform val_squarepad128_transform --model-name dm_nfnet_f0 --log-directory dm_nfnet_f0_primary
```

For repvgg_b3g4 (primary):

```bash
python3 train.py --train-dataset /path/to/train_dataset --train-transform-name train_squarepad128_transform --validation-dataset /path/to/validation_dataset --validation-transform val_squarepad128_transform --model-name repvgg_b3g4 --log-directory repvgg_b3g4_primary
```

For resnetv2_101x1_bitm (primary):

```bash
python3 train.py --train-dataset /path/to/train_dataset --train-transform-name train_squarepad128_transform --validation-dataset /path/to/validation_dataset --validation-transform val_squarepad128_transform --model-name resnetv2_101x1_bitm --log-directory resnetv2_101x1_bitm_primary
```

If not specified, the device will be cuda if it is available.

`--train-dataset` and `--validation-dataset` specify the paths to datasets following the structure of [torchvision.datasets.ImageFolder](https://pytorch.org/vision/stable/datasets.html#torchvision.datasets.ImageFolder).

`--train-transform-name` and `--validation-transform-name` are transforms in [`transforms.py`](src/transform.py).

`--model-name` specifies a model name accepted by [models.get_model](src/models.py).

To save model checkpoints, remember to specify `--log-directory /path/to/log_directory`.

Log directory structure:

```
/path/to/log_directory
├── info.json
├── log.txt
└── models
    ├── best_accuracy.ckpt
    ├── best_macro_average_f1.ckpt
    └── last.ckpt
```

## Api

individual node:

```
usage: api.py [-h] --primary PRIMARY [PRIMARY ...] [--primary-threshold PRIMARY_THRESHOLD]
              [--prelim PRELIM [PRELIM ...]] [--prelim-threshold PRELIM_THRESHOLD]
              [--max-workers MAX_WORKERS] [--training-data-dic TRAINING_DATA_DIC] [--data DATA]
              [--captain-email CAPTAIN_EMAIL] [--salt SALT]

optional arguments:
  -h, --help            show this help message and exit
  --primary PRIMARY [PRIMARY ...]
                        primary checkpoints to ensemble (default: None)
  --primary-threshold PRIMARY_THRESHOLD
                        (default: 0.28)
  --prelim PRELIM [PRELIM ...]
                        prelim checkpoints to ensemble (default: None)
  --prelim-threshold PRELIM_THRESHOLD
                        (default: 0.7)
  --max-workers MAX_WORKERS
                        The maximum number of processes that can be used to execute the predict
                        function calls (default: 1)
  --training-data-dic TRAINING_DATA_DIC
  --data DATA           directory to save requests and responses (default: data)
  --captain-email CAPTAIN_EMAIL
  --salt SALT
```

If `--training-data-dic /path/to/training data dic.txt` is specified, predictions not in `training data dic.txt` will be converted to "isnull".

Additional arguments will be passed as gunicorn settings (bind, threads, timeout, etc.).

If not specified, captain email, salt, and other gunicorn settings will be loaded from [`config.py`](src/config.py).

Example:

```bash
python3 --primary inception_v3_primary/models/best_macro_average_f1.ckpt dm_nfnet_f0_primary/models/best_macro_average_f1.ckpt repvgg_b3g4_primary/models/best_macro_average_f1.ckpt resnetv2_101x1_bitm_primary/models/best_macro_average_f1.ckpt --prelim repvgg_b3g4_prelim/models/best_macro_average_f1.ckpt --training-data-dic 'training data dic.txt' --bind '0.0.0.0:24865'
```

load balancer:

```
usage: balance.py [-h] [--netloc NETLOC [NETLOC ...]] [--max-workers MAX_WORKERS]

optional arguments:
  -h, --help            show this help message and exit
  --netloc NETLOC [NETLOC ...]
                        netloc of api server node (default: None)
  --max-workers MAX_WORKERS
```

If `--max-workers` is not specified, it will be 4 * number_of_netlocs.

Additional arguments will be passed as gunicorn settings (bind, threads, timeout, etc.).

If not specified, netlocs and other gunicorn settings will be loaded from [`config.py`](src/config.py).

Example:

```bash
python3 balance.py --netloc ADDRESS1 ADDRESS2 --bind '0.0.0.0:44966' --threads 120
```

## Generate Fake Handwriting Images as Additional Data

See [Generate Fake Handwriting Images Using CycleGAN](cycleGAN).
