with io.capture_output() as captured:
    # edit this so it matches where you download the DSB data
    DATA_PATH = '/home/moon/Downloads/kaggle_data/'
    caffe.set_mode_gpu()
    net = caffe.Net('fcn_deploy.prototxt', './model_logs/fcn_iter_15000.caffemodel', caffe.TEST)
    train_dir = os.path.join(DATA_PATH, 'train')
    studies = next(os.walk(train_dir))[1]
    labels = np.loadtxt(os.path.join(DATA_PATH, 'train.csv'), delimiter=',', skiprows=1)
    label_map = {}
    for l in labels:
        label_map[l[0]] = (l[2], l[1])
    if os.path.exists('output'):
        shutil.rmtree('output')
    os.mkdir('output')
    accuracy_csv = open('accuracy.csv', 'w')
    for s in studies:
        dset = Dataset(os.path.join(train_dir, s), s)
        print 'Processing dataset %s...' % dset.name
        try:
            dset.load()
            segment_dataset(dset)
            (edv, esv) = label_map[int(dset.name)]
            accuracy_csv.write('%s,%f,%f,%f,%f\n' % (dset.name, edv, esv, dset.edv, dset.esv))
        except Exception as e:
            print '***ERROR***: Exception %s thrown by dataset %s' % (str(e), dset.name)
    accuracy_csv.close()

with open('logs.txt', 'w') as f:
    f.write(captured.stdout)
