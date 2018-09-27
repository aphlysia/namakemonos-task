This is a regular task manager for sloths.


# Requiements

Currently, it works on Google App Engine.  
In addition, following softwares are required.

- pipenv


# Usage

```
git clone https://github.com/aphlysia/namakemonos-task.git
cd namakemonos-task
pipenv install
pipenv lock -r 2> /dev/null > requirements.txt
gcloud app deploy
```
