from pages.base_page import BasePage
from playwright.sync_api import Page
import logging

logger = logging.getLogger(__name__)

class LoginPage(BasePage):
    """
    Page Object para Sauce Demo Login Page.
    Aplicación real: https://www.saucedemo.com/
    """
    
    def __init__(self, page: Page):
        """Constructor - Locators para Sauce Demo"""
        super().__init__(page)
        
        # Locators para Sauce Demo (selectores correctos)
        self.username_input = "input#user-name"
        self.password_input = "input#password"
        self.login_button = "input#login-button"
        self.error_message = "h3[data-test='error']"
        self.products_title = "span.title"  # Título en página de productos
        self.menu_button = "button#react-burger-menu-btn"  # Para verificar login exitoso
    
    def navigate_to_login(self):
        """Navega a Sauce Demo"""
        self.navigate("https://www.saucedemo.com/")
        logger.info("Navegó a Sauce Demo")
    
    def login(self, username: str, password: str):
        """
        Realiza login con credenciales válidas
        Args:
            username: Usuario (ej: standard_user)
            password: Contraseña (ej: secret_sauce)
        """
        logger.info(f"Intentando login con usuario: {username}")
        
        # Rellena usuario
        self.fill(self.username_input, username)
        logger.info("Username ingresado")
        
        # Rellena contraseña
        self.fill(self.password_input, password)
        logger.info("Password ingresado")
        
        # Click en botón login
        self.click(self.login_button)
        logger.info("Click en login button")
        
        # Espera a que cargue la página de productos
        # Esto verifica que login fue exitoso
        self.wait_for_element(self.products_title, timeout=10000)
        logger.info("Login EXITOSO - Página de productos cargada")
    
    def login_with_invalid_credentials(self, username: str, password: str) -> str:
        """
        Intenta login con credenciales inválidas
        Args:
            username: Usuario incorrecto
            password: Contraseña incorrecta
        Returns:
            Mensaje de error
        """
        logger.info(f"Intentando login con credenciales inválidas")
        
        # Rellena usuario
        self.fill(self.username_input, username)
        
        # Rellena contraseña
        self.fill(self.password_input, password)
        
        # Click en botón login
        self.click(self.login_button)
        
        # Espera mensaje de error
        self.wait_for_element(self.error_message, timeout=5000)
        
        # Obtiene el mensaje de error
        error_text = self.get_text(self.error_message)
        logger.info(f"Error message recibido: {error_text}")
        
        return error_text
    
    def is_login_page_visible(self) -> bool:
        """Verifica si estamos en página de login"""
        return self.is_element_visible(self.username_input)
    
    def is_logged_in(self) -> bool:
        """Verifica si login fue exitoso (productos visibles)"""
        return self.is_element_visible(self.products_title)