from rest_framework.renderers import BaseRenderer

class CSVRenderer(BaseRenderer):
    media_type = 'text/csv'
    format = 'csv'
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        import csv
        from io import StringIO

        if not data:
            return ''

        if isinstance(data, dict) and 'results' in data:
            data = data['results']

        if not isinstance(data, list):
            data = [data]

        if not data:
            return ''

        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=data[0].keys())
        writer.writeheader()
        for row in data:
            writer.writerow(row)
        return output.getvalue() 