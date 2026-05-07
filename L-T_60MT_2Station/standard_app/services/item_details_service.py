import json
from django.db import connection, transaction

class ItemDetailsService:
    @staticmethod
    def _to_camel_case(text):
        """Convert text to Camel Case (each word capitalized)"""
        if not text:
            return text
        return ' '.join(word.capitalize() for word in text.strip().split())

    @staticmethod
    def _to_storage(fields):
        """Convert array to object for storage (no array)."""
        return {str(i): f for i, f in enumerate(fields)}

    @staticmethod
    def _from_storage(data):
        """Convert stored object to array for API."""
        if isinstance(data, list):
            return data
        if isinstance(data, dict):
            keys = sorted(data.keys(), key=lambda k: int(k) if k.isdigit() else k)
            return [data[k] for k in keys]
        return []

    @staticmethod
    def get_all_item_details():
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, column_name, row_details, status
                FROM form_item_details
                ORDER BY id DESC
            """)
            columns = [col[0] for col in cursor.description]
            results = []
            for row in cursor.fetchall():
                item = dict(zip(columns, row))
                if isinstance(item.get('row_details'), str):
                    try:
                        raw = json.loads(item['row_details'])
                        item['row_details'] = ItemDetailsService._from_storage(raw)
                    except json.JSONDecodeError:
                        item['row_details'] = []
                else:
                    item['row_details'] = ItemDetailsService._from_storage(item.get('row_details') or {})
                results.append(item)
            return results

    @staticmethod
    def add_item_detail(data):
        fields = data.get('row_details')
        if isinstance(fields, str):
            try:
                fields = json.loads(fields)
            except json.JSONDecodeError:
                fields = []
        if isinstance(fields, list):
            stored = ItemDetailsService._to_storage(fields)
        else:
            stored = fields if isinstance(fields, dict) else {}
        row_details = json.dumps(stored)

        with transaction.atomic():
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO form_item_details (column_name, row_details, status)
                    VALUES (%s, %s, %s)
                """, [
                    ItemDetailsService._to_camel_case(data.get('column_name')),
                    row_details,
                    data.get('status', 'Enabled')
                ])
                last_id = cursor.lastrowid
            
        # After adding, sync all items to include any new labels
        ItemDetailsService.sync_all_item_labels(priority_id=last_id)
        return last_id

    @staticmethod
    def update_item_detail(detail_id, data):
        fields = data.get('row_details')
        if isinstance(fields, str):
            try:
                fields = json.loads(fields)
            except json.JSONDecodeError:
                fields = []
        if isinstance(fields, list):
            stored = ItemDetailsService._to_storage(fields)
        else:
            stored = fields if isinstance(fields, dict) else {}
        row_details = json.dumps(stored)

        with transaction.atomic():
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE form_item_details
                    SET column_name = %s, row_details = %s, status = %s
                    WHERE id = %s
                """, [
                    ItemDetailsService._to_camel_case(data.get('column_name')),
                    row_details,
                    data.get('status', 'Enabled'),
                    detail_id
                ])
                row_count = cursor.rowcount
            
        # After updating, sync all items to include any new labels
        ItemDetailsService.sync_all_item_labels(priority_id=detail_id)
        return row_count

    @staticmethod
    def delete_item_detail(detail_id):
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM form_item_details WHERE id = %s", [detail_id])
            return cursor.rowcount

    @staticmethod
    def bulk_delete_item_details(detail_ids):
        if not detail_ids:
            return 0
        with connection.cursor() as cursor:
            format_strings = ','.join(['%s'] * len(detail_ids))
            cursor.execute(f"DELETE FROM form_item_details WHERE id IN ({format_strings})", detail_ids)
            return cursor.rowcount

    @staticmethod
    def get_all_unique_row_labels(priority_id=None):
        """Fetch all unique field_names and their configurations across all items"""
        all_items = ItemDetailsService.get_all_item_details()
        label_configs = {}
        
        # If we have a priority item, its CURRENT set of labels should define the global set
        # to allow for DELETION of labels.
        active_priority_labels = None
        if priority_id:
            priority_id_int = int(priority_id)
            priority_item = next((i for i in all_items if int(i['id']) == priority_id_int), None)
            if priority_item:
                details = priority_item.get('row_details', [])
                active_priority_labels = set(f.get('field_name') for f in details if f.get('field_name'))

        # Sort items: older ID first, priority item LAST
        sorted_items = sorted(all_items, key=lambda x: (1 if priority_id and int(x['id']) == int(priority_id) else 0, int(x['id'])))
        
        for item in sorted_items:
            details = item.get('row_details', [])
            for field in details:
                name = field.get('field_name')
                if name:
                    # If we are syncing after a priority update, only keep labels that still exist in the priority item
                    if active_priority_labels is not None and name not in active_priority_labels:
                        continue
                    label_configs[name] = field
        
        # print(f"[DEBUG] Syncing labels with priority {priority_id}: {list(label_configs.keys())}")
        return label_configs

    @staticmethod
    def sync_all_item_labels(priority_id=None):
        """Ensure all items have the same set of row labels and types for consistent rendering"""
        label_configs = ItemDetailsService.get_all_unique_row_labels(priority_id)
        unique_labels = list(label_configs.keys())
        all_items = ItemDetailsService.get_all_item_details()
        
        with connection.cursor() as cursor:
            for item in all_items:
                current_details = item.get('row_details', [])
                # Not used for matching anymore, we want to enforce the master config
                # but we might want to keep some local state? 
                # Actually, the user wants to update data type and mandatory data too.
                # So we rebuild new_details according to label_configs order and content.
                
                new_details = []
                for label in unique_labels:
                    # Always use the configuration from our master map
                    new_details.append(label_configs[label])
                
                stored = ItemDetailsService._to_storage(new_details)
                row_details_json = json.dumps(stored)
                
                cursor.execute("""
                    UPDATE form_item_details 
                    SET row_details = %s 
                    WHERE id = %s
                """, [row_details_json, item['id']])
