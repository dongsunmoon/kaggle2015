DATA_PATH = '/home/moon/kaggle/data/'
train_dir = os.path.join(DATA_PATH, 'train')

studies = next(os.walk(train_dir))[1]
labels = np.loadtxt(os.path.join(DATA_PATH, 'train.csv'), delimiter=',', skiprows=1)
label_map = {}
for l in labels:
    # Id,Systole,Diastole
    label_map[int(l[0])] = (l[1], l[2])

counter_img = 0
counter_train = 0
counter_test = 0
dset = None
for s in studies:
    # if s != '442':
    #     continue
    # 2016.1.1
    # skip error inputs
    if s in ['123','463','234','279','499','416','334']:
        continue
    try:
        dset = Dataset(os.path.join(train_dir, s), s)
        print 'Processing dataset %s...(%f,%f)' % (dset.name,label_map[int(s)][0],label_map[int(s)][1])
        # DMoon Note
        # A dataset has many slides
        # And each slides has 30 images (id:time)
        # dataset[j][i] : jth slide, ith time image
        dset.load()
        counter_img_of_s = 0
        counter_label = counter_img
        if int(s) < 401:
            db_imgs = lmdb.open('train2_images_lmdb', map_size=1e12)
        else:
            db_imgs = lmdb.open('test2_images_lmdb', map_size=1e12)
        with db_imgs.begin(write=True) as txn_img:
            for images_on_a_slide in dset.images:
                # datum = caffe.io.array_to_datum(images_on_a_slide)
                datum = caffe.io.array_to_datum(diff_images(images_on_a_slide))
                txn_img.put("{:0>10d}".format(counter_img), datum.SerializeToString())
                counter_img += 1
                counter_img_of_s += 1
                print("Processed {:d} images".format(counter_img))
                if int(s) < 401:
                    counter_train += 1
                else:
                    counter_test += 1
    except Exception as e:
        print '------------------------------------------'
        print 'Error reading: %s' % s
        print e
        print '------------------------------------------'
        continue
    if int(s) < 401:
        db_labels = lmdb.open('train2_labels_lmdb', map_size=1e12)
    else:
        db_labels = lmdb.open('test2_labels_lmdb', map_size=1e12)
    with db_labels.begin(write=True) as txn_label:
        for i in range(counter_img_of_s):
            systole_label = map(int, label_map[int(s)][0] < np.arange(600))
            diastole_label = map(int, label_map[int(s)][1] < np.arange(600))
            label_pair = np.array(systole_label+diastole_label)
            label_pair = np.expand_dims(label_pair, axis=1)
            label_pair = np.expand_dims(label_pair, axis=1)
            datum = caffe.io.array_to_datum(label_pair)
            txn_label.put("{:0>10d}".format(counter_label), datum.SerializeToString())
            counter_label += 1
        print("Processed {:d} labels".format(counter_label))
    db_imgs.close()
    db_labels.close()

print 'counter_train: %s' % counter_train
print 'counter_test: %s' % counter_test
