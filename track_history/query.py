from django.db import connection
from django.db.models import QuerySet


class SnapshotQuerySet(QuerySet):
    def create_snapshot_for_model(self, **kwargs):
        """Runs query which creates row snapshot."""
        query = """INSERT INTO %(snapshot_table)s(history_data)
            VALUES (COALESCE((SELECT row_to_json(%(data_table)s) FROM %(data_table)s WHERE id = %%s), '{}')::jsonb)
            RETURNING %(snapshot_table_pk)s;""" % {
            'snapshot_table': self.model._meta.db_table,
            'snapshot_table_pk': self.model._meta.pk.column,
            'data_table': kwargs.get('model')._meta.db_table
        }

        with connection.cursor() as cursor:
            cursor.execute(query, [kwargs.get('row_id')])
            snapshot_id = cursor.fetchone()

        return snapshot_id[0] if snapshot_id else None
