import logging
import shutil
from datetime import datetime
from pathlib import Path

from .exceptions import SimpleBackupsError

logger = logging.getLogger(__name__)


def backup_file(filename: Path, backup_folder: Path, datetime_format: str = '%Y%m%d_%H%M%S',
                current_version: str = None, ) -> Path:
    if not backup_folder.is_dir():
        error_message = f'Backup folder has to be a folder.' f' Supplied: {backup_folder}. Type: {type(backup_folder)}'
        logger.error(error_message)
        raise SimpleBackupsError(error_message)

    backup_filename = build_filename(backup_folder, filename, current_version, datetime_format)
    if backup_filename == filename:
        error_message = f'Cannot overwrite backup file: {backup_filename}.'
        logger.error(error_message)
        raise SimpleBackupsError(error_message)
    try:
        shutil.copy(filename, backup_filename)
        return backup_filename
    except Exception as e:
        error_message = f'Unexpected error backing up file {filename}. Type: {e.__class__.__name__}' f' error: {e}'
        logger.error(error_message)
        raise SimpleBackupsError(error_message)


def build_filename(filename: Path, backup_folder: Path, current_version: str, datetime_format: str):
    if current_version is None:
        version_val = ''
    else:
        version_val = f'v{current_version}_'
    if datetime_format is None:
        timestamp_val = ''
    else:
        timestamp = datetime.now().strftime(datetime_format)
        timestamp_val = f'{timestamp}_'
    backup_filename = backup_folder / f'{timestamp_val}{version_val}{filename.name}'
    return backup_filename
