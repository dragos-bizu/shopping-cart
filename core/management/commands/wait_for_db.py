import time

from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand
from typing import Any, Optional


class Command(BaseCommand):
    """Django command to pause execution until db is available"""

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        self.stdout.write("Waiting for DB...")
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections["default"]
            except OperationalError:
                self.stdout.write("Database unavailable, waiting 1 second")
                time.sleep(1)
            self.stdout.write(self.style.SUCCESS("Database available!"))
