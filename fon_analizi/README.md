# TEFAS / BEFAS Fon Analizi

Bu klasör, Fintables verisi kullanılarak hazırlanan TEFAS yatırım fonu ve BEFAS emeklilik fonu karar destek raporunu içerir.

- **RAPOR.md** — Ana rapor (Türkçe, 11 bölüm: yönetici özeti, metodoloji, TEFAS/BEFAS genel görünüm, karşılaştırma tabloları, risk-getiri analizi, fon sepeti analizi, model portföy çerçeveleri, izleme kuralları, sonuç ve uyarılar, kullanıcıdan istenen ek bilgiler).
- **data/** — Rapordaki tüm tabloların kaynağı olan ham/işlenmiş CSV dosyaları:
  - `tefas_islem_goren_master.csv` — TEFAS'ta işleme açık 1.057 yatırım fonunun tam kimlik/kategori/maliyet/büyüklük verisi.
  - `befas_islem_goren_master.csv`, `befas_diger_emeklilik_master.csv` — BEFAS/emeklilik fonlarının iki alt grubu (311 + 116 fon).
  - `tefas_kategori_ozet.csv`, `befas_islem_goren_kategori_ozet.csv`, `befas_klasik_kategori_ozet.csv` — Kategori bazında fon sayısı ve büyüklük özetleri.
  - `one_cikan_fonlar_performans_risk.csv` — Kategori başına en büyük 3 fonun (173 fon) dönemsel getiri, volatilite, maksimum düşüş ve Calmar oranı.
  - `kategori_getiri_risk_ornek_ozet.csv` — Kategori bazında örneklem getiri/risk özeti.
  - `portfoy_dagilim_ornek.csv` — 173 fonun güncel varlık sınıfı dağılımı (%5 üstü kalemler).
  - `ornek_secilen_fonlar_listesi.csv` — Derin analiz için seçilen 173 fonun listesi ve seçim gerekçesi (kategori başına en büyük 3 fon).

Veri kaynağı: Fintables (fintables.com), bu oturumda MCP arayüzü üzerinden SQL ile sorgulanmıştır. Veri tarihi ve kısıtlar için RAPOR.md'nin 1. ve 2. bölümlerine bakınız. Bu rapor yatırım tavsiyesi değildir.
