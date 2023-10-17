



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

**At its core, git-datasets is an attempt at introducing a "data as code" paradigm.** Imagine being able to commit, revert, restore, pull, push, merge, resolve conflicts, open a PR and review data just as you do with code. All right from git and with minimal setup.

## How are you planning to do that ?

Every dataset has an `index.py` file. The promise? A committed `index.py` always tells the truth. Every transformation occurs on `git commit` of this file. Let's say you want a dataset with images and object segmentations. Your `index.py` could look like this:

```python
@dataset
class SegmentationDataset:
    image: File[png | jpg]
    segmentation: File[png]
```

First, you set this up as a dataset using `git datasets new index.py`, then you save it with `git commit`. When you do this, an sqlite file is made to keep track of everything and folders named `image/` and `segmentation/` are created. 

Whenever you modify and commit the file, the corresponding updates take place.

A git history of your dataset is kept in parallel to the actual git history of your repository. 

## Where are files going ?

Files go into the `.git` folder and are symlinked to where they need to be.

They are uploaded to your chosen cloud provider - at this stage, I will only support aws s3.

You link the repository to a bucket once. That link is stored in `.git`, but of course,  credentials are requested on a per-user basis and never stored in the repository.


## How would you add data ?

Declare a method with return type `Action.Insert`:

```python
@dataset
class SegmentationDataset:
    image: File[png | jpg]
    segmentation: File[png]

    def get_data_from_web(image: File[png | jpg], segmentation: File[png]) -> Action.Insert:
        # since the declared actions is `Insert`. the values
        # of the arguments `image` and `segmentation` are set
        # to `None`

        ... # perform some requests, massage data into the correct form

        # the order of the returned values must match
        # the order of the function arguments
        return list_of_image, list_of_segmentation
```

this method is called once on the first time it is commited.


## How would you transform data ?

All data transformations will happen on commit, leaving a traceable history of everything that happened to the dataset. 

For example, I might want to resize the orignal image and have it as a new feature for the dataset:

```python

@dataset
class SegmentationDataset:
    image: File[png | jpg]
    segmentation: File[png]

    def image_resized(image: File[png | jpg]) -> File[png]:

        ... # perform resize

        return file # instance of `File[png]``

```

Commiting this results in the creation of a new field, `image_resized` with type `File[png]`, and in the application of the transformation to populate that field.

Additionally, multi-stage transformations are possible:


```python

@dataset
class SegmentationDataset:
    image: File[png | jpg]
    segmentation: File[png]

    def image_resized(image: File[png | jpg]) -> File[png]:
        ... # perform resize
        return file # instance of `File[png]``

    def image_resized_plus_brightness(image_resized: File[png]) -> File[png]:
        ... # add brightness
        return file # instance of `File[png]``

    def image_plus_resized(image: File[png | jpg], image_resized: File[png]) -> File[png]:
        ... # do stuff with both files
        return file # instance of `File[png]``

```

# And vertical transformations ?

For editing individual rows you can use `Action`:

```python
@dataset
class SegmentationDataset:
    image: File[png | jpg]
    segmentation: File[png]

    def delete_corrupted_files(image: File[png | jpg]) -> Action.Delete:
        ... # perform some checks, get image_is_corrupted: bool
        return True if image_is_corrupted else False
```

Note that by declaring `Action` as a return type, you inform git-datasets that a new field is not to be created (like in the previous example), instead, current values will be altered.

Transformations always occur once, on the first time they are commited.

For more control over which rows you are iterating:

```python
@dataset
class SegmentationDataset:
    image: File[png | jpg]
    segmentation: File[png]

    @range(1, 10, 3)
    def transformation_2(image: File[png | jpg]) -> Action.Delete:
        ... # perform some checks
        return False if image_checks_out else True

    @index(10)
    def transformation_3() -> Action.Delete:
        ... # perform some checks
        return True

    @index(11)
    def transformation_4(image: File[png | jpg], segmentation: File[png]) -> Action.Alter:
        ... # get data
        return new_image, new_segmentation
```

You can also declare `None` as the return type for no action. This is useful if you want to implement some check:

```python
@dataset
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
@dataset
class SegmentationDataset:

    image_segmentation: File[png]

    @index(11)
    def transformation_4(image: File[jpg | png]) -> Action.Alter:
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

Not a hard requirement and will be changed at later stages. I will likely support various db types. 

## Isn't it a lot of overhead added to git commands ?

Depends on the dataset size and the transformations you are doing.

