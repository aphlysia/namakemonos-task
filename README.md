Task manager for tasks like clearning, watering, and trainnig.


# Dependencies

It works on Google App Engine. Also, it uses,

- Google Cloud Datastore
- pipenv


# Usage

You need a GCP project and Cloud SDK. Please see the GAE document about them. Following steps supposes you have already had them.

```
git clone https://github.com/aphlysia/namakemonos-task.git
cd namakemonos-task
```

To run locally (but use Google Cloud Datastore),

```
pipenv install
pipenv run python main.py
```

To run on GAE,

```
pipenv lock -r 2> /dev/null > requirements.txt
gcloud app deploy
```


# Security

This software is not secure: no authentication and no encryption. Don't put any sensitive information.
