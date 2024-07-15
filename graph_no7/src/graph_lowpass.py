import inspect
import matplotlib.pyplot as plt
import numpy as np
import os
import warnings

from pygsp import graphs


def to_abs_path(fpath):
    dirpath = get_caller_path()
    return os.path.normpath(os.path.join(dirpath, fpath))


def get_caller_path() -> str:
    caller_frame = inspect.stack()[-1]
    caller_module = inspect.getmodule(caller_frame[0])

    caller_module_path = os.path.abspath(caller_module.__file__)
    return os.path.dirname(caller_module_path)


def mnist(datapath = './data', dtype = None):
    """import mnist dataset from PyTorch

    Parameters
    ----------
    datapath : str, optional
        Description of download folder path, by default './data'

    Returns
    -------
    traindata : ndarray
    testdata : ndarray
    trainlabel : ndarray
    testlabel : ndarray

    Examples
    --------
    >>> traindata, testdata, trainlabel, testlabel = mnist_from_torch()
    >>> assert traindata.shape == (60000, 784)
    >>> assert testdata.shape == (10000, 784)
    >>> assert trainlabel.shape == (60000,)
    >>> assert testlabel.shape == (10000,)
    """
    from torchvision.datasets import MNIST

    trainset = MNIST(to_abs_path(datapath), train=True, download=True)
    testset = MNIST(to_abs_path(datapath), train=False, download=True)
    traindata:np.ndarray = trainset.data.detach().numpy().copy().reshape(-1, 784)
    testdata: np.ndarray = testset.data.detach().numpy().copy().reshape(-1, 784)

    trainlabel:np.ndarray = trainset.targets.detach().numpy().copy()
    testlabel :np.ndarray = testset.targets.detach().numpy().copy()

    if dtype is not None:
        return (
            traindata.astype(dtype),
            testdata.astype(dtype),
            trainlabel.astype(dtype),
            testlabel.astype(dtype))

    return traindata, testdata, trainlabel, testlabel


def to_abs(x, y, /, *, bias = 0):
    with warnings.catch_warnings():
        warnings.filterwarnings("error")
        try:
            return bias + (x-y if x-y >= 0 else y-x)
        except Warning as e:
            print(f"{x=}{x.dtype} {y=}{y.dtype}")
            raise Exception(e)


def normalize(x:np.ndarray) -> np.ndarray:
    return x / 255


def adjacency_matrix(x, width = None) -> np.ndarray:
    length = len(x)
    if width is None:
        width = int(np.sqrt(length))
    height = length // width

    a = np.zeros([length, length])

    for i in range(length):
        row, column = divmod(i, width)
        if row != 0:         a[i, i-width] = a[i-width, i] = to_abs(x[i], x[i-width], bias=1)
        if row != height-1:  a[i, i+width] = a[i+width, i] = to_abs(x[i], x[i+width], bias=1)
        if column != 0:      a[i, i-1]     = a[i-1, i]     = to_abs(x[i], x[i-1], bias=1)
        if column !=width-1: a[i, i+1]     = a[i+1, i]     = to_abs(x[i], x[i+1], bias=1)
    return a


def funch(lamda):
    return 1 if lamda < 5 else 0


def main():

    traindata, *_ = mnist(dtype=np.int16)
    data = traindata[0]
    A = adjacemcy_matrix(data)

    g = graphs.Graph(A)
    g.compute_fourier_basis()
    gft_sig = g.gft(data)

    fig, ax = plt.subplots()
    ax.stem(g.e, gft_sig, linefmt="--", basefmt="k-", label="correct")
    plt.show()

    gft_sig = np.diag(
        np.array([funch(i) for i in g.e])
        )@gft_sig

    plt.imshow(g.igft(gft_sig).reshape(int(np.sqrt(data.shape[0])), -1), cmap="gray")
    plt.show()


if __name__=="__main__":
    main()