A lot will be done to aliviate this issue:

- a `@skip` decorator that let's you commit a transformation without running it (so you can share it)
- transformations fetch data on demand and only the data that is needed to populate the fields
- a `@cicd` decorator so that certain transformations can be delegated to a remote somewhere 

on top of this, note that:

The command

```
git commit index.py
```

will process data only if:

- a new transformation is added
- new data is added
- results from a current transformation are missing

the dataset is not processed from scratch, only the "deltas" in the `index.py` file can cause a change.

```
git checkout
```

will just change the contents of `index.py` file. The file structure only changes when you do `git pull` afterwards.


```
git push
```

will only upload the files that are not already in remote. Data integrity checks are done before pushing. Deduplication is in place.


But even so - this does not scale for medium-large, large and collossal datasets. My only answer to this is, if there's a real need later, I'll build a self-hosted solution that let's people offload a lot of the work to a remote. Right now, this is a one man side project. In the end, the objective is for me to push myself to the limits while trying to solve what I perceive to be a real problem in the comunity.


## What happens when there is a merge conflict ?

Merge conflicts are resolved directly in the `index.py` file. The state of the dataset can always be derived from its previous commit and its current commit. So after resolving a conflict, that's what determines what happens to the data.

## What happens if someone commits without `git-datasets` ?

This will happen. A merge conflict might get resolved on github's interface. Someone might commit without having git datasets installed. Etc.

If the commits make sense, that is, the dataset can be constructed as usual by following the transformations on each commit, that's what will happen.

If some commit does not make sense and generates integrity issues. The commits will be marked as corrupt and the `index.py` file is simply reverted to the last non-corrupt commit via a revert commit.

Git status will always indicate if the index.py files are truthful or not. Checking out commits and branches will always issue a warning if an index.py file is not truthful. The lest non-corrupted commit is included in the large commit message.

## But the index.py file doesn't really paint the whole picture. What happens when conflicts occur on details that `index.py` is not aware of ?

The full picture is painted by the commit history.

Inside the `.git` folder I will be keeping sparse checkpoints of the database.

Each commit might have a checkpoint, or it might have a diff tha transforms the last checkpoint into the desired state.

Diffs are kept in the cloud provider and once they are there, they cannot be unlinked from a commit.



That's true, while a commited `index.py` file is always truthful, by allowing transformations to be removed it will never really paint the whole picture. Painting the full picture is not the point, , the point is to paint an accurate and sufficient picture of the dataset so that you not only know what's going on at a glance, but also so that a lot of details can be assumed due to the trust mechanism. The full picture is told via the commit history of the `index.py` file.




## How do you inspect data ?

Files are stored in folders with the same name as the fields in the schema. The name of each file has the form `[id].[checksum].[mimetype]`, for example: `21.2ef7bde608ce5404e97d5f042f95f89f1c232871.png`. So they can inspected quite easily. As for the database:

```
python index.py --sql-shell
```

which will open the sqlite shell in read only mode. 

## There's quite a lot of hidden complexity here, especially when it comes to resolving conflicts.

Yes.

At this point, it is not obvious to me how I can fight it. So I'm just gonna go on a trial and error basis, get some experience with the problem and brainstorm ideas later.

For the first prototype, I'm going to assume that these conflicts don't occur. For the second, I'll assume they only occur on the local machine, for the third I'll account for remote changes. By the fourth, I'll be able to truly address this problem.

In the end, my focus is going to be on **not adding another layer of complexity to the git commands**. My objective is for this tool to be invisible, so reliable that you forget it is there - this might not be possible, but I won't find out until I get to a later stage.

## Dependency on git ?

Yes, I love git, this a git extension. 

## Isn't it a large learning curve, especially for someone not familiar to git ?

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
    def fetch_initial_data(
        patient_id: str,
        age: int,
        weight: float,
        height: float,
        mri_scan: File[dicom],
        radiologist_note: File[txt],
        diagnosis: str,
    ) -> Action.Insert:
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
    @range(0, 100, 1)
    def filter_by_age(age: int) -> Action | None:
        if age < 18:
            return Action.Delete
        return None

    # Verification that MRI scans meet certain quality criteria
    def ensure_mri_quality(mri_scan: File[dicom]) -> None:
        ... # load the dicom file and check its properties
        assert quality_check(mri_scan)
```


## Previous Work

- https://github.com/iterative/dvc
- https://github.com/dolthub/dolt


<p align="right">(<a href="#readme-top">back to top</a>)</p>






