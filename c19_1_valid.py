DATA_PATH = '/home/moon/Downloads/kaggle_data/'
caffe.set_mode_gpu()
net = caffe.Net('fcn_deploy.prototxt', './model_logs/fcn_iter_15000.caffemodel', caffe.TEST)
valid_dir = os.path.join(DATA_PATH, 'validate')
studies = next(os.walk(valid_dir))[1]
if os.path.exists('output'):
    shutil.rmtree('output')

os.mkdir('output')
valid_csv = open('valid.csv', 'w')
for s in studies:
    dset = Dataset(os.path.join(valid_dir, s), s)
    print 'Processing dataset %s...' % dset.name
    try:
        dset.load()
        segment_dataset(dset)
        valid_csv.write('%s,%f,%f\n' % (dset.name, dset.edv, dset.esv))
    except Exception as e:
        print '***ERROR***: Exception %s thrown by dataset %s' % (str(e), dset.name)

valid_csv.close()
