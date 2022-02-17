# Contributor guidelines
Thank you for reading this document and considering contributing to a COSSAS product. With every contribution, we improve the quality of these products. To help you with a potential contribution, we have crafted this document. 

## Why should I contribute?
COSSAS is a community for open-source security automation software that we are creating and improving together. Contributing to community will benefit us all, so just do it!

## What do I need to know to help?
If you are looking to help to improve one of the COSSAS products with a code contribution, you might want to read more about the product first. First, have a look at our [website](https://cossas-project.org) to see where this product came from, what's it trying to achieve and what the status of this product is. Afterwards, have a look at the [issues on Gitlab](https://gitlab.com/cossas/dgad/-/issues) to find the problems you might want to solve. If you just want to help others with this COSSAS product, responding to issues is also much appreciated. 

In short if you want to know more about a COSSAS product:
- Read the product entry on our [website](https://cossas-project.org/portfolio/dga-detective/)
- Browse through the list of [issues on GitLab](https://gitlab.com/cossas/dgad/-/issues)

### GitLab vs GitHub
Most of the COSSAS products are the results of TNO projects and TNO uses GitLab internally for software development. Therefor, continuous integration and continuous deployment (CI/CD) is done through GitLab pipelines. To easily open source TNO projects, the COSSAS initiative decided to host all software on [GitLab](https://gitlab.com/cossas) with a push mirroring to [GitHub](https://github.com/cossas). So, if you are reading this document on GitHub and want to make a contribution, please switch over the [GitLab](https://gitlab.com/cossas/dgad/) to continue!

## How do I contribute?
Any contribution is appreciated, and many don’t imply coding. Contributions can range from a suggestion for improving documentation, requesting a new feature, reporting a bug, to developing features or fixing bugs yourself. 

If you're ready to contribute by coding and want to make your first contribution to a COSSAS product, but you're not that familiar with contributing to open-source software, we have included a useful step-by-step tutorial how to contribute:

1. Find an issue that you are interested in addressing or think of a feature that you would like to add. 
1. Fork the repository to your GitLab account. This means that you will have a copy of the repository under **your-GitLab-username/repository-name**.
1. Clone the repository to your local machine using `git clone https://gitlab.com/your-GitLab-username/repository-name.git`.
1. Create a new branch for your fix using `git checkout -b [fix/feature]-branch-name-here`. Please use the `fix` prefix if you are fixing stuff, and `feature` if you are adding a new feature. 
1. Make the necessary changes for the issue you are trying to fix or the feature that you want to add.
1. Use `git add the-files-you-want-to-include` to add the file contents of the changed files to the "snapshot" git uses to manage the state of the project, also known as the index.
1. Use `git commit -m "Insert a short message of the changes made here"` to store the contents of the index with a descriptive message.
1. Push the changes to the remote repository using `git push origin branch-name-here`.
1. Submit a pull request to the upstream repository. This means that you request your fork to be merged with the COSSAS product main branch.
1. Title the pull request with a short description of the changes made and the issue number associated with your change. For example, you can title an issue like so "Added more log outputting to resolve #435".
1. In the description of the pull request, explain the changes that you made, any issues you think exist with the pull request you made, and any questions you have for the maintainer. It's OK if your pull request is not perfect (no pull request is), the reviewer will be able to help you fix any problems and improve it!
1. Wait for the pull request to be reviewed by a maintainer or any other member in the community. We encourage every contributor to collaborate as much as possible! We really appreciate it when contributor review each other’s pull requests. 
1. Make changes to the pull request if the reviewing maintainer recommends them.
1. Celebrate your success after your pull request is merged!

## Where can I go for help?
If you need help, you can ask your questions in a separate [Gitlab issue](https://gitlab.com/cossas/dgad/-/issues) or email them. You can find our email address at our [contact page](https://cossas-project.org/contact/).

## What does the Code of Conduct mean for me?
Our [Code of Conduct](https://gitlab.com/cossas/home/-/blob/main/CODE_OF_CONDUCT.md) means that you are responsible for treating everyone on the project with respect and courtesy regardless of their identity. If you are the victim of any inappropriate behavior or comments as described in our [Code of Conduct](https://gitlab.com/cossas/home/-/blob/main/CODE_OF_CONDUCT.md), we are here for you and will do the best to ensure that the abuser is reprimanded appropriately, per our code.
