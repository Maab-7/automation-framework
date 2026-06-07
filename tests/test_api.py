import requests
import logging

logger = logging.getLogger(__name__)

class TestBookingAPI:
    """
    Tests para API Restful Booker: https://restful-booker.herokuapp.com
    API pública para testing - perfecta para aprender API testing
    """
    
    BASE_URL = "https://restful-booker.herokuapp.com"
    
    def test_get_all_bookings(self):
        """Test GET - Obtener lista de bookings"""
        # Arrange
        url = f"{self.BASE_URL}/booking"
        
        # Act
        response = requests.get(url)
        
        # Assert
        assert response.status_code == 200, "Status debe ser 200"
        booking_ids = response.json()
        assert isinstance(booking_ids, list), "Response debe ser lista"
        assert len(booking_ids) > 0, "Debe haber al menos un booking"
        logger.info(f"✅ GET /booking: {len(booking_ids)} bookings encontrados")
    
    def test_create_booking(self):
        """Test POST - Crear un booking nuevo"""
        # Arrange
        url = f"{self.BASE_URL}/booking"
        payload = {
            "firstname": "Marco",
            "lastname": "Alfaro",
            "totalprice": 150,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2024-06-01",
                "checkout": "2024-06-05"
            },
            "additionalneeds": "Breakfast"
        }
        headers = {"Content-Type": "application/json"}
        
        # Act
        response = requests.post(url, json=payload, headers=headers)
        
        # Assert
        assert response.status_code == 200, "Status debe ser 200"
        response_data = response.json()
        assert "bookingid" in response_data, "Response debe tener bookingid"
        booking_id = response_data["bookingid"]
        logger.info(f"✅ POST /booking: Booking creado con ID {booking_id}")
        
        # Guardar para próximo test
        self.booking_id = booking_id
    
    def test_get_booking_detail(self):
        """Test GET - Obtener detalle de un booking específico"""
        # Arrange
        booking_id = 1  # Booking que sabemos existe
        url = f"{self.BASE_URL}/booking/{booking_id}"
        
        # Act
        response = requests.get(url)
        
        # Assert
        assert response.status_code == 200, "Status debe ser 200"
        booking = response.json()
        assert "firstname" in booking, "Response debe tener firstname"
        assert "lastname" in booking, "Response debe tener lastname"
        logger.info(f"✅ GET /booking/{booking_id}: {booking['firstname']} {booking['lastname']}")
    
    def test_get_nonexistent_booking(self):
        """Test GET - Obtener booking que NO existe (error 404)"""
        # Arrange
        booking_id = 999999  # Booking que no existe
        url = f"{self.BASE_URL}/booking/{booking_id}"
        
        # Act
        response = requests.get(url)
        
        # Assert
        assert response.status_code == 404, "Status debe ser 404"
        logger.info(f"✅ GET /booking/{booking_id}: Correctly retorna 404")
    
    def test_create_booking_invalid_data(self):
        """Test POST - Crear booking con datos inválidos"""
        # Arrange
        url = f"{self.BASE_URL}/booking"
        payload = {
            "firstname": "",  # INVÁLIDO: vacío
            "lastname": "Alfaro",
            "totalprice": -100,  # INVÁLIDO: negativo
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2024-06-05",  # INVÁLIDO: checkout antes de checkin
                "checkout": "2024-06-01"
            }
        }
        headers = {"Content-Type": "application/json"}
        
        # Act
        response = requests.post(url, json=payload, headers=headers)
        
        # Assert
        # Esta API acepta datos inválidos, pero nosotros verificamos
        # que al menos NO crashea (no error 5xx)
        assert response.status_code < 500, "No debe retornar error 5xx"
        logger.info(f"✅ POST con datos inválidos: Status {response.status_code}")