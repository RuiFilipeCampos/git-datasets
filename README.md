



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

    def get_data_from_web() -> list[Row["image", "image_segmentation"]]:
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

Additionally, multi-stage transformations are possible:


```python

@dataset(remote="urltoyourawsbucket")
class SegmentationDataset:
    image: File[png | jpg]
    image_segmentation: File[png]

    def image_resized(image: File[png | jpg]) -> File[png]:
        ... # perform resize
        return file # instance of `File[png]``

    def image_resized_plus_brightness(image_resized: File[png]) -> File[png]:
        ... # add brightness
        return file # instance of `File[png]``

    def image_plus_resized(image: File[png | jpg], image_resized: File[png]) -> -> File[png]:
        ... # do stuff with both files
        return file # instance of `File[png]``

```


# And vertical transformations ?

For editing individual rows you can use `Action`:

```python
@dataset(remote="urltoyourawsbucket")
class SegmentationDataset:
    image: File[png | jpg]
    image_segmentation: File[png]

    def transformation_1(image: File[png | jpg]) -> Action:
        ... # perform some checks
        action = None if image_checks_out else Action.Delete
        return action
```

Note that by declaring `Action` as a return type, you inform git-datasets that a new field is not to be created (like in the previous example), instead, current values will be altered.

Transformations always occur once, on the first time they are commited.

For more control over which rows you are iterating:

```python
@dataset(remote="urltoyourawsbucket")
class SegmentationDataset:
    image: File[png | jpg]
    image_segmentation: File[png]

    @range(1, 10, 3)
    def transformation_2(image: File[png | jpg]) -> Action | None:
        ... # perform some checks
        action = None if image_checks_out else Action.Delete
        return action

    @index(10)
    def transformation_3() -> Action:
        ... # perform some checks
        return Action.Delete

    @index(11)
    def transformation_4() -> Action.Alter["image", "image_segmentation"]:
        ... # get data
        return new_image, new_segmentation
```

You can also declare `None` as the return type for no action. This is useful if you want to implement some check:

```python
@dataset(remote="urltoyourawsbucket")
class SegmentationDataset:
    image: File[png | jpg]
    image_segmentation: File[png]

    def ensure_rgb(image: File[png | jpg]) -> None:
        ... # load image
        assert image.size[2] == 3 

```

## How important are the type hints ?

Critical. When you commit a transformation you get to keep it in the code without it being run again on each new commit. This is good, it serves as documentation. But if you alter the schema in such a way that the transformation now does not make sense, the index.py file would now be lying to you. You would end up with something like:

```python
@dataset(remote="urltoyourawsbucket")
class SegmentationDataset:

    image_segmentation: File[png]

    @index(11)
    def transformation_4() -> Action.Alter["image"]:
        ... # get data
        return new_image

```

note how the type hints of `transformation_4` clearly state that the transformation is applied to a field that does not exist anymore.

By having the type hints, I know that I need to throw an error and prevent the commit from happening.

## Is git handling the files ?

No, large files are uploaded to aws. Git will version the `index.py` file and possibly an internal list of files that have been uploaded to aws.

Aws is not strict requirement too, will be extended at later stages.

## What about scale and integrity? 

At an initial phase, I'm planing data deduplication schemes and data integrity guarantees via checksums. Any structure is imposed via the sqlite database, files themselves are always cached in an hidden folder and symlinked to the places they need to be so that checking out different commits is efficient. Same goes for the aws bucket, structure is imposed by the repository, the bucket will just have a lot of files pointing to it. 

## SQLite for ML datasets ?

For now, yes. I'm going for prototype and for something that works on small to medium sized datasets. This requirement will be relaxed at later stages.

## Isn't it a lot of overhead added to git commands ?

I'm still brainstorming on this one.

`git commit` and `git push` is fine because they only act when the `index.py` file changes, which is the whole point. But when checking out branches or commits, it might become cumberson to have it move files around all the time.

The most likely solution will be to change files (except `index.py`) only on `git pull index.py`. Checking out a different branch would change the `index.py` file to the correct version, but you'd have to explicitly pull to get the data in the correct form. 





<p align="right">(<a href="#readme-top">back to top</a>)</p>




