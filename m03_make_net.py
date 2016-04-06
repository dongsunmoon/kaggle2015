# from caffe import layers as L
# from caffe import params as P
#
# n = caffe.NetSpec()
#
# # helper functions for common structures
# def conv_relu(bottom, ks, nout, weight_init='gaussian', weight_std=0.01, bias_value=0, mult=1, stride=1, pad=0, group=1):
#     conv = L.Convolution(bottom, kernel_size=ks, stride=stride,
#                          num_output=nout, pad=pad, group=group,
#                          weight_filler=dict(type=weight_init, mean=0.0, std=weight_std),
#                          bias_filler=dict(type='constant', value=bias_value),
#                          param=[dict(lr_mult=mult, decay_mult=mult), dict(lr_mult=2*mult, decay_mult=0*mult)])
#     return conv, L.ReLU(conv, in_place=True)
#
# def max_pool(bottom, ks, stride=1):
#     return L.Pooling(bottom, pool=P.Pooling.MAX, kernel_size=ks, stride=stride)
#
# def FCN(images_lmdb, labels_lmdb, batch_size, include_acc=False):
#     # net definition
#     n.data = L.Data(source=images_lmdb, backend=P.Data.LMDB, batch_size=batch_size, ntop=1)
#     n.label = L.Data(source=labels_lmdb, backend=P.Data.LMDB, batch_size=batch_size, ntop=1)
#     n.conv1, n.relu1 = conv_relu(n.data, ks=5, nout=40, stride=1, pad=50, bias_value=0.1)
#     n.pool1 = max_pool(n.relu1, ks=2, stride=2)
#     n.conv2, n.relu2 = conv_relu(n.pool1, ks=3, nout=40, stride=1, bias_value=0.1)
#     n.pool2 = max_pool(n.relu2, ks=2, stride=2)
#     n.flatten = L.Flatten(n.pool2)
#     n.drop = L.Dropout(n.flatten, dropout_ratio=0.1, in_place=True)
#     n.score = L.InnerProduct(n.drop, num_output=1200)
#     #n.score = L.Reshape(n.score1, reshape_param=dict(shape=[1,1200,1,1]))
#     n.loss = L.SoftmaxWithLoss(n.score, n.label, loss_param=dict(normalize=True))
#     #n.loss = L.SigmoidCrossEntropyLoss(n.score, n.label, loss_param=dict(normalize=True))
#     # from mxnet #######################
#     # net = mx.sym.Convolution(source, kernel=(5, 5), num_filter=40)
#     # net = mx.sym.BatchNorm(net, fix_gamma=True)
#     # net = mx.sym.Activation(net, act_type="relu")
#     # net = mx.sym.Pooling(net, pool_type="max", kernel=(2,2), stride=(2,2))
#     # net = mx.sym.Convolution(net, kernel=(3, 3), num_filter=40)
#     # net = mx.sym.BatchNorm(net, fix_gamma=True)
#     # net = mx.sym.Activation(net, act_type="relu")
#     # net = mx.sym.Pooling(net, pool_type="max", kernel=(2,2), stride=(2,2))
#     # flatten = mx.symbol.Flatten(net)
#     # flatten = mx.symbol.Dropout(flatten)
#     # fc1 = mx.symbol.FullyConnected(data=flatten, num_hidden=600)
#     # return mx.symbol.LogisticRegressionOutput(data=fc1, name='softmax')
#     ####################################
#     if include_acc:
#         n.accuracy = L.Accuracy(n.score, n.label)
#         return n.to_proto()
#     else:
#         return n.to_proto()
#
# def make_nets():
#     header = 'name: "FCN"\nforce_backward: true\n'
#     with open('fcn2_train.prototxt', 'w') as f:
#         f.write(header + str(FCN('train2_images_lmdb/', 'train2_labels_lmdb/', batch_size=1, include_acc=False)))
#     with open('fcn2_test.prototxt', 'w') as f:
#         f.write(header + str(FCN('test2_images_lmdb/', 'test2_labels_lmdb/', batch_size=1, include_acc=True)))
#
# if __name__ == '__main__':
#     make_nets()
