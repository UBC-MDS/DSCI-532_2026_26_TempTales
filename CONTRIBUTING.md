# Contributing

The following document outlines how each team member will contribute to
the project on this repository, as a part of the UBC Master of Data
Science program. Each member will follow the same guideline to ensure
code quality, reproducibility and smooth collaboration.

## Collaboration Strategy

- The `main` branch always contains stable and working code
- The `dev` branch contains the code that is under development
- All work is done on `feature branches` created from `dev`
- Changes are merged into `dev` using a PR (Pull Request), which should include:
  - at least one team member for review
  - a short description of what was changed
  - how it should be tested
- After testing, the `branch` can be merged into `dev` and can be
    deleted to keep the repository clean.
- Once the team is happy with the tested `dev` product, it is merged into `main`, corresponding to a new release version.

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

Changes are merged to `dev` through a Pull Request. Each PR should include:
    - brief description to changes.
    - any relevant verification steps.
    - Each PR should be assigned for review to at least one other team member.
    - PR feedback should be commented before merging to `main`

## Getting Started

### Clone the repository

``` bash
git clone https://github.com/UBC-MDS/DSCI-532_2026_26_TempTales.git
```

### Switch to `dev`

``` bash
git branch dev
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

- The collaborators demonstrate a consistent usage of **branching** strategy that ensured a clear and well managed workflow. Before merging into `dev`, at least one collaborator is required to review the PR and provide a constructive feedback or suggestion whenever needed.

- Clear guidelines of the code of conduct support and shape a clear collaboration.

### Scaling the Project

If this project were scaled to a larger or production-level application, additional tools and practices would be required. These include stronger code reviews, more tests, versioned releases, and better dependency management. Automated deployment and CI/CD pipelines would help maintain reliability as the project grows.

## Code of Conduct

All the team members are expected to follow those guidelines to support
an effective collaboration ([code of
conduct](CODE_OF_CONDUCT.md))

## M3 Retrospective

During Milestone 3, our team continued to work from the feature branch to `dev` to `main` framework, which worked well. This helped maintain a stable working version of the app and reduced the likelihood of merge conflicts. Also, we always had another team member review PR requests before merging.

However, several areas could be improved upon:

- While we evaluated another team member's PR, we did not explicitly add comments in the PR describing what was checked. We had more of a discussion on Slack about whether there were any issues, but this should have been done more transparently on the issues log.
- Work distribution across the team could be improved so that coding tasks can be shared more evenly.

These observations informed the collaboration norms we adopted in Milestone 4.

## M4 Norms

For Milestone 4, we committed to the following practices:

- We will use PRs as an opportunity to track appraisal by logging comments or discussions.
- We will make sure that an issue is created before coding begins. This will help with modular PRs and keep them task-specific for better tracking.
- We will link issues in the PR messaging for tracking of project development.
- Coding tasks should be distributed across team members to provide opportunities for everyone to contribute.
- We will avoid last-minute commits to try to have a more balanced implementation/merging of code so that we can maintain our best practices for code development.

These norms were intended to improve coordination and maintain a clear project history.
