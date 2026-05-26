"""Kütüphane Yönetim Sistemi - Ana konsol uygulaması."""

from services.kitap_service import KitapService
from services.uye_service import UyeService
from services.odunc_service import OduncService

MENU_METNI = """
========================================
    KÜTÜPHANe YÖNETİM SİSTEMİ
========================================
  1. Kitap Ekle
  2. Üye Ekle (Standart)
  3. Öğrenci Üye Ekle
  4. Ödünç Al
  5. İade Et
  6. Kitapları Listele
  7. Üyeleri Listele
  8. Aktif Ödünçleri Listele
  9. Kitap Ara
  0. Çıkış
========================================
Seçiminiz: """


def giris_al(mesaj):
    """Kullanıcıdan string giriş alır."""
    return input(mesaj).strip()


def kitap_ekle_menu(kitap_servis):
    """Kitap ekleme menüsünü işler."""
    print("\n--- Kitap Ekle ---")
    isbn = giris_al("ISBN: ")
    adi = giris_al("Kitap Adı: ")
    yazar = giris_al("Yazar: ")
    yil = giris_al("Yayın Yılı: ")
    kitap = kitap_servis.kitap_ekle(isbn, adi, yazar, yil)
    print(f"Kitap eklendi: {kitap}")


def uye_ekle_menu(uye_servis):
    """Standart üye ekleme menüsünü işler."""
    print("\n--- Üye Ekle ---")
    uye_id = giris_al("Üye ID: ")
    ad = giris_al("Ad: ")
    soyad = giris_al("Soyad: ")
    email = giris_al("Email: ")
    uye = uye_servis.uye_ekle(uye_id, ad, soyad, email)
    print(f"Üye eklendi: {uye}")


def ogrenci_uye_ekle_menu(uye_servis):
    """Öğrenci üye ekleme menüsünü işler."""
    print("\n--- Öğrenci Üye Ekle ---")
    uye_id = giris_al("Üye ID: ")
    ad = giris_al("Ad: ")
    soyad = giris_al("Soyad: ")
    email = giris_al("Email: ")
    ogrenci_no = giris_al("Öğrenci Numarası: ")
    bolum = giris_al("Bölüm: ")
    uye = uye_servis.ogrenci_uye_ekle(
        uye_id, ad, soyad, email, ogrenci_no, bolum
    )
    print(f"Öğrenci üye eklendi: {uye}")


def odunc_al_menu(odunc_servis):
    """Ödünç alma menüsünü işler."""
    print("\n--- Ödünç Al ---")
    uye_id = giris_al("Üye ID: ")
    isbn = giris_al("ISBN: ")
    odunc = odunc_servis.odunc_al(uye_id, isbn)
    print(f"Ödünç kaydı oluşturuldu: {odunc}")


def iade_et_menu(odunc_servis):
    """İade etme menüsünü işler."""
    print("\n--- İade Et ---")
    uye_id = giris_al("Üye ID: ")
    isbn = giris_al("ISBN: ")
    odunc = odunc_servis.iade_et(uye_id, isbn)
    print(f"İade işlemi tamamlandı: {odunc}")


def kitaplari_listele_menu(kitap_servis):
    """Tüm kitapları listeler."""
    print("\n--- Kitap Listesi ---")
    kitaplar = kitap_servis.tum_kitaplari_listele()
    if not kitaplar:
        print("Sistemde kayıtlı kitap yok.")
        return
    for kitap in kitaplar:
        print(f"  {kitap}")


def uyeleri_listele_menu(uye_servis):
    """Tüm üyeleri listeler."""
    print("\n--- Üye Listesi ---")
    uyeler = uye_servis.tum_uyeleri_listele()
    if not uyeler:
        print("Sistemde kayıtlı üye yok.")
        return
    for uye in uyeler:
        print(f"  {uye}")


def aktif_oduncleri_listele_menu(odunc_servis):
    """Aktif ödünçleri listeler."""
    print("\n--- Aktif Ödünçler ---")
    oduncler = odunc_servis.aktif_oduncleri_listele()
    if not oduncler:
        print("Aktif ödünç kaydı yok.")
        return
    for odunc in oduncler:
        print(f"  {odunc}")


def kitap_ara_menu(kitap_servis):
    """Kitap arama menüsünü işler."""
    print("\n--- Kitap Ara ---")
    terim = giris_al("Arama terimi (ad veya yazar): ")
    sonuclar = kitap_servis.kitap_ara(terim)
    if not sonuclar:
        print("Eşleşen kitap bulunamadı.")
        return
    for kitap in sonuclar:
        print(f"  {kitap}")


MENU_ISLEMLERI = {
    "1": kitap_ekle_menu,
    "2": uye_ekle_menu,
    "3": ogrenci_uye_ekle_menu,
    "6": kitaplari_listele_menu,
    "7": uyeleri_listele_menu,
    "9": kitap_ara_menu,
}

ODUNC_ISLEMLERI = {
    "4": odunc_al_menu,
    "5": iade_et_menu,
    "8": aktif_oduncleri_listele_menu,
}


def secim_isle(secim, kitap_servis, uye_servis, odunc_servis):
    """Menü seçimini işler ve ilgili fonksiyonu çağırır."""
    if secim in MENU_ISLEMLERI:
        if secim in ("1", "6", "9"):
            MENU_ISLEMLERI[secim](kitap_servis)
        else:
            MENU_ISLEMLERI[secim](uye_servis)
    elif secim in ODUNC_ISLEMLERI:
        ODUNC_ISLEMLERI[secim](odunc_servis)
    else:
        print("Geçersiz seçim. Lütfen tekrar deneyin.")


def ana_dongu(kitap_servis, uye_servis, odunc_servis):
    """Ana menü döngüsünü çalıştırır."""
    while True:
        try:
            secim = input(MENU_METNI).strip()
            if secim == "0":
                print("Çıkılıyor... Güle güle!")
                break
            try:
                secim_isle(secim, kitap_servis, uye_servis, odunc_servis)
            except (ValueError, KeyError, Exception) as hata:
                print(f"Hata: {hata}")
        except KeyboardInterrupt:
            print("\nProgram sonlandırıldı.")
            break


def main():
    """Uygulamanın giriş noktası."""
    print("Kütüphane Yönetim Sistemi başlatılıyor...")
    kitap_servis = KitapService()
    uye_servis = UyeService()
    odunc_servis = OduncService(kitap_servis, uye_servis)
    ana_dongu(kitap_servis, uye_servis, odunc_servis)


if __name__ == "__main__":
    main()
