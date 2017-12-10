from django.db import connection
from django.db.models import QuerySet


class DateQuerySet(QuerySet):
    def after_date(self, date):
        return self.in_dates(from_date=date)

    def before_date(self, date):
        return self.in_dates(to_date=date)

    def in_dates(self, from_date=None, to_date=None):
        qs = self

        if from_date:
            qs = qs.filter(date_created__gte=from_date)

        if to_date:
            qs = qs.filter(date_created__lte=to_date)

        return qs


class TrackHistorySnapshotQuerySet(QuerySet):
    def bulk_create(self, *args, **kwargs):
        raise NotImplementedError

    def create(self, *args, **kwargs):
        raise NotImplementedError

    def get_or_create(self, *args, **kwargs):
        raise NotImplementedError

    def delete(self, *args, **kwargs):
        raise NotImplementedError

    delete.queryset_only = True

    def update(self, *args, **kwargs):
        raise NotImplementedError

    def create_snapshot_for_model(self, **kwargs):
        """Runs query which creates row snapshot."""
        query = """INSERT INTO {snapshot_table}(history_data)
            VALUES (COALESCE((SELECT row_to_json({data_table}) FROM {data_table} WHERE id = %s), '{{}}')::jsonb)
            RETURNING {snapshot_table_pk};""".format(
            snapshot_table=self.model._meta.db_table,
            snapshot_table_pk=self.model._meta.pk.column,
            data_table=kwargs.get('model')._meta.db_table
        )

        with connection.cursor() as cursor:
            cursor.execute(query, [kwargs.get('raw_id')])
            snapshot_id = cursor.fetchone()

        return snapshot_id[0] if snapshot_id else None
