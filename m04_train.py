ret = subprocess.call(os.path.join(CAFFE_ROOT, 'build/tools/caffe') + ' ' + 'train -solver=fcn2_solver.prototxt -gpu 0 2> fcn2_train.log', shell=True)
