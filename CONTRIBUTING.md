# Contribution Guidelines

:+1::tada: First off, thanks for taking the time to contribute! :tada::+1:
The following is a set of guidelines for contributing to CSC 510 Project 2 and its packages, which are hosted on the [GitHub project page](https://github.com/jaymodi98/Sync-Ends.git). These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.
#### Table Of Contents
[Code of Conduct](#code-of-conduct)
[What should I know before I get started?](#what-should-i-know-before-i-get-started)
[How Can I Contribute?](#how-can-i-contribute)
  * [Reporting Bugs](#reporting-bugs)
  * [Suggesting Enhancements](#suggesting-enhancements)
  * [Your First Code Contribution](#your-first-code-contribution)
  * [Pull Requests](#pull-requests)
  
[Styleguides](#styleguides)
  * [Coding Style](#coding-style)
  * [Git Commit Messages](#git-commit-messages)

## Code of Conduct
This project and everyone participating in it is governed by the [Code of Conduct](CODE-OF-CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to [cagandhi97@gmail.com](mailto:cagandhi97@gmail.com).

## What should I know before I get started?
This is a sample project that sets up some base project files for future work. Please look through the [README](README.md) file.
* For feature requests, please fork the repository, create a new branch with your feature changes and make a pull request. The maintainers will review the code change and merge it into the master branch once checks have successfully passed.
* Provide documentation for the modifications in the code. It will be easier and quicker for the maintainers to review and approve your code if you have added meaningful comments to your code change.

## How Can I Contribute?
### Reporting Bugs
This section guides you through submitting a bug report. Following these guidelines helps maintainers and the community understand your report :pencil:, reproduce the behavior :computer: :computer:, and find related reports :mag_right:.
Before creating bug reports, please check [this list](#before-submitting-a-bug-report) as you might find out that you don't need to create one. When you are creating a bug report, please include detailed information about the environment, package version numbers, OS and other information maintainers may find useful in reproducing and resolving issues quickly.
> **Note:** If you find a **Closed** issue that seems like it is the same thing that you're experiencing, open a new issue and include a link to the original issue in the body of your new one.
#### Before Submitting A Bug Report
Check that the bug does not exists because of any issue in your local environment. You might be able to find the cause of the problem and fix things yourself. If the problem has been reported **and the issue is still open**, add a comment to the existing issue instead of opening a new one.

#### How Do I Submit A (Good) Bug Report?
Explain the problem and include details to help maintainers reproduce the problem:
* **Use a clear and descriptive title** for the issue to identify the problem.
* **Describe the exact steps which reproduce the problem** in as many details as possible. When listing steps, **don't just say what you did, but explain how you did it**. 
* **Describe the behavior you observed after following the steps** and point out what exactly is the problem with that behavior.
* **Explain which behavior you expected to see instead and why.**
* **Include screenshots** that show the described steps and clearly demonstrate the problem.
Include details about your configuration and environment:
* **What's the name and version of the OS you're using**?
* **Which packages do you have installed?** Check that issue is not present because of a local package.
### Pull Requests
The process described here has several goals:
- Maintain the project's quality
- Fix problems that are important to users
- Engage the community in working toward the best possible Atom
- Enable a sustainable system for project maintainers to review contributions
Please follow these steps to have your contribution considered by the maintainers:
1. Follow the [styleguides](#styleguides)
2. After you submit your pull request, verify that the build is passing and the tests are successful.
While the prerequisites above must be satisfied prior to having your pull request reviewed, the reviewer(s) may ask you to complete additional design work, tests, or other changes before your pull request can be ultimately accepted.

## Styleguides
### Coding Style
* Use tab based indentation
* Make sure variables representing constants such as `DATA_FOLDER` and `FILE_PATH` should be capitalized.
### Git Commit Messages
* Use the present tense ("Add feature" not "Added feature")
* Use short, crisp and clear commit messages. It's easier to understand for everyone.
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Reference issues and pull requests liberally after the first line
* When only changing documentation, include `[ci skip]` in the commit title
* Consider starting the commit message with an applicable emoji:
    * :art: `:art:` when improving the format/structure of the code
    * :racehorse: `:racehorse:` when improving performance
    * :memo: `:memo:` when writing docs
    * :penguin: `:penguin:` when fixing something on Linux
    * :apple: `:apple:` when fixing something on macOS
    * :checkered_flag: `:checkered_flag:` when fixing something on Windows
    * :bug: `:bug:` when fixing a bug
    * :fire: `:fire:` when removing code or files
    * :green_heart: `:green_heart:` when fixing the CI build
    * :white_check_mark: `:white_check_mark:` when adding tests
