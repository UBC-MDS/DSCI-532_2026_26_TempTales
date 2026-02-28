# Contributing

The following document outlines how each team member will contribute to
the project on this repository, as a part of the UBC Master of Data
Science program. Each member will follow the same guideline to ensure
code quality, reproducibility and smooth collaboration.

## Collaboration Strategy

- The `main` branch always contains stable and working code
- All work is done on `feature branches` created from `main`
- Changes are merged into `main` using a PR (Pull Request), which should include:
  - at least one team member for review
  - a short description of what was changed
  - how it should be tested
- After testing, the `branch` can be merged into `main` and can be
    deleted to keep the repository clean.

### Branching

Each task is done on its own branch, and all the branches are deleted
after being merged.

### Issues and Project Management

- Github issues are used to plan, track and discuss work
- Issues are grouped according to Milestones
- Each issue is assigned to one team member
- Project boards are used to keep track of the progress

### Commits

Commits should be frequent and should clearly state how the solution was
managed. All the contributors are expected to make a comparable
number of commits throughout the project.

## Pull Requests

Changes are merged to `main` through a Pull Request. Each PR should include:
    - brief description to changes.
    - any relevant verification steps.
    - Each PR should be assigned for review to at least one other team member.
    - PR feedback should be commented before merging to `main`

## Getting Started

### Clone the repository

``` bash
git clone https://github.com/UBC-MDS/DSCI-532_2026_26_TempTales.git
```

### Create a new branch

``` bash
git switch -c feature/<name>
```

### Commit changes

``` bash
git add <files> 
git commit -m "Add a brief and descriptive message"
```

### Push changes to the branch

``` bash
git push origin <branch_name>
```

### Create a PR

Open a Pull Request on GitHub, link the issue, request a review from at
least one teammate and address the feedback before merging.

## Development Tools and Practices

The current project applies modern software tools and organizational practices to ensure quality, reproducibility and effective collaboration between each member of the team.

### Used Tools and Infrastructures

- **GitHub** was used as main tool for version control and communication. In order to reduce errors, branch-method and  Pull Requests (PR) were created effectively.

- **GitHub Issues and Project Boards** managed the division of the tasks, ensuring an even distribution of the workload and tracking of the milestones projects.

- **Environment Management** was ensured through `environment.yml` to ensure reproducibility across development environments

### Organizational Practices

- The collaborators demonstrate a consistent usage of **branching** strategy that ensured a clear and well managed workflow. Before merging into `main`, at least one collaborator is required to review the PR and provide a constructive feedback or suggestion whenever needed.

- Clear guidelines of the code of conduct support and shape a clear collaboration.

### Scaling the Project

If this project were scaled to a larger or production-level application, additional tools and practices would be required. These include stronger code reviews, more tests, versioned releases, and better dependency management. Automated deployment and CI/CD pipelines would help maintain reliability as the project grows.

## Code of Conduct

All the team members are expected to follow those guidelines to support
an effective collaboration ([code of
conduct](CODE_OF_CONDUCT.md))
