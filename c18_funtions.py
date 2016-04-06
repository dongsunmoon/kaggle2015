MEAN_VALUE = 77
THRESH = 0.5

def calc_all_areas(images):
    (num_images, times, _, _) = images.shape
    all_masks = [{} for i in range(times)]
    all_areas = [{} for i in range(times)]
    for i in range(times):
        for j in range(num_images):
            # print 'Calculating area for time %d and slice %d...' % (i, j)
            img = images[j][i]
            in_ = np.expand_dims(img, axis=0)
            in_ -= np.array([MEAN_VALUE])
            net.blobs['data'].reshape(1, *in_.shape)
            net.blobs['data'].data[...] = in_
            net.forward()
            prob = net.blobs['prob'].data
            obj = prob[0][1]
            preds = np.where(obj > THRESH, 1, 0)
            all_masks[i][j] = preds
            all_areas[i][j] = np.count_nonzero(preds)
    return all_masks, all_areas

def calc_total_volume(areas, area_multiplier, dist):
    slices = np.array(sorted(areas.keys()))
    modified = [areas[i] * area_multiplier for i in slices]
    vol = 0
    for i in slices[:-1]:
        a, b = modified[i], modified[i+1]
        subvol = (dist/3.0) * (a + np.sqrt(a*b) + b)
        vol += subvol / 1000.0  # conversion to mL
    return vol

def segment_dataset(dataset):
    # shape: num slices, num snapshots, rows, columns
    print 'Calculating areas...'
    all_masks, all_areas = calc_all_areas(dataset.images)
    print 'Calculating volumes...'
    area_totals = [calc_total_volume(a, dataset.area_multiplier, dataset.dist)
                   for a in all_areas]
    print 'Calculating EF...'
    edv = max(area_totals)
    esv = min(area_totals)
    ef = (edv - esv) / edv
    print 'Done, EF is {:0.4f}'.format(ef)
    dataset.edv = edv
    dataset.esv = esv
    dataset.ef = ef
