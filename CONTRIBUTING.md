We are happy that you want to contribute to our project! To get you started, we have collected a few things you should know in order to add helpful issues, well-formatted pull requests and well-structured code from the beginning:

### Contributing to the docs
* We use the [reST](https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html) format and compile the docs with sphinx.
* You can find the docs in the top level `docs` folder. After you installed the requirements from `docs/requirements.readthedocs.txt` with pip you can admire the beauty locally with `cd docs && make html` (`make clean` to clean up) or `docker-compose up && docker-compose run documentation make html` if you use docker. The generated files live in `docs/_build`. Once your code is merged into the main branch, the change will automatically be deployed to our [readthedocs page](https://match4everything.readthedocs.io/en/latest/?badge=latest).

### Contributing code
* Please use our issue and pull request templates. Github will automatically offer them to you. Our base-branch is `staging`.
* To ensure well-formatted code, we use [pre-commit](https://pre-commit.com/) hooks in git. Since they cannot be checked into the git history, please run `pre-commit install` in the repo folder after installing the requirements from `requirements.txt` with `pip3 install -r backend/requirements.txt`
* Our project is currently translated based on German and translated into English, please ensure the following requirements are met:
  * Whenever you write user-facing text, do it in a translatable way.
    * In django templates, that means surrounding your String with `blocktrans` tags like [here](https://docs.djangoproject.com/en/3.0/topics/i18n/translation/#blocktrans-template-tag). Use the `trimmed` keyword to prevent newlines from appearing in the po-file where they don't belong.
    * In python files, use `_("Text")` and add this line to your imports: `from django.utils.translation import gettext as _` which creates an alias for the [gettext function](https://docs.djangoproject.com/en/3.0/topics/i18n/translation/#standard-translation).
  * please use `python3 manage.py makemessages -l de --no-location` to generate missing translations and fill them out in `backend/locale/en/django.po`. If you are not fluent enough in one of them, state so and we will help you in the pull request.
* If you want to propose an idea or draft with code that is not ready to merge yet, please use the *Draft* option Github provides. Draft PRs can also be helpful to you, since we can give early feedback while knowing that it is still a work-in-progress.


If you have any questions, feel free to reach out to the maintaining developers @maltezacharias, @bjrne, @Baschdl, @kevihiin, @feeds, and @josauder.
