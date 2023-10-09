# Datasets (pre-alpha, design phase)

I've been playing with this idea for an easy way to create, manage and transform datasets. It started as an `.yml` based configuration thing, but after iterating it with other developers it reached an interesting form:

```python

@dataset()
class SegmentationDataset:
    image: File
    segmentation: File

    def image_512x512(image: File) -> File:
        image_array = plt.imread(image.path)
        image_array = cv2.resize(image_array, size=(512, 512))
        with File.make_tmp() as tmp_file:
            plt.imsave(tmp_file.path)
            return tmp_file
   
    def segmentation_512x512(segmentation: File) -> File:
        segmentation_array = plt.imread(segmentation.path)
        segmentation_array = cv2.resize(segmentation_array, size=(512, 512))
        with File.make_tmp() as tmp_file:
            plt.imsave(tmp_file.path)
            return tmp_file

@batch(SegmentationDataset)
class SegmentationBatch:

    def image_512x512_batch(image_512x512: list[File]) -> tf.Tensor:
        arrays = [plt.imread(path) for path in image_512x512]
        arrays = np.array(arrays)
        return tf.Tensor(arrays)

    def segmentation_512x512_batch(segmentation_512x512: list[File]) -> tf.Tensor:
        arrays = [plt.imread(path) for path in segmentation_512x512]
        arrays = np.array(arrays)
        return tf.Tensor(arrays)

    def image_512x512_batch_augmented(image_512x512_batch: tf.Tensor) -> tf.Tensor:
        shape_of_batch = image_512x512_batch.shape()
        noise = make_noise(shape_of_batch)
        return image_512x512_batch + noise
    
    def augmented_toguether(image_512x512_batch, image_512x512_batch_augmented) -> tuple[tf.Tensor, tf.Tensor]:
        transformation = tf.RandomAffine()
        mapping = map(transformation, [image_512x512_batch, image_512x512_batch_augmented])
        return tuple(mapping)

iterator = SegmentationBatch.image_512x512_batch_augmented.range(0, 100, 10)
for batch in iterator.randomize():
    ...

```


## How it will work

Going in parts:

```python
@dataset(sql_file="./dataset.sql", data_dir="./dataset")
class SegmentationDataset:
    image: File
    segmentation: File
```

If not there already, this code will create a file named `dataset.sql` and a folder named `dataset` with subdirectories `dataset/image` and `dataset/segmentation`. 







