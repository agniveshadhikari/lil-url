#


## Dev

Env vars are used extensively. Look for the `./.env` file, populate it.


### Using psql cli

```sh
psql "dbname=$DATABASE_DB user=$DATABASE_USERNAME password=$DATABASE_PASSWORD host=$DATABASE_HOST sslmode=require"
```
