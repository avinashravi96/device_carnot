# Redis OM Python Flask Starter Application

We'll let Redis OM handle generation of unique IDs, which it does using [ULIDs](https://github.com/ulid/spec).  Redis OM will also handle creation of unique Redis key names for us, as well as saving and retrieving entities from JSON documents stored in a Redis Stack database.

## Getting Started

Let's go...

### Requirements

To run this application you'll need:

* [git](https://git-scm.com/download) - to clone the repo to your machine. 
* [Python 3.9 or higher](https://www.python.org/downloads/).
* A [Redis Stack](https://redis.io) database, or Redis with the [RediSearch](https://redisearch.io) and [RedisJSON](https://redisjson.io) modules installed.  We've provided a `docker-compose.yml` for this.  You can also [sign up for a free 30Mb database with Redis Enterprise Cloud](https://redis.com/try-free/) - be sure to check the Redis Stack option when creating your cloud database.
* [curl](https://curl.se/), or [Postman](https://www.postman.com/) - to send HTTP requests to the application.  We'll provide examples using curl in this document.
* Optional: [RedisInsight](https://redis.com/redis-enterprise/redis-insight/), a free data visualization and database management tool for Redis.  When downloading RedisInsight, be sure to select version 2.x or use the version that comes with Redis Stack.

### Start a Redis Stack Database, or Configure your Redis Enterprise Cloud Credentials

Next, we'll get a Redis Stack database up and running.  If you're using Docker:

```bash
$ docker-compose up -d

```

If you're using Redis Enterprise Cloud, you'll need the hostname, port number, and password for your database.  Use these to set the `REDIS_OM_URL` environment variable like this:

```bash
$ export REDIS_OM_URL=redis://default:<password>@<host>:<port>
```

(This step is not required when working with Docker as the Docker container runs Redis on `localhost` port `6379` with no password, which is the default connection that Redis OM uses.)

For example if your Redis Enterprise Cloud database is at port `9139` on host `enterprise.redis.com` and your password is `5uper53cret` then you'd set `REDIS_OM_URL` as follows:

```bash
$ export REDIS_OM_URL=redis://default:5uper53cret@enterprise.redis.com:9139
```

### Create a Python Virtual Environment and Install the Dependencies

Create a Python virtual environment, and install the project dependencies which are [Flask](https://pypi.org/project/Flask/), [Requests](https://pypi.org/project/requests/) (used only in the data loader script) and [Redis OM](https://pypi.org/project/redis-om/):

```bash
$ python3 -m venv venv
$ . ./venv/bin/activate
$ pip install -r requirements.txt
```

### Start the Flask Application

Let's start the Flask application in development mode, so that Flask will restart the server for you each time you save code changes in `app.py`:

```bash
$ export FLASK_ENV=development
$ flask run
```

If all goes well, you should see output similar to this:

```bash
$ flask run
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: XXX-XXX-XXX
```

You're now up and running, and ready to perform CRUD operations on data with Redis, RediSearch, RedisJSON and Redis OM for Python!  To make sure the server's running, point your browser at `http://127.0.0.1:5000/`, where you can expect to see the application's basic home page:

![screenshot](screenshots/server_running.png)

### Load the Sample Data

We've provided a small amount of sample data (it's in `data/raw.csv`.  The Python script `csv_to_redis.py` loads each device log into Redis by posting the data to the application's create a new device endpoint.  Run it like this:

```bash
$ python csv_to_redis.py
```

### Problems?

If the Flask server fails to start, take a look at its output.  If you see log entries similar to this:

```python
raise ConnectionError(self._error_message(e))
redis.exceptions.ConnectionError: Error 61 connecting to localhost:6379. Connection refused.
```

then you need to start the Redis Docker container if using Docker, or set the `REDIS_OM_URL` environment variable if using Redis Enterprise Cloud.

If you've set the `REDIS_OM_URL` environment variable, and the code errors with something like this on startup:

```python
raise ConnectionError(self._error_message(e))
redis.exceptions.ConnectionError: Error 8 connecting to enterprise.redis.com:9139. nodename nor servname provided, or not known.
```

then you'll need to check that you used the correct hostname, port, password and format when setting `REDIS_OM_URL`.

If the data loader fails to post the sample data into the application, make sure that the Flask application is running **before** running the data loader.

## API Documentation (POSTMAN)

[API Document link](https://documenter.getpostman.com/view/6060124/VUjMnkDf)



## Shutting Down Redis (Docker)

If you're using Docker, and want to shut down the Redis container when you are finished with the application, use `docker-compose down`:

```bash
$ docker-compose down
Stopping redis_om_python_flask_starter ... done
Removing redis_om_python_flask_starter ... done
Removing network redis-om-python-flask-skeleton-app_default
```
