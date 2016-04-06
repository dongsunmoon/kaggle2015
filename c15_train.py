ret = subprocess.call(os.path.join(CAFFE_ROOT, 'build/tools/caffe') + ' ' + 'train -solver=fcn_solver.prototxt -gpu 0 2> fcn_train.log', shell=True)
