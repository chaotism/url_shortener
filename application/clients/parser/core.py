from typing import Optional, Generator
from contextlib import contextmanager
from queue import Queue
from config.client import ParserSettings
from loguru import logger
from queue import Queue
from pathlib import Path
from pydantic import HttpUrl
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
import undetected_chromedriver as uc

from common.constants import BASE_PATH
from clients.parser.proxies import get_proxy
from clients.parser.useragent import get_useragent
from poetry.core.constraints.version import Version  # TODO: check chrome version

from common.errors import ProviderError


def get_web_driver(headless: bool = True, proxy: Optional[str] = None, useragent: Optional[str] = None) -> uc.Chrome:
    options = uc.ChromeOptions()
    options.user_data_dir = Path(BASE_PATH, 'var', 'chrome_userdata')  # TODO: generate user data
    if headless:
        options.add_argument('--headless')
    if proxy:
        options.add_argument(f'--proxy-server={proxy}')
    if useragent:
        options.add_argument(f'--user-agent={useragent}')

    chrome = uc.Chrome(options=options)
    chrome.maximize_window()
    return chrome


@contextmanager
def get_web_drivers_pool(  # FIXME: crashed in one thread calling
    count: int,
    headless=True,
    proxy=False,
    random_useragent=False
) -> Generator[Queue[uc.Chrome], None, None]:
    driver_queue = Queue(maxsize=count)  # TODO: migrate to async queue
    try:
        for _ in range(count):
            driver_queue.put(
                get_web_driver(
                    headless=headless,
                    proxy=get_proxy() if proxy else None,
                    useragent=get_useragent() if random_useragent else None,
                )
            )
        yield driver_queue
    finally:
        while not driver_queue.empty():
            driver = driver_queue.get()
            driver.close()
            driver.quit()


class BaseParser:
    config: Optional[ParserSettings] = None  # TODO: could remove (its for debug only)
    client: Optional[uc.Chrome] = None

    @property
    def is_inited(self):
        return (
            self.config is not None and self.client is not None
        )

    def init(self, config: ParserSettings):
        if self.is_inited:
            logger.info('Already inited')
            return
        logger.info('Start initialising chrome client.....')
        self.config = config
        client = get_web_driver(
            headless=config.has_headless,
            useragent=get_useragent() if config.has_random_useragent else None,
            proxy=get_proxy() if config.has_proxies else None
        )
        self.client = client
        logger.info('Chrome client ready')

    def close_client(self):  # TODO: migrate to pool
        if not self.is_inited:
            logger.warning('Chrome client is not inited')
            return
        logger.info('Start closing client...')
        self.client.close()
        self.client.quit()
        logger.info('Client closed')

    def get_page(self, url: HttpUrl) -> uc.Chrome:
        if not self.is_inited:
            raise ProviderError('MongoMotorAdapter is not inited')
        logger.debug(f'Get page {url}')
        self.client.get(url)
        self.client.implicitly_wait(time_to_wait=0.3)  # TODD: remove it
        return self.client

    def get_elements(self, by: By, name: str) -> list[WebElement]:
        if not self.is_inited:
            raise ProviderError('MongoMotorAdapter is not inited')
        logger.debug(f'Get elements by {by} with value {name}')
        return self.client.find_elements(by, name)


parser_client = BaseParser()
