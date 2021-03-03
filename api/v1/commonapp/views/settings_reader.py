import os
from api.settings import prod
settings = None
if os.environ["smart360_env"] == 'dev':
    from api.settings import dev
    settings = dev
if os.environ["smart360_env"] == 'prod':
    settings = prod
if os.environ["smart360_env"] == 'qa':
    settings = prod


class SettingReader:

    @staticmethod
    def get_display_date_format():
        try:
            return settings.DISPLAY_DATE_FORMAT
        except:
            pass

    @staticmethod
    def get_s3_credentials():
        try:
            data={
                "AWS_ACCESS_KEY":settings.AWS_ACCESS_KEY,
                "AWS_SECRET_KEY":settings.AWS_SECRET_KEY,
                "AWS_S3_BUCKET":settings.AWS_S3_BUCKET
                }
            return data
        except:
            pass

