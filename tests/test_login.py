import pytest
import logging
from pages.login_page import LoginPage

logger = logging.getLogger(__name__)

class TestLoginSauceDemo:
    """
    Tests para la página de login de Sauce Demo.
    Estos tests son REALES y ejecutables.
    """
    
    def test_login_with_valid_credentials(self, page):
        """
        Test 1: Login exitoso con credenciales válidas
        Verificar que el usuario puede entrar al sistema
        """
        # Arrange
        login_page = LoginPage(page)
        username = "standard_user"
        password = "secret_sauce"
        
        # Act
        login_page.navigate_to_login()
        login_page.login(username, password)
        
        # Assert
        assert login_page.is_logged_in(), "Login no fue exitoso - No se cargó página de productos"
        logger.info("✅ TEST PASSED: Login exitoso")
    
    def test_login_with_invalid_credentials(self, page):
        """
        Test 2: Login fallido con credenciales inválidas
        Verificar que se muestre mensaje de error
        """
        # Arrange
        login_page = LoginPage(page)
        username = "invalid_user"
        password = "wrong_password"
        
        # Act
        login_page.navigate_to_login()
        error_message = login_page.login_with_invalid_credentials(username, password)
        
        # Assert
        assert "Epic sadface" in error_message, "Mensaje de error no encontrado"
        assert "Username and password do not match" in error_message, "Mensaje de error específico no encontrado"
        logger.info("✅ TEST PASSED: Error message correcto")
    
    def test_login_with_locked_user(self, page):
        """
        Test 3: Login con usuario bloqueado
        Verificar que usuario bloqueado no puede entrar
        """
        # Arrange
        login_page = LoginPage(page)
        username = "locked_out_user"
        password = "secret_sauce"
        
        # Act
        login_page.navigate_to_login()
        error_message = login_page.login_with_invalid_credentials(username, password)
        
        # Assert
        assert "locked out" in error_message.lower(), "Mensaje de usuario bloqueado no encontrado"
        logger.info("✅ TEST PASSED: Usuario bloqueado detectado correctamente")
    
    def test_empty_username(self, page):
        """
        Test 4: Login sin username
        Verificar validación de campo vacío
        """
        # Arrange
        login_page = LoginPage(page)
        password = "secret_sauce"
        
        # Act
        login_page.navigate_to_login()
        error_message = login_page.login_with_invalid_credentials("", password)
        
        # Assert
        assert "Username is required" in error_message, "Error de username requerido no encontrado"
        logger.info("✅ TEST PASSED: Validación de username requerido funciona")
    
    def test_empty_password(self, page):
        """
        Test 5: Login sin password
        Verificar validación de password vacío
        """
        # Arrange
        login_page = LoginPage(page)
        username = "standard_user"
        
        # Act
        login_page.navigate_to_login()
        error_message = login_page.login_with_invalid_credentials(username, "")
        
        # Assert
        assert "Password is required" in error_message, "Error de password requerido no encontrado"
        logger.info("✅ TEST PASSED: Validación de password requerido funciona")