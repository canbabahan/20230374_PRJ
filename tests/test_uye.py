"""Uye ve OgrenciUye sınıfları için birim testleri."""

import pytest
from models.uye import Uye, OgrenciUye, STANDART_ODUNC_LIMITI, OGRENCI_ODUNC_LIMITI
from utils.dogrulama import DogrulamaHatasi


class TestUyeOlusturma:
    """Uye nesnesi oluşturma testleri."""

    def test_gecerli_uye_olusturma(self):
        """Geçerli parametrelerle üye oluşturulabilmeli."""
        uye = Uye("U001", "Ayşe", "Kaya", "ayse@test.com")
        assert uye.uye_id == "U001"
        assert uye.ad == "Ayşe"
        assert uye.soyad == "Kaya"
        assert uye.aktif is True

    def test_gecersiz_email_hata_firlatir(self):
        """Geçersiz email ile hata fırlatılmalı."""
        with pytest.raises((DogrulamaHatasi, ValueError)):
            Uye("U002", "Ali", "Veli", "gecersiz_email")

    def test_bos_ad_hata_firlatir(self):
        """Boş ad ile hata fırlatılmalı."""
        with pytest.raises((DogrulamaHatasi, ValueError)):
            Uye("U003", "", "Veli", "ali@test.com")

    def test_standart_odunc_limiti(self):
        """Standart üye doğru limiti döndürmeli."""
        uye = Uye("U004", "Test", "Kullanici", "t@test.com")
        assert uye.odunc_limit_al() == STANDART_ODUNC_LIMITI


class TestOgrenciUye:
    """OgrenciUye sınıfı testleri."""

    @pytest.fixture
    def ogrenci_uye(self):
        """Test için örnek öğrenci üye nesnesi."""
        return OgrenciUye(
            "O001", "Mehmet", "Demir",
            "mehmet@uni.edu.tr", "20210001", "Bilgisayar Müh."
        )

    def test_ogrenci_uye_olusturma(self, ogrenci_uye):
        """Öğrenci üye doğru alanlarla oluşturulmalı."""
        assert ogrenci_uye.ogrenci_no == "20210001"
        assert ogrenci_uye.bolum == "Bilgisayar Müh."

    def test_ogrenci_odunc_limiti_yuksek(self, ogrenci_uye):
        """Öğrenci üye standart üyeden yüksek limit almalı."""
        standart = Uye("U005", "Test", "User", "t2@test.com")
        assert ogrenci_uye.odunc_limit_al() > standart.odunc_limit_al()

    def test_ogrenci_limiti_dogru_deger(self, ogrenci_uye):
        """Öğrenci üye ödünç limiti doğru olmalı."""
        assert ogrenci_uye.odunc_limit_al() == OGRENCI_ODUNC_LIMITI

    def test_ogrenci_uye_kalitim(self, ogrenci_uye):
        """OgrenciUye, Uye'nin bir örneği olmalı."""
        assert isinstance(ogrenci_uye, Uye)


class TestUyeSerilestime:
    """Üye serileştirme testleri."""

    def test_uye_to_dict(self):
        """Üye to_dict tür bilgisi içermeli."""
        uye = Uye("U006", "Can", "Ak", "can@test.com")
        veri = uye.to_dict()
        assert veri["tur"] == "uye"
        assert veri["uye_id"] == "U006"

    def test_ogrenci_from_dict(self):
        """OgrenciUye from_dict doğru nesne oluşturmalı."""
        veri = {
            "uye_id": "O002",
            "ad": "Fatma",
            "soyad": "Çelik",
            "email": "fatma@uni.edu.tr",
            "ogrenci_no": "20220002",
            "bolum": "Yazılım",
            "aktif": True,
        }
        uye = OgrenciUye.from_dict(veri)
        assert uye.ogrenci_no == "20220002"
        assert uye.bolum == "Yazılım"
