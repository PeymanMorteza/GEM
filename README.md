
# GEM : GMM based Energy Measurement

This repository contains the code for **Provable guarantees for undrestanding out-of-distribution Detection** by *Peyman Morteza* and *Sharon Yixuan Li*. Substantial part of this codebase is based on [Energy-OOD](https://github.com/wetliu/energy_ood) and [Outlier-Exposure](https://github.com/hendrycks/outlier-exposure). 

![Alt text](img/main_teaser.png "OOD detection")

## Required datasets
* [CIFAR-10](https://www.cs.toronto.edu/~kriz/learning-features-2009-TR.pdf) and [CIFAR-100](https://www.cs.toronto.edu/~kriz/learning-features-2009-TR.pdf) are used as ID data.
* [Textures](https://ieeexplore.ieee.org/document/6909856), [SVHN](https://research.google/pubs/pub37648/), [Places365](https://ieeexplore.ieee.org/document/7968387), [LSUN-Crop](https://dblp.org/rec/journals/corr/YuZSSX15.html), [LSUN-Resize](https://dblp.org/rec/journals/corr/YuZSSX15.html),and [iSUN](https://arxiv.org/abs/1504.06755) are used as OOD data.

## GEM-score computation 
* Download the required data sets into ``./data/``.
* Run the following to see performance of GEM method on OOD data using a [WideResNet](https://github.com/szagoruyko/wide-residual-networks) architecture pretrained on CIFAR-10:
```
bash run.sh GEM 0
```
* Run the following to see performance of GEM method on OOD data using a [WideResNet](https://github.com/szagoruyko/wide-residual-networks) architecture pretrained on CIFAR-100:
```
bash run.sh GEM 1
```

## Experimental Result on CIFAR-10

| Model name         |     FPR95       |  AUROC  |  AUPR  |
| ------------------ |---------------- | --------| ------ |  
| [Softmax score](https://arxiv.org/abs/1610.02136) |     51.04      |  90.90 |  97.92  |  
| [ODIN](https://arxiv.org/abs/1706.02690)          |     35.71      |  91.09 |  97.62  |
| [Mahalanobis](https://arxiv.org/abs/1807.03888)   |     36.96      |  93.24 |  98.47  |
| [Energy score](https://arxiv.org/abs/2010.03759)  |     33.01      |  91.88 |  97.83  |
| GEM (ours)    |     37.21      |  93.23 |  98.47  |


## Experimental Result on CIFAR-100

| Model name         |     FPR95       |  AUROC  |  AUPR  |
| ------------------ |---------------- | --------| ------ |  
| [Softmax score](https://arxiv.org/abs/1610.02136) |     80.41      |  75.53 |  93.93  |  
| [ODIN](https://arxiv.org/abs/1706.02690)          |     74.64      |  77.43 |  94.23  |
| [Mahalanobis](https://arxiv.org/abs/1807.03888)   |     57.01      |  82.70 |  95.68  |
| [Energy score](https://arxiv.org/abs/2010.03759)  |     73.60      |  79.56 |  94.87  |
| GEM (ours)    |     57.03      |  82.67 |  95.66  |

## Citation

    @article{??,
            title={GEM},
            author={Morteza, Peyman and Li, Yixuan},
            journal={??},
            year={2021}
            } 
