# How to contribute to this Repo

The following is a set of guidelines for contributing to **_ExpertSystem_** and its packages hosted in the MES-CoBraD Organization on GitHub (**_mescobrad-project_**). These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

## Bug Report

There are two different ways to report a bug, either by opening a Git issue or creating a Jira Bug task.
You are free to describe it in the best way possible but use clear and descriptive information to be able to reproduce it.
It will be helpful to provide an image or other useful information.

## Branching

### Model

The current repo utilizes the following branching model:

| Branch      | Type       | Description                                          |
| ----------- | ---------- | ---------------------------------------------------- |
| master      | Production | Presents the latest production-ready app version     |
| development | Staging    | Used for QAing and Validating the latest app version |
| release/\*  | Release    | Prefix for version release branches                  |
| feature/\*  | Feature    | Prefix for creating app features                     |
| hotfix/\*   | Hotfix     | Prefix for fixing critical production bugs           |
| bugfix/\*   | Bugfix     | Prefix for creating fixes for various bugs           |

In more detail:

-   **_master_**: it's the main production branch used to present the latest production version.
-   **_development_**: it's the "testing" branch used to QA and test the latest version before hitting production.
-   **_release/\*_**: each branch with this prefix holds the corresponding version of the app. They are used to keep support for old versions.
-   **_feature/\*_**: each branch with this prefix is used to address new app features.
-   **_hotfix/\*_**: each branch with this prefix is used to address a critical production bug that needs to be pushed asap.
-   **_bugfix/\*_**: each branch with this prefix is used to address app bugs that are found and need to be solved.

### Pipeline

Whenever you need to contribute to this repo, keep in mind that the following pipeline is followed:

| Step | Branch                                     | Example              | GOTO        |
| ---- | ------------------------------------------ | -------------------- | ----------- |
| 1    | - feature/\*<br>- hotfix/\*<br>- bugfix/\* | feature/test_feature | development |
| 2    | development                                | development          | master      |
| 3    | master                                     | master               | -           |

In more detail:

**_Step 1_**: Do most of the work here. Feature branches add a minor version, and bug/hotfix branches add a patch version. After committing, create a pull request on the appropriate release branch. Make sure to pass all tests.

**_Step 2_**: After the merge, pull changes and update the staging server to make a QA or other desired test. If every test is passed, then create a pull request to master.

**_Step 3_**: After the merge, pull changes and update the version accordingly for git and docker tags.

## Suggesting Enhancements

### Submitting Changes

#### Commit

The only accepted commits are on branches under the following prefixes:

-   feature
-   hotfix
-   bugfix

> Please make commits as short as possible and provide clear titles and descriptions

#### Pull Requests

Every change you want to introduce will need to be accepted and approved to keep everything under control. The strategy to see your suggestions in production is to create a series of pull requests starting with the release branches and ending with the main branch.

> Please keep in mind to add details and clear descriptions to each pull request

## Coding Conventions

Start reading our code and you'll get the hang of it. We optimize for readability:

-   We indent using four spaces (soft tabs)
-   We ALWAYS put spaces after list items and method parameters (`[1, 2, 3]`, not `[1,2,3]`), around operators (`x += 1`, not `x+=1`), and around hash arrows.
-   Consider the people who will read your code, and make it look nice for them.

### Git Commit Messages

-   Use the present tense ("Add feature" not "Added feature")
-   Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
-   Limit the first line to 72 characters or less
-   Reference issues and pull requests liberally after the first line
-   When only changing documentation, include `[ci skip]` in the commit title
-   Consider starting the commit message with an applicable emoji:
    -   :art: `:art:` when improving the format/structure of the code
    -   :racehorse: `:racehorse:` when improving performance
    -   :memo: `:memo:` when writing docs
    -   :bug: `:bug:` when fixing a bug
    -   :fire: `:fire:` when removing code or files
    -   :green_heart: `:green_heart:` when fixing the CI build
    -   :white_check_mark: `:white_check_mark:` when adding tests
    -   :lock: `:lock:` when dealing with security
    -   :arrow_up: `:arrow_up:` when upgrading dependencies
    -   :arrow_down: `:arrow_down:` when downgrading dependencies
    -   :shirt: `:shirt:` when removing linter warnings
    -   Follow the full guide [here](https://gitmoji.dev/)
