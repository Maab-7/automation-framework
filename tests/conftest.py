import pytest
from playwright.sync_api import sync_playwright
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.fixture
def browser():
    """Fixture que proporciona un browser"""
    playwright = sync_playwright().start()
    
    # CAMBIO: Usar FIREFOX en lugar de Chromium
    # Firefox es más estable en macOS
    browser = playwright.firefox.launch(headless=True)
    
    yield browser
    
    browser.close()
    playwright.stop()

@pytest.fixture
def page(browser):
    """Fixture que proporciona una página"""
    context = browser.new_context()
    page = context.new_page()
    yield page
    page.close()
    context.close()