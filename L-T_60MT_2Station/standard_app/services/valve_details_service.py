from django.db import connection

class ValveDetailsService:
    @staticmethod
    def _to_camel_case(text):
        """Convert text to Camel Case (each word capitalized)"""
        if not text:
            return text
        return ' '.join(word.capitalize() for word in text.strip().split())
    
    @staticmethod
    def get_all_valve_details():
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, column_name, data_type, is_mandatory, is_top_header, status
                FROM form_valve_details
                ORDER BY id ASC
            """)
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    @staticmethod
    def add_valve_detail(data):
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO form_valve_details (column_name, data_type, is_mandatory, is_top_header, status)
                VALUES (%s, %s, %s, %s, %s)
            """, [
                ValveDetailsService._to_camel_case(data.get('column_name')),
                data.get('data_type'),
                1 if data.get('is_mandatory') == 'on' or data.get('is_mandatory') is True else 0,
                1 if data.get('is_top_header') == 'on' or data.get('is_top_header') is True else 0,
                data.get('status', 'Enabled')
            ])
            return cursor.lastrowid

    @staticmethod
    def update_valve_detail(detail_id, data):
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE form_valve_details
                SET column_name = %s, data_type = %s, is_mandatory = %s, is_top_header = %s, status = %s
                WHERE id = %s
            """, [
                ValveDetailsService._to_camel_case(data.get('column_name')),
                data.get('data_type'),
                1 if data.get('is_mandatory') == 'on' or data.get('is_mandatory') is True else 0,
                1 if data.get('is_top_header') == 'on' or data.get('is_top_header') is True else 0,
                data.get('status', 'Enabled'),
                detail_id
            ])
            return cursor.rowcount

    @staticmethod
    def delete_valve_detail(detail_id):
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM form_valve_details WHERE id = %s", [detail_id])
            return cursor.rowcount

    @staticmethod
    def bulk_delete_valve_details(detail_ids):
        if not detail_ids:
            return 0
        with connection.cursor() as cursor:
            format_strings = ','.join(['%s'] * len(detail_ids))
            cursor.execute(f"DELETE FROM form_valve_details WHERE id IN ({format_strings})", detail_ids)
            return cursor.rowcount
