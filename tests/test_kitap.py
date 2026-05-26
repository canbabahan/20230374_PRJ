"""Kitap sınıfı için birim testleri."""

import pytest
from models.kitap import Kitap
from utils.dogrulama import DogrulamaHatasi


class TestKitapOlusturma:
    """Kitap nesnesi oluşturma testleri."""

    def test_gecerli_kitap_olusturma(self):
        """Geçerli parametrelerle kitap başarıyla oluşturulmalı."""
        kitap = Kitap("9786051005294", "Python 101", "Ahmet Yılmaz", 2021)
        assert kitap.isbn == "9786051005294"
        assert kitap.kitap_adi == "Python 101"
        assert kitap.yazar == "Ahmet Yılmaz"
        assert kitap.yil == 2021
        assert kitap.musait is True

    def test_gecersiz_isbn_hata_firlatir(self):
        """Geçersiz ISBN ile hata fırlatılmalı."""
        with pytest.raises((DogrulamaHatasi, ValueError)):
            Kitap("123", "Kitap", "Yazar", 2020)

    def test_bos_kitap_adi_hata_firlatir(self):
        """Boş kitap adıyla hata fırlatılmalı."""
        with pytest.raises((DogrulamaHatasi, ValueError)):
            Kitap("9786051005294", "   ", "Yazar", 2020)

    def test_gecersiz_yil_hata_firlatir(self):
        """Geçersiz yıl ile hata fırlatılmalı."""
        with pytest.raises((DogrulamaHatasi, ValueError)):
            Kitap("9786051005294", "Kitap", "Yazar", 9999)


class TestKitapOzellikleri:
    """Kitap getter/setter testleri."""

    @pytest.fixture
    def ornek_kitap(self):
        """Test için örnek kitap nesnesi."""
        return Kitap("9786051005294", "Python 101", "Ali Veli", 2021)

    def test_kitap_adi_guncelleme(self, ornek_kitap):
        """Kitap adı setter ile güncellenebilmeli."""
        ornek_kitap.kitap_adi = "Python 202"
        assert ornek_kitap.kitap_adi == "Python 202"

    def test_musaitlik_guncelleme(self, ornek_kitap):
        """Müsaitlik durumu güncellenebilmeli."""
        ornek_kitap.musait = False
        assert ornek_kitap.musait is False

    def test_musaitlik_gecersiz_tur_hata(self, ornek_kitap):
        """Müsaitliğe bool dışı değer atanması hata vermeli."""
        with pytest.raises(ValueError):
            ornek_kitap.musait = "evet"


class TestKitapSerilestime:
    """Kitap serileştirme testleri."""

    def test_to_dict_tam_veri(self):
        """to_dict tüm alanları içermeli."""
        kitap = Kitap("1234567890", "Test Kitap", "Test Yazar", 2000)
        veri = kitap.to_dict()
        assert veri["isbn"] == "1234567890"
        assert veri["kitap_adi"] == "Test Kitap"
        assert veri["musait"] is True

    def test_from_dict_nesne_olusturur(self):
        """from_dict doğru Kitap nesnesi oluşturmalı."""
        veri = {
            "isbn": "1234567890",
            "kitap_adi": "Test Kitap",
            "yazar": "Test Yazar",
            "yil": 2000,
            "musait": False,
        }
        kitap = Kitap.from_dict(veri)
        assert kitap.isbn == "1234567890"
        assert kitap.musait is False

    def test_str_temsili(self):
        """__str__ Müsait veya Ödünçte bilgisi içermeli."""
        kitap = Kitap("1234567890", "Test", "Yazar", 2000)
        assert "Müsait" in str(kitap)
