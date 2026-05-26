"""Entegrasyon testleri: 2'li ve 3'lü modül kombinasyonları."""

import pytest
from services.kitap_service import KitapService
from services.uye_service import UyeService
from services.odunc_service import OduncService
from utils.dogrulama import (
    KitapBulunamadiHatasi,
    UyeBulunamadiHatasi,
    OduncLimitiAsimHatasi,
)


@pytest.fixture
def gecici_dizin(tmp_path):
    """Her test için geçici veri dizini sağlar."""
    return str(tmp_path)


@pytest.fixture
def kitap_service(gecici_dizin):
    """Test için KitapService örneği."""
    return KitapService(veri_dizini=gecici_dizin)


@pytest.fixture
def uye_service(gecici_dizin):
    """Test için UyeService örneği."""
    return UyeService(veri_dizini=gecici_dizin)


@pytest.fixture
def odunc_service(kitap_service, uye_service, gecici_dizin):
    """Test için OduncService örneği."""
    return OduncService(kitap_service, uye_service, gecici_dizin)


# ============================================================
# 2'li Entegrasyon Testleri: KitapService + OduncService
# ============================================================

class TestKitapOduncEntegrasyon:
    """KitapService ile OduncService entegrasyon testleri."""

    def test_odunc_alma_kitap_musait_degil_olur(
        self, kitap_service, uye_service, odunc_service
    ):
        """Ödünç alındığında kitap müsait olmamalı."""
        kitap_service.kitap_ekle(
            "1234567890", "Test Kitap", "Yazar A", 2020
        )
        uye_service.uye_ekle("U001", "Ali", "Veli", "ali@test.com")
        odunc_service.odunc_al("U001", "1234567890")
        kitap = kitap_service.kitap_getir("1234567890")
        assert kitap.musait is False

    def test_iade_sonrasi_kitap_musait_olur(
        self, kitap_service, uye_service, odunc_service
    ):
        """İade edilince kitap tekrar müsait olmalı."""
        kitap_service.kitap_ekle(
            "1234567891", "Test Kitap 2", "Yazar B", 2021
        )
        uye_service.uye_ekle("U002", "Ayşe", "Kaya", "ayse@test.com")
        odunc_service.odunc_al("U002", "1234567891")
        odunc_service.iade_et("U002", "1234567891")
        kitap = kitap_service.kitap_getir("1234567891")
        assert kitap.musait is True

    def test_odunc_alinmis_kitap_tekrar_odunc_alinamaz(
        self, kitap_service, uye_service, odunc_service
    ):
        """Ödünçteki kitap başka üyeye verilmemeli."""
        kitap_service.kitap_ekle(
            "1234567892", "Paylaşılamaz Kitap", "Yazar C", 2019
        )
        uye_service.uye_ekle("U003", "Can", "Ak", "can@test.com")
        uye_service.uye_ekle("U004", "Elif", "Yıl", "elif@test.com")
        odunc_service.odunc_al("U003", "1234567892")
        with pytest.raises(ValueError):
            odunc_service.odunc_al("U004", "1234567892")


# ============================================================
# 2'li Entegrasyon Testleri: UyeService + OduncService
# ============================================================

class TestUyeOduncEntegrasyon:
    """UyeService ile OduncService entegrasyon testleri."""

    def test_olmayan_uye_odunc_alamaz(
        self, kitap_service, uye_service, odunc_service
    ):
        """Sistemde olmayan üye ödünç alamamalı."""
        kitap_service.kitap_ekle(
            "9999999999", "Kitap X", "Yazar X", 2018
        )
        with pytest.raises(UyeBulunamadiHatasi):
            odunc_service.odunc_al("HAYALET_UYE", "9999999999")

    def test_odunc_limit_asimi(
        self, kitap_service, uye_service, odunc_service
    ):
        """Üye limitini aşınca hata fırlatılmalı."""
        uye_service.uye_ekle("U010", "Limit", "Test", "limit@test.com")
        for i in range(3):
            isbn = f"000000000{i}"
            kitap_service.kitap_ekle(
                isbn, f"Kitap {i}", "Yazar", 2020
            )
            odunc_service.odunc_al("U010", isbn)
        kitap_service.kitap_ekle(
            "0000000099", "Fazla Kitap", "Yazar", 2020
        )
        with pytest.raises(OduncLimitiAsimHatasi):
            odunc_service.odunc_al("U010", "0000000099")


# ============================================================
# 3'lü Entegrasyon Testleri: Kitap + Uye + Odunc birlikte
# ============================================================

class TestUcluEntegrasyon:
    """Kitap, Uye ve Odunc servislerinin birlikte testleri."""

    def test_tam_odunc_dongusu(
        self, kitap_service, uye_service, odunc_service
    ):
        """Tam ödünç döngüsü: ekle→kaydet→ödünç al→iade."""
        kitap_service.kitap_ekle(
            "5555555555", "Döngü Kitabı", "Döngü Yazar", 2022
        )
        uye_service.uye_ekle(
            "U020", "Döngü", "Testi", "dongu@test.com"
        )
        odunc = odunc_service.odunc_al("U020", "5555555555")
        assert odunc.aktif is True
        kitap = kitap_service.kitap_getir("5555555555")
        assert kitap.musait is False
        odunc_service.iade_et("U020", "5555555555")
        kitap_sonra = kitap_service.kitap_getir("5555555555")
        assert kitap_sonra.musait is True

    def test_ogrenci_yuksek_limit_tam_senaryo(
        self, kitap_service, uye_service, odunc_service
    ):
        """Öğrenci üye 4 kitap alabilmeli (standart limit 3)."""
        uye_service.ogrenci_uye_ekle(
            "OGR001", "Öğrenci", "Test",
            "ogrenci@uni.edu.tr", "20230001", "Bilgisayar"
        )
        for i in range(4):
            isbn = f"777777777{i}"
            kitap_service.kitap_ekle(
                isbn, f"Ders Kitabı {i}", "Prof", 2023
            )
            odunc_service.odunc_al("OGR001", isbn)
        aktif = odunc_service.aktif_oduncleri_listele("OGR001")
        assert len(aktif) == 4
