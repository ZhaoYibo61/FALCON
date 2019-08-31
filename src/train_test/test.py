"""
FALCON: FAst and Lightweight CONvolution

Authors:
 - Chun Quan (quanchun@snu.ac.kr)
 - U Kang (ukang@snu.ac.kr)
 - Data Mining Lab. at Seoul National University.

File: train_test/test.py
 - test the pre-trained model on test datasets.
 - print the test accuracy and inference time.

Version: 1.0

This software may be used only for research evaluation purposes.
For other purposes (e.g., commercial), please contact the authors.

"""
import torch
import torch.nn.functional as F

import time

from utils.load_data import load_cifar10, load_cifar100, load_svhn, load_mnist, load_tiny_imagenet


def test(net, log=None, batch_size=128, data='cifar100'):
    """
    Test on trained model.
    :param net: model to be tested
    :param log: log dir
    :param batch_size: batch size
    :param data: datasets used
    """

    net.eval()
    is_train = False

    # data
    if data == 'cifar10':
        test_loader = load_cifar10(is_train, batch_size)
    elif data == 'cifar100':
        test_loader = load_cifar100(is_train, batch_size)
    elif data == 'svhn':
        test_loader = load_svhn(is_train, batch_size)
    elif data == 'mnist':
        test_loader = load_mnist(is_train, batch_size)
    elif data == 'tinyimagenet':
        test_loader = load_tiny_imagenet(is_train, batch_size)
    else:
        exit()

    correct = 0
    total = 0
    inference_start = time.time()
    with torch.no_grad():
        for i, data in enumerate(test_loader, 0):
            inputs, labels = data
            outputs, outputs_conv = net(inputs.cuda())
            _, predicted = torch.max(F.softmax(outputs, -1), 1)
            total += labels.size(0)
            correct += (predicted == labels.cuda()).sum()
    inference_time = time.time() - inference_start
    print('Accuracy: %f %%; Inference time: %fs' % (float(100) * float(correct) / float(total), inference_time))
    # print('.', end='')

    if log != None:
        log.write('Accuracy of the network on the 10000 test images: %f %%\n' % (float(100) * float(correct) / float(total)))
        log.write('Inference time is: %fs\n' % inference_time)

    return inference_time