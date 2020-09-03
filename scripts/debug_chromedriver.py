# pip install rpaframework
import logging
import subprocess
from RPA.Browser import Browser
from webdrivermanager import ChromeDriverManager


logging.basicConfig(
    level=logging.DEBUG,
    format="[{%(name)s:%(filename)s:%(lineno)d} %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(filename="debug.log", mode="w")],
)

logger = logging.getLogger(__name__)
cdm = ChromeDriverManager()


def runcmd(command, loglabel):
    info = subprocess.run(
        command, shell=True, capture_output=True, universal_newlines=True
    )
    logger.info(f"{loglabel} {info.stdout.strip()}")


runcmd("python --version", "PYTHON VERSION:")
runcmd("pip list", "PIP LIST:\n\n")
logger.info(f"ChromeDriverManager link path: {cdm.link_path}")
logger.info(f"ChromeDriverManager download root: {cdm.download_root}")

br = Browser()
br.open_available_browser("https://www.google.com")
br.close_all_browsers()
