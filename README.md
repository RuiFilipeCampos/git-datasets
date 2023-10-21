



<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>



<!-- PROJECT LOGO -->
<br/>
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

**At its core, git-datasets is an attempt at introducing a "data as code" paradigm.** Imagine being able to commit, revert, restore, pull, push, merge, resolve conflicts, open a PR and review data just as you do with code. All right from git and with minimal setup.

## How are you planning to do that ?

Every dataset has an `index.py` file. The promise? A committed `index.py` always tells the truth. The consequence is that every transformation occurs on `git commit index.py`. 

Let's say you want a dataset with images and object segmentations. Your `index.py` could look like this:

```python
@dataset
class ImageClassificationDataset:
    image: File[jpg]
    label: Literal["cat", "dog", "person"]
```

First, you set this up as a dataset using `git datasets new index.py`. When you save it with `git commit index.py` a parquet file is created with that schema. This file is hidden out of view in the `.git` folder and when you run `git push` it is uploaded to a chosen cloud provider ([apache-libcloud](https://libcloud.apache.org) will be used to support all providers)

## How would you add data ?

Declare a method with return type of `Action.Insert`:

```python
@dataset
class SegmentationDataset:
    image: File[jpg]
    label: Literal["cat", "dog", "person"]

    def get_data_from_web() -> Action.Insert[{
        "image": File[jpg],
        "label": Literal["cat", "dog", "person"],
    }]

        ... # perform some requests, massage data into the correct form

        return [
            (image_1, label_1),
            (image_2, label_2),
            (image_3, label_3),
            ...
        ]
```

this method is called once on the first time it is commited.


## How would you transform data ?

All data transformations will happen on commit, leaving a traceable history of everything that happened to the dataset. 

For example, I might want to resize the orignal images and encode the label:

```python
@dataset
class SegmentationDataset:
    image: File[jpg]
    label: Literal["cat", "dog", "person"]

    def image_resized_512x512(image: File[jpg]) -> File[png]:

        ... # perform resize

        # return an instance of `File[png]`
        return file

    def encoded_label(label: Literal["cat", "dog", "person"]) -> Literal[0, 1, 2]:
        if label == "cat":
            return 0
        elif label == "dog":
            return 1
        elif label == "person":
            return 2
        else:
            raise ValueError("Not a cat, dog or person !!")

```

Commiting this results in the creation of a new field, `image_resized_512x512` with type `File[png]`, and in the application of the transformation to populate that field. This transform is only applied again if one value happens to be missing.

Additionally, multi-stage transformations are possible:


```python

@dataset
class SegmentationDataset:
    image: File[jpg]
    label: Literal["cat", "dog", "person"]

    def image_resized_512x512(image: File[jpg]) -> File[png]:

        ... # perform resize

        return file

    def encoded_label(label: Literal["cat", "dog", "person"]) -> Literal[0, 1, 2]:
        if label == "cat":
            return 0
        elif label == "dog":
            return 1
        elif label == "person":
            return 2
        else:
            raise ValueError("Not a cat, dog or person !!")

    def example_field(
        image_resized_512x512: File[png],
        encoded_label: Literal[0, 1, 2],
    ) -> File[png]:

        ... # do stuff

        return file

```

## Transformations on every commit, sounds like it could get annoying.


A lot of transformations will be blocking if you have a large dataset. These are the attenuating factors:

1. Commiting will only lock changes to the `index.py` file, letting you work while you wait for the processing to take place. (live inspection during transformations will be possible via `python index.py --sql-shell` or `python index.py --python-shell` or `python index.py --jupyter-notebook`, etc)
2. It will be possible to mark certain transformations to be skiped (with `@skip`)
3. It will also be possible to mark transformations to be consumed by a github workflow (with `@cicd`)
4. For truly large datasets, an integration with spark will be available. (possibly with `@spark`, but probably a deeper integration, still researching)



```python 

@dataset
class SegmentationDataset:
    image: File[jpg]
    label: Literal["cat", "dog", "person"]

    @skip
    def field_to_skip(image: File[jpg]) -> File[png]:

        ... # perform resize

        return file

    @cicd
    def field_for_cicd(image: File[jpg]) -> File[png]:

        ... # perform resize

        return file

    @spark
    def field_for_spark(image: File[jpg]) -> File[png]:

        ... # perform resize

        return file

```

Furthermore, commits only cause a transformation when there is a "delta" in the file that requires it.

Adding a new transformation will cause a transformation. Adding a docstring will not cause any transformation to occur. 

Processing only occurs when:

- a new transformation is added
- new data is added
- results from a current transformation are missing

And finally, of course, paralelization will be used when possible.

## Still, is the transformation on commit thing really necessary ? 

There are two parts to this:

1. The code that is used to execute the transformation
2. The result of a *successful* transformation

By tying these two toguether with a commit, **we have now turned the commit into an imutable snapshot of the dataset**.

Each commit is tied to the resulting (versioned) parquet file which itself points to any resulting files. 



## What about row transformations ?

For editing individual rows you can use `Action` again:

```python
@dataset
class SegmentationDataset:
    image: File[jpg]
    segmentation: File[png]
    label: str

    def delete_corrupted_files(image: File[jpg]) -> Action.Delete:

        ... # perform some checks, get image_is_corrupted: bool

        return image_is_corrupted
```

Transformations always occur once, on the first time they are commited.

For more control over which rows you are iterating:

```python
@dataset
class SegmentationDataset:
    image: File[jpg]
    segmentation: File[png]
    label: str

    @range(1, 10, 3)
    def transformation_2(image: File[jpg]) -> Action.Delete:

        ... # perform some checks

        return False if image_checks_out else True

    @index(10)
    def transformation_3() -> Action.Delete:

        ... # perform some checks

        return True

    @index(11)
    def transformation_4(image: File[jpg], segmentation: File[png]) -> Action.Alter:

        ... # get data

        return new_image, new_segmentation
```

You can also declare `None` as the return type for no action. This is useful if you want to implement some check:

```python
@dataset
class SegmentationDataset:
    image: File[jpg]
    image_segmentation: File[png]

    def ensure_rgb(image: File[jpg]) -> None:

        ... # load image

        assert image.size[2] == 3

```


## Where are files going ?

Files go into the `.git` folder, but they are uploaded to your chosen cloud provider.

For example, you'd link your repository to a bucket via

```
git datasets link --provider "AWS" --bucket $AWS_BUCKET`
```

you'd do this once, but credentions would be provided on a per user basis.


## But my dataset is large, I can't fit it into my computer.

You setup a memory limit. Once that limit is reached, only a snapshot of the dataset is kept. Files are cycled on demand as needed.


## How important are the type hints ?

Critical. When you commit a transformation you get to keep it in the code without it being run again on each new commit. This is good, it serves as documentation. But if you alter the schema in such a way that the transformation now does not make sense, the index.py file would now be lying to you. You would end up with something like:

```python
@dataset
class SegmentationDataset:

    image_segmentation: File[png]

    @index(11)
    def transformation_4(image: File[png]) -> Action.Alter:

        ... # get data

        return new_image

```

note how the type hints of `transformation_4` clearly state that the transformation is applied to a field that does not exist anymore.

By having the type hints, I know that I need to throw an error and prevent the commit from happening.

## Is git handling the files ?

No, large files are uploaded to your chosen cloud provider. Git will version the `index.py` file. 


## What about scale and integrity? 

I'm planing data deduplication schemes and data integrity guarantees via checksums. 




## What happens when there is a merge conflict ?

Merge conflicts are resolved directly in the `index.py` file. The state of the dataset can always be derived from its previous commit and its current commit. So after resolving a conflict, that's what determines what happens to the data.

## What happens if someone commits without `git-datasets` ?

This will happen. A merge conflict might get resolved on github's interface. Someone might commit without having git datasets installed. Etc.

If the commits make sense, that is, the dataset can be constructed as usual by following the transformations on each commit, that's what will happen.

If some commit does not make sense and generates integrity issues. The commits will be marked as corrupt and the `index.py` file is simply reverted to the last non-corrupt commit via a revert commit.

Git status will always indicate if the index.py files are truthful or not. Checking out commits and branches will always issue a warning if an index.py file is not truthful. The lest non-corrupted commit is included in the large commit message.





## Dependency on git ? Isn't it a large learning curve, especially for someone not familiar to git ?

Yes, I love git, this a git extension. 

For someone who uses git, this will be second nature to them. That is my objective at least.

Since this is a git extension, anyone not familiar with git must learn it first !

## Examples

### Medical dataset

```python
@dataset
class MedicalDiagnosisDataset:
    patient_id: str
    age: int
    weight: float
    height: float
    mri_scan: File[dicom]
    radiologist_note: File[txt]
    diagnosis: str

    # Initial method to populate the dataset from the hospital database
    def fetch_initial_data() -> Action.Insert[{
        "patient_id": str,
        "age": int,
        "weight": float,
        "height": float,
        "mri_scan": File[dicom],
        "radiologist_note": File[txt],
        "diagnosis": str,
    }]:
        ... # fetch from a medical DB, ensuring data privacy and de-identification
        return [
            ("patient_001", 45, 70.5, 175.0, mri_1, note_1, "Benign"),
            ("patient_002", 56, 80.2, 180.0, mri_2, note_2, "Malignant"),
            ...
        ]

    # Field representing normalized MRI scans
    def normalized_mri(mri_scan: File[dicom]) -> File[dicom]:
        ... # apply some normalization techniques on the MRI scan
        return processed_mri

    # Field representing the summarized points from radiologist's notes
    def radiologist_key_findings(radiologist_note: File[txt]) -> str:
        ... # use NLP techniques to extract essential points
        return findings_summary

    # Vertical transformation to exclude patients below a certain age
    def filter_by_age(age: int) -> Action.Delete:
        return age < 18

    # Verification that MRI scans meet certain quality criteria
    def ensure_mri_quality(mri_scan: File[dicom]) -> None:
        ... # load the dicom file and check its properties
        assert quality_check(mri_scan)
```


## Previous Work

- https://github.com/iterative/dvc
- https://github.com/dolthub/dolt

## Important stuff 

- https://spark.apache.org/
- https://parquet.apache.org/
- https://delta.io/
- https://libcloud.apache.org

<p align="right">(<a href="#readme-top">back to top</a>)</p>






