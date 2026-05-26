"""Sistem testleri: uçtan uca tam senaryolar."""

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
def sistem(tmp_path):
    """Tam sistem ortamını hazırlar (tüm servisler)."""
    dizin = str(tmp_path)
    ks = KitapService(veri_dizini=dizin)
    us = UyeService(veri_dizini=dizin)
    os_ = OduncService(ks, us, veri_dizini=dizin)
    return ks, us, os_


class TestSenaryo1_TamOduncSureci:
    """Senaryo 1: Üye kaydı → kitap ekleme → ödünç alma → iade."""

    def test_tam_senaryo_basarili(self, sistem):
        """Tam ödünç süreci hatasız tamamlanmalı."""
        kitap_servis, uye_servis, odunc_servis = sistem

        # 1. Üye kaydı
        uye = uye_servis.uye_ekle(
            "SIS001", "Sistem", "Testi", "sistem@test.com"
        )
        assert uye.uye_id == "SIS001"

        # 2. Kitap ekleme
        kitap = kitap_servis.kitap_ekle(
            "1111111111", "Sistem Testi Kitabı", "Sistem Yazar", 2024
        )
        assert kitap.musait is True

        # 3. Ödünç alma
        odunc = odunc_servis.odunc_al("SIS001", "1111111111")
        assert odunc.aktif is True
        assert kitap.musait is False

        # 4. Aktif ödünç listesinde görünmeli
        aktifler = odunc_servis.aktif_oduncleri_listele("SIS001")
        assert len(aktifler) == 1

        # 5. İade etme
        iade_odunc = odunc_servis.iade_et("SIS001", "1111111111")
        assert iade_odunc.aktif is False
        assert kitap.musait is True

        # 6. İade sonrası aktif ödünç listesi boş olmalı
        aktifler_sonra = odunc_servis.aktif_oduncleri_listele("SIS001")
        assert len(aktifler_sonra) == 0

    def test_iade_edilen_kitap_tekrar_odunc_alinabilir(self, sistem):
        """İade edilen kitap başka üye tarafından alınabilmeli."""
        kitap_servis, uye_servis, odunc_servis = sistem
        kitap_servis.kitap_ekle(
            "2222222222", "Tekrar Alınabilir", "Yazar", 2020
        )
        uye_servis.uye_ekle("SIS002", "Birinci", "Uye", "b@test.com")
        uye_servis.uye_ekle("SIS003", "Ikinci", "Uye", "i@test.com")

        odunc_servis.odunc_al("SIS002", "2222222222")
        odunc_servis.iade_et("SIS002", "2222222222")
        odunc2 = odunc_servis.odunc_al("SIS003", "2222222222")
        assert odunc2.uye_id == "SIS003"


class TestSenaryo2_GecersizIslemler:
    """Senaryo 2: Geçersiz işlem denemeleri."""

    def test_olmayan_uye_odunc_alamaz(self, sistem):
        """Sistemde olmayan üye ödünç alamamalı."""
        kitap_servis, uye_servis, odunc_servis = sistem
        kitap_servis.kitap_ekle(
            "3333333333", "Erişilemeyen Kitap", "Yazar", 2019
        )
        with pytest.raises(UyeBulunamadiHatasi):
            odunc_servis.odunc_al("HAYALET", "3333333333")

    def test_olmayan_kitap_odunc_alinamaz(self, sistem):
        """Sistemde olmayan kitap ödünç alınamamalı."""
        kitap_servis, uye_servis, odunc_servis = sistem
        uye_servis.uye_ekle(
            "SIS010", "Var", "Olan Uye", "var@test.com"
        )
        with pytest.raises(KitapBulunamadiHatasi):
            odunc_servis.odunc_al("SIS010", "0000000000")

    def test_standart_uye_limit_asimi(self, sistem):
        """Standart üye 3'ten fazla kitap alamamalı."""
        kitap_servis, uye_servis, odunc_servis = sistem
        uye_servis.uye_ekle(
            "SIS011", "Limit", "Testi", "lt@test.com"
        )
        for i in range(3):
            isbn = f"444444444{i}"
            kitap_servis.kitap_ekle(
                isbn, f"Kitap {i}", "Yazar", 2020
            )
            odunc_servis.odunc_al("SIS011", isbn)
        kitap_servis.kitap_ekle(
            "4444444449", "Limit Asimi", "Yazar", 2020
        )
        with pytest.raises(OduncLimitiAsimHatasi):
            odunc_servis.odunc_al("SIS011", "4444444449")

    def test_iki_kez_iade_edilemez(self, sistem):
        """İade edilmiş ödünç tekrar iade edilememeli."""
        kitap_servis, uye_servis, odunc_servis = sistem
        kitap_servis.kitap_ekle(
            "5555555550", "Tek İade", "Yazar", 2021
        )
        uye_servis.uye_ekle(
            "SIS012", "Tek", "Iade", "ti@test.com"
        )
        odunc_servis.odunc_al("SIS012", "5555555550")
        odunc_servis.iade_et("SIS012", "5555555550")
        with pytest.raises(ValueError):
            odunc_servis.iade_et("SIS012", "5555555550")
