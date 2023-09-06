Django Track History
====================

A simple model change tracking for Django.

PostgreSQL exclusive as it uses some special database functions for better performance.


### Installation

```bash
pip install django-track-history
```

Then add `track_history` to `INSTALLED_APPS`.

And add `track_history.middleware.TrackHistoryMiddleware` to the `MIDDLEWARE` list. 

Decorate each model you want to track changes with `@track_changes`

```python
@track_changes
class Author(models.Model):
    ...
```


### Limitations

Django Track History does not track changes for bulk operations like `bulk_create` or `.objects.filter(...).update(...)`. It is related to how Django handles that kind of queries.


### Feature plans:
* Better deferred model tests and tests for more complicated model structures
* Django 2.0 support
* Admin interface
* EPIC: Handle bulk operations `bulk_create`, `.objects.filter(...).update(...)` (If it's even possible)


### Legal

Copyright (c) 2023, Arkadiusz Szydełko All rights reserved.

Licensed under BSD 3-Clause License
