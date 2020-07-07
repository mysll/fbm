#from scrapy.conf import settings
from scrapy.utils.project import get_project_settings
from scrapy.exporters import CsvItemExporter

class LeisuCsvItemExporter(CsvItemExporter):
    def __init__(self, *args, **kwargs):
        settings = get_project_settings()
        kwargs['fields_to_export'] = settings['EXPORT_FIELDS'] or None
        super(LeisuCsvItemExporter, self).__init__(*args,**kwargs)
