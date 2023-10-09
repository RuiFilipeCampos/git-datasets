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

So, essentially, this class defines a schema, how your dataset looks like. Right now, each row has two features, an image and its segmentation, saved as filee.

But, it is often the case that we need all the images to be of the same size.

Instead of writing a for loop, altering the sqlite database, performing all sorts of cleanup, taking care of data integrity concerns, etc etc etc

You kind of just, declare it:

```python
@dataset(sql_file="./dataset.sql", data_dir="./dataset")
class SegmentationDataset:
    image: File
    segmentation: File

    def image_512x512(image: File) -> File:
        image_array = plt.imread(image.path)
        image_array = cv2.resize(image_array, size=(512, 512))
        with File.make_tmp() as tmp_file:
            plt.imsave(tmp_file.path)
            return tmp_file
```

What this says is, let there be a new field, named `image_512x512`, that is the result of applying these transformations to the `image`.

The dependency of `image_512x512` on `image` is described by function definition: `def image_512x512(image: File) -> File`, which also defines the resulting type.

In this case, we'd wish for the model to output labels(segmentation) with the same size of the image, so we define the same transformation to the `segmentation` field:

```
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
```





