import os
import datetime
import atexit
import threading
import time
import shutil
from django.apps import AppConfig

# Backup directory - change this per system or use environment variable
BACKUP_DIR = os.getenv('BRAY_BACKUP_DIR', r"D:\Bray_db_backup")


class StandardAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'standard_app'
    backup_thread = None
    stop_thread = False
    mysqldump_available = False

    def ready(self):
        """Run when Django starts"""
        # Only run in the main process, not in reloader
        if os.environ.get('RUN_MAIN') == 'true':
            # Check if mysqldump is available before starting backup system
            self.mysqldump_available = shutil.which('mysqldump') is not None
            
            if not self.mysqldump_available:
                print("WARNING: mysqldump not found in PATH. Database backups will be disabled.")
                print("To enable backups, install MySQL and add mysqldump to system PATH.")
                return
            
            # Start backup monitor thread (will handle backup after delay)
            self.start_backup_monitor()
            # Register shutdown backup
            atexit.register(self.shutdown_backup)

    def start_backup_monitor(self):
        """Start background thread to check for backup"""
        if self.backup_thread is None or not self.backup_thread.is_alive():
            self.stop_thread = False
            self.backup_thread = threading.Thread(target=self.backup_monitor_loop, daemon=True)
            self.backup_thread.start()
            print(f"Backup monitor started (backup dir: {BACKUP_DIR})")

    def backup_monitor_loop(self):
        """Background loop that checks for backup"""
        # Wait 10 seconds for Django to fully initialize before first backup check
        time.sleep(10)
        
        while not self.stop_thread:
            self.check_and_run_backup()
            # Wait 100 seconds before next check
            for _ in range(100):
                if self.stop_thread:
                    break
                time.sleep(1)

    def check_and_run_backup(self):
        """Check if backup is needed and run it"""
        from django.core.management import call_command
        from django.db import connection
        
        try:
            # Check if backup already done today
            today = datetime.date.today().strftime("%Y-%m-%d")
            backup_file = os.path.join(BACKUP_DIR, f"backup_{today}.sql")
            
            if os.path.exists(backup_file):
                return  # Already backed up today, no need to print
            
            # Check if safe to backup (no tests running)
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT COUNT(*) 
                    FROM master_temp_data 
                    WHERE STATION_STATUS = 'Enabled'
                """)
                test_count = cursor.fetchone()[0]
            
            if test_count == 0:
                print("Starting daily database backup...")
                call_command('daily_db_backup')
            else:
                print(f"Backup skipped: {test_count} test(s) in progress")
                
        except Exception as e:
            print(f"Backup check failed: {e}")

    def shutdown_backup(self):
        """Run backup when Django shuts down"""
        from django.core.management import call_command
        
        # Stop the background thread
        self.stop_thread = True
        
        # Check if mysqldump is available
        if not self.mysqldump_available:
            return
        
        try:
            # Check if backup already done today
            today = datetime.date.today().strftime("%Y-%m-%d")
            backup_file = os.path.join(BACKUP_DIR, f"backup_{today}.sql")
            
            if os.path.exists(backup_file):
                return  # Already backed up today
            
            # On shutdown, tests should be stopped, so just create backup
            print("\nShutdown: Creating daily database backup...")
            call_command('daily_db_backup')
                
        except Exception as e:
            print(f"Shutdown backup failed: {e}")
