class Dataset(object):
    dataset_count = 0
    def __init__(self, directory, subdir):
        # deal with any intervening directories
        while True:
            subdirs = next(os.walk(directory))[1]
            if len(subdirs) == 1:
                directory = os.path.join(directory, subdirs[0])
            else:
                break
        slices = []
        for s in subdirs:
            m = re.match('sax_(\d+)', s)
            if m is not None:
                slices.append(int(m.group(1)))
        slices_map = {}
        first = True
        times = []
        for s in slices:
            print '[s] %s' % s
            files = next(os.walk(os.path.join(directory, 'sax_%d' % s)))[2]
            offset = None
            for f in files:
                m = re.match('IM-(\d{4,})-(\d{4})\.dcm', f)
                # print '%s :%s' % (f, m.group(1))
                # print '%s : %d' % (f, offset)
                if m is not None:
                    if first:
                        times.append(int(m.group(2)))
                    if offset is None:
                        offset = int(m.group(1))
                else:
                    print '%s is None' % f
            first = False
            slices_map[s] = offset
        self.directory = directory
        self.time = sorted(times)
        self.slices = sorted(slices)
        self.slices_map = slices_map
        Dataset.dataset_count += 1
        self.name = subdir
    def _filename(self, s, t):
        if self.slices_map[s] < 10000:
            return os.path.join(self.directory,
                                'sax_%d' % s,
                                'IM-%04d-%04d.dcm' % (self.slices_map[s], t))
        else:
            return os.path.join(self.directory,
                                'sax_%d' % s,
                                'IM-%05d-%04d.dcm' % (self.slices_map[s], t))
    def _crop_resize(self, img, size):
        if img.shape[0] < img.shape[1]:
            img = img.T
        # we crop image from center
        short_egde = min(img.shape[:2])
        yy = int((img.shape[0] - short_egde) / 2)
        xx = int((img.shape[1] - short_egde) / 2)
        crop_img = img[yy : yy + short_egde, xx : xx + short_egde]
        # resize to 64, 64
        resized_img = transform.resize(crop_img.astype('float'), (size, size))
        return resized_img
    def _read_dicom_image(self, filename):
        #print '_read_dicom_image(%s)' % filename
        d = dicom.read_file(filename)
        img = d.pixel_array.astype('int64')
        # print np.shape(img)
        # print type(img)
        # print type(img[0][0])
        return self._crop_resize(img, 128)
    def _read_all_dicom_images(self):
        f1 = self._filename(self.slices[0], self.time[0])
        d1 = dicom.read_file(f1)
        (x, y) = d1.PixelSpacing
        (x, y) = (float(x), float(y))
        f2 = self._filename(self.slices[1], self.time[0])
        d2 = dicom.read_file(f2)
        # try a couple of things to measure distance between slices
        try:
            dist = np.abs(d2.SliceLocation - d1.SliceLocation)
        except AttributeError:
            try:
                dist = d1.SliceThickness
            except AttributeError:
                dist = 8  # better than nothing...
        print self.time
        print self.slices
        self.images = np.array([[self._read_dicom_image(self._filename(d, i))
                                 for i in self.time]
                                for d in self.slices])
        print np.shape(self.images)
        self.dist = dist
        self.area_multiplier = x * y
    def load(self):
        self._read_all_dicom_images()
