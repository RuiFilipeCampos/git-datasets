



<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/RuiFilipeCampos/git-datasets">
    <img src="https://github.com/RuiFilipeCampos/git-datasets/assets/63464503/e0885e59-865e-48f2-bdb5-3113102522fc" alt="Logo" width="260" height="260">
  </a>



  <p align="center">
    Declaratively create, transform, and manage ML datasets.
    <br />

  </p>
</div>

<!-- ABOUT THE PROJECT -->
## What are you trying to do? 

**The basic premise of git-datasets is to attempt to introduce a data as code paradigm.** Imagine being able to commit, revert, restore, pull, push, open a PR and review data just as you do with code. All right from git and with minimal setup.

## How are you planning to do that ?

The idea is that for each dataset you have an `index.py`. The rule is that a commited `index.py` file will always tell the truth. The consequence of this is that all data transformations must occur only when you do a `git commit` on `index.py`. As a concrete example, imagine you want to build an `(image, image_segmentation)` dataset. You'd start by writing the following `index.py` file:

```python

@dataset(remote="urltoyourawsbucket")
class SegmentationDataset:
    image: File[png | jpg]
    image_segmentation: File[png]

```

You'd first mark this as a dataset via `git datasets track index.py`, and then commit it via `git commit`. Commiting this file results in the creation of an sqlite file that tracks file and in the creation of the `image/` and `image_segmentation/` folders. Everytime you change the above schema and commit the file, the changes are enacted. 


## How would you add data ?

Adding data happens by writing a method without arguments:


```python
@dataset(remote="urltoyourawsbucket")
class SegmentationDataset:
    image: File[png | jpg]
    image_segmentation: File[png]

    def get_data_from_web() -> list[Row]:
        ... # perform some requests, massage data, return it to save it
        return [
            (file_1, file_2),
            (file_3, file_4),
            ...
        ]
```

this method is called once on the first time it is commited.


## How would you transform data ?

All data transformations will happen on commit, leaving a traceable history of everything that happened to the dataset. For example, I might want to resize the orignal image and have it as a new feature for the dataset:


```python

@dataset(remote="urltoyourawsbucket")
class SegmentationDataset:
    image: File[png | jpg]
    image_segmentation: File[png]

    def image_resized(image: File[png | jpg]) -> File[png]:
        ... # perform resize
        return file # instance of `File[png]``

```

Commiting this results in the creation of a new field, `image_resized` with type `File[png]`, and in the application of the transformation to populate that field.

# And vertical transformations ?

```python

@dataset(remote="urltoyourawsbucket")
class SegmentationDataset:
    image: File[png | jpg]
    image_segmentation: File[png]

    # range iterates every row, the return type instructs    
    @range()
    def transformation_1(image: File[png | jpg]) -> Action:
        ... # perform some checks
        action = None if image_checks_out else Action.Delete
        return action

    @range(1, 10, 3)
    def transformation_2(image: File[png | jpg]) -> Action:
        ... # perform some checks
        action = None if image_checks_out else Action.Delete
        return action

    @index(10)
    def transformation_3() -> Action:
        ... # perform some checks
        return Action.Delete

    @index(11)
    def transformation_4() -> Row["image", "image_segmentation"]:
        ... # get data
        return new_image, new_segmentation

```


## What about scale and integrity? 

At an initial phase, I'm planing data deduplication schemes and data integrity guarantees via checksums. Any structure is imposed via the sqlite database, files themselves are always cached in an hidden folder and symlinked to the places they need to be so that checking out different commits is efficient. Same goes for the aws bucket, structure is imposed by the repository, the bucket will just have a lot of files pointing to it. 

## SQLite for ML datasets ?

For now, yes. I'm going for prototype and for something that works on small to medium sized datasets.






<p align="right">(<a href="#readme-top">back to top</a>)</p>




