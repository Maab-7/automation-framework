from playwright.sync_api import Page
import logging

logger = logging.getLogger(__name__)

class BasePage:
    """
    Clase base que contiene métodos comunes para todos los page objects.
    Aplica el principio DRY (Don't Repeat Yourself).
    """
    
    def __init__(self, page: Page):
        """
        Constructor
        Args:
            page: Playwright Page object
        """
        self.page = page
    
    def navigate(self, url: str):
        """Navega a una URL"""
        self.page.goto(url)
        logger.info(f"Navegó a: {url}")
    
    def click(self, locator: str):
        """
        Click en un elemento con espera y manejo de errores
        Args:
            locator: CSS selector o XPath
        """
        try:
            element = self.page.locator(locator)
            element.wait_for(state="visible", timeout=10000)
            element.scroll_into_view_if_needed()
            element.click()
            logger.info(f"Click realizado en: {locator}")
        except Exception as e:
            logger.error(f"Error al hacer click en {locator}: {e}")
            self.take_screenshot("click_error")
            raise
    
    def fill(self, locator: str, text: str):
        """
        Rellena un campo de input
        Args:
            locator: CSS selector o XPath
            text: Texto a ingresar
        """
        try:
            element = self.page.locator(locator)
            element.wait_for(state="visible", timeout=10000)
            element.clear()
            element.fill(text)
            logger.info(f"Rellenó {locator} con texto: {text}")
        except Exception as e:
            logger.error(f"Error al rellenar {locator}: {e}")
            self.take_screenshot("fill_error")
            raise
    
    def wait_for_element(self, locator: str, timeout: int = 10000):
        """
        Espera a que un elemento sea visible
        Args:
            locator: CSS selector o XPath
            timeout: Milisegundos a esperar (default 10s)
        """
        try:
            self.page.locator(locator).wait_for(
                state="visible",
                timeout=timeout
            )
            logger.info(f"Elemento visible: {locator}")
        except Exception as e:
            logger.error(f"Timeout esperando elemento {locator}: {e}")
            self.take_screenshot("wait_error")
            raise
    
    def assert_text_present(self, text: str):
        """
        Verifica que un texto esté presente en la página
        Args:
            text: Texto a buscar
        """
        try:
            assert text in self.page.content()
            logger.info(f"Texto '{text}' encontrado en página")
        except AssertionError:
            logger.error(f"Texto '{text}' NO encontrado en página")
            self.take_screenshot("assert_error")
            raise
    
    def get_text(self, locator: str) -> str:
        """
        Obtiene el texto de un elemento
        Args:
            locator: CSS selector o XPath
        Returns:
            Texto del elemento
        """
        element = self.page.locator(locator)
        text = element.text_content() or ""
        logger.info(f"Texto obtenido de {locator}: {text}")
        return text
    
    def take_screenshot(self, name: str = "screenshot"):
        """
        Captura screenshot de la página
        Args:
            name: Nombre del archivo (sin extensión)
        """
        path = f"reports/{name}.png"
        self.page.screenshot(path=path)
        logger.info(f"Screenshot guardado: {path}")
    
    def is_element_visible(self, locator: str) -> bool:
        """
        Verifica si un elemento es visible
        Args:
            locator: CSS selector o XPath
        Returns:
            True si visible, False si no
        """
        try:
            element = self.page.locator(locator)
            return element.is_visible()
        except:
            return False