import numpy as np
import pytest
import os
from torchvision import transforms

from continuum.datasets import MNIST, CIFAR10, CIFAR100, KMNIST, FashionMNIST, TinyImageNet200, AwA2, Core50
from continuum.scenarios import Rotations
from continuum.scenarios import Permutations
from continuum.scenarios import ClassIncremental
from continuum.datasets import MNISTFellowship

DATA_PATH = os.environ.get("CONTINUUM_DATA_PATH")

@pytest.mark.slow
@pytest.mark.parametrize("dataset, name, shape", [(MNIST, "MNIST", [28, 28, 1]),
                                                  (KMNIST, "KMNIST", [28, 28, 1]),
                                                  (FashionMNIST, "FashionMNIST", [28, 28, 1]),
                                                  (CIFAR10, "CIFAR10", [32, 32, 3]),
                                                  (CIFAR100, "CIFAR100", [32, 32, 3]),
                                                  (AwA2, "AwA2", [224, 224, 3]),
                                                  (Core50, "Core50", [224, 224, 3]),
                                                  (TinyImageNet200, "TinyImageNet200", [64, 64, 3])])
def test_visualization_ClassIncremental(dataset, name, shape):
    increment = 2
    init_increment = 0
    trsf = None
    if name == "CIFAR100":
        increment = 20
    elif name == "TinyImageNet200":
        increment = 40
    elif name == "AwA2":
        init_increment = 3
        trsf = [transforms.Compose([transforms.Resize((224, 224)), transforms.ToTensor()])]
    elif name == "Core50":
        trsf = [transforms.Compose([transforms.Resize((224, 224)), transforms.ToTensor()])]
    scenario = ClassIncremental(cl_dataset=dataset(data_path=DATA_PATH, download=True, train=True),
                                increment=increment, initial_increment=init_increment, transformations=trsf)

    folder = "tests/samples/class_incremental/"
    if not os.path.exists(folder):
        os.makedirs(folder)

    for task_id, taskset in enumerate(scenario):
        taskset.plot(path=folder,
                     title="{}_ClassIncremental_{}.jpg".format(name, task_id),
                     nb_samples=100,
                     shape=shape)


'''
Test the visualization with three tasks for rotations tasks
'''
@pytest.mark.slow
def test_visualization_rotations():
    scenario = Rotations(cl_dataset=MNIST(data_path=DATA_PATH, download=True, train=True),
                         nb_tasks=3,
                         list_degrees=[0, 45, 92])

    folder = "tests/samples/rotations/"
    if not os.path.exists(folder):
        os.makedirs(folder)

    for task_id, taskset in enumerate(scenario):
        taskset.plot(path=folder,
                     title="MNIST_Rotation_{}.jpg".format(task_id),
                     nb_samples=100,
                     shape=[28, 28, 1])


'''
Test the visualization with three tasks for permutations tasks
'''
@pytest.mark.slow
def test_visualization_permutations():
    scenario = Permutations(cl_dataset=MNIST(data_path=DATA_PATH, download=True, train=True),
                            nb_tasks=3,
                            seed=0)

    folder = "tests/samples/permutations/"
    if not os.path.exists(folder):
        os.makedirs(folder)

    for task_id, taskset in enumerate(scenario):
        taskset.plot(path=folder,
                     title="MNIST_Permutations_{}.jpg".format(task_id),
                     nb_samples=100,
                     shape=[28, 28, 1])


'''
Test the visualization with three tasks for incremental tasks
'''
@pytest.mark.slow
def test_visualization_MNISTFellowship():
    cl_dataset = MNISTFellowship(data_path=DATA_PATH, download=True, train=True)
    scenario = ClassIncremental(cl_dataset=cl_dataset,
                                increment=10)

    folder = "tests/samples/fellowship/"
    if not os.path.exists(folder):
        os.makedirs(folder)

    for task_id, taskset in enumerate(scenario):
        taskset.plot(path=folder,
                     title="MNISTFellowship_Incremental_{}.jpg".format(task_id),
                     nb_samples=100,
                     shape=[28, 28, 1])
