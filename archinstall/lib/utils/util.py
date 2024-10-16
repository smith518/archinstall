from pathlib import Path
from typing import Any, TYPE_CHECKING, Optional, List

from ..output import FormattedOutput
from ..output import info
import subprocess
import logging

if TYPE_CHECKING:
	_: Any


def prompt_dir(text: str, header: Optional[str] = None) -> Path:
	if header:
		print(header)

	while True:
		path = input(text).strip(' ')
		dest_path = Path(path)
		if dest_path.exists() and dest_path.is_dir():
			return dest_path
		info(_('Not a valid directory: {}').format(dest_path))


def is_subpath(first: Path, second: Path) -> bool:
	"""
	Check if _first_ a subpath of _second_
	"""
	try:
		first.relative_to(second)
		return True
	except ValueError:
		return False


def format_cols(items: List[str], header: Optional[str] = None) -> str:
	if header:
		text = f'{header}:\n'
	else:
		text = ''

	nr_items = len(items)
	if nr_items <= 4:
		col = 1
	elif nr_items <= 8:
		col = 2
	elif nr_items <= 12:
		col = 3
	else:
		col = 4

	text += FormattedOutput.as_columns(items, col)
	return text



logger = logging.getLogger(_name_)

def detect_virtualization():
    try:
        result = subprocess.check_output(['systemd-detect-virt'], stderr=subprocess.STDOUT)
        logger.info(f"Virtualization detected: {result.decode().strip()}")
        return result.decode().strip()  # Return the virtualization type (if any)
    except subprocess.CalledProcessError as e:
        logger.error(f"Virtualization detection failed: {e.output.decode().strip()}")
        return "unknown"  # Return a default value indicating undetectable virtualization
