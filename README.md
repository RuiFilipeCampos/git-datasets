# Datasets (design and prototype phase)


# The idea

1. Create an `index.py` file and write:
```python

@dataset(remote="awsbucket")
class SegmentationDataset:
    image: File[png | jpg]
    segmentation: File[png]
```

2. Track the dataset

```bash
git datasets track index.py
```

3. Commit the file

```
git commit index.py
```

This results in the creation of an sqlite database with the given schema and since it has two file fields, two new folders:

```
| image/
| segmentation/
| dataset.sqlite
| index.py
```

4. Write an ingest method to get data into the dataset

```python
@dataset(remote="awsbucket")
class SegmentationDataset:
    image: File[png | jpg]
    segmentation: File[png]
    
    @ingest
    def get_dataset_from_web():
        ... # perform some web requests, save the files
        return list_of_image, list_of_segmentation

```

5. Commit the changes

```
git commit index.py
```

This will execute the `get_dataset_from_web` method and backup the files in a cache, they are also symlinked to the `image/` and `segmentation/` folders (which are fields in the schema) 

6. To perform transformations on the dataset:


```python
@dataset(remote="awsbucket")
class SegmentationDataset:
    image: File[png | jpg]
    segmentation: File[png]
    
    def segmentation_resized(segmentation: File[png]) -> File[png]:
        ...
        return file

```

and then

```
git commit index.py
```

will alter the schema and perform the transformation, resulting in 

```
| image/
| segmentation/
| segmentation_resized/
| dataset.sqlite
| index.py
```

7. You can also remove fields



```python
@dataset(remote="awsbucket")
class SegmentationDataset:
    segmentation: File[png]
    
    def segmentation_resized(segmentation: File[png]) -> File[png]:
        ...
        return file

```

and,

```
git commit index.py
```

results in 

```
| segmentation/
| segmentation_resized/
| dataset.sqlite
| index.py
```


8. But of course, you can go back

```
git reset --hard HEAD~1
```

resulting in 

```
| image/
| segmentation/
| segmentation_resized/
| dataset.sqlite
| index.py
```

9. Save the changes as you normally do, by pushing the commits

```
git push
```

The message here is: the only thing you truly need to care about is the `index.py` file, comited `index.py` file is guaranteed to describe the current state of `database.sqlite` and the data folders. 



