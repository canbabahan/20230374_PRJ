"""Odunc sınıfı için birim testleri."""

import pytest
from models.odunc import Odunc
from utils.dogrulama import DogrulamaHatasi


class TestOduncOlusturma:
    """Odunc nesnesi oluşturma testleri."""

    def test_gecerli_odunc_olusturma(self):
        """Geçerli parametrelerle ödünç oluşturulabilmeli."""
        odunc = Odunc("ODC001", "U001", "9786051005294", "01.01.2024")
        assert odunc.odunc_id == "ODC001"
        assert odunc.uye_id == "U001"
        assert odunc.isbn == "9786051005294"
        assert odunc.aktif is True
        assert odunc.iade_tarihi is None

    def test_bos_uye_id_hata_firlatir(self):
        """Boş üye ID ile hata fırlatılmalı."""
        with pytest.raises((DogrulamaHatasi, ValueError)):
            Odunc("ODC002", "", "9786051005294", "01.01.2024")

    def test_bos_isbn_hata_firlatir(self):
        """Boş ISBN ile hata fırlatılmalı."""
        with pytest.raises((DogrulamaHatasi, ValueError)):
            Odunc("ODC003", "U001", "", "01.01.2024")

    def test_iade_tarihiyle_olusturma(self):
        """İade tarihiyle oluşturulan ödünç aktif olmamalı."""
        odunc = Odunc(
            "ODC004", "U001", "1234567890",
            "01.01.2024", "10.01.2024"
        )
        assert odunc.iade_tarihi == "10.01.2024"
        assert odunc.aktif is False


class TestOduncIade:
    """Ödünç iade işlemleri testleri."""

    @pytest.fixture
    def aktif_odunc(self):
        """Test için aktif ödünç nesnesi."""
        return Odunc("ODC005", "U001", "1234567890", "01.01.2024")

    def test_iade_tarihi_guncellenir(self, aktif_odunc):
        """İade tarihi set edilince güncellenmeli."""
        aktif_odunc.iade_tarihi = "15.01.2024"
        assert aktif_odunc.iade_tarihi == "15.01.2024"

    def test_iade_sonrasi_aktif_degil(self, aktif_odunc):
        """İade edilince ödünç aktif olmamalı."""
        aktif_odunc.iade_tarihi = "15.01.2024"
        assert aktif_odunc.aktif is False

    def test_bos_iade_tarihi_hata(self, aktif_odunc):
        """Boş iade tarihi hata fırlatmalı."""
        with pytest.raises((DogrulamaHatasi, ValueError)):
            aktif_odunc.iade_tarihi = ""


class TestOduncSerilestime:
    """Odunc serileştirme testleri."""

    def test_to_dict_tam_veri(self):
        """to_dict tüm gerekli alanları içermeli."""
        odunc = Odunc("ODC006", "U001", "1234567890", "01.01.2024")
        veri = odunc.to_dict()
        assert veri["odunc_id"] == "ODC006"
        assert veri["aktif"] is True
        assert veri["iade_tarihi"] is None

    def test_from_dict_nesne_olusturur(self):
        """from_dict doğru Odunc nesnesi oluşturmalı."""
        veri = {
            "odunc_id": "ODC007",
            "uye_id": "U002",
            "isbn": "9876543210",
            "odunc_tarihi": "05.01.2024",
            "iade_tarihi": None,
            "aktif": True,
        }
        odunc = Odunc.from_dict(veri)
        assert odunc.uye_id == "U002"
        assert odunc.aktif is True
