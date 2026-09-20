# TEFAS ve BEFAS Fon Analizi — Karar Destek Raporu

**Veri tarihi:** 20 Eylül 2026 (fiyat verileri fon bazında 16–21 Eylül 2026 aralığında, fon büyüklüğü/nakit akışı verileri 16–21 Eylül 2026 aralığında güncellenmiştir; her tablo kendi veri tarihini taşır)
**Veri kaynağı:** Fintables (fintables.com) — `yatirim_fonlari`, `ohlcv` ve ilişkili veri setleri, bu oturumda MCP arayüzü üzerinden SQL ile sorgulanmıştır.
**Rapor niteliği:** Bu belge bir **yatırım tavsiyesi değildir**. Fon seçimine yardımcı olacak bir **uygunluk analizi, aday fon listesi, risk‑getiri karşılaştırması ve model portföy çerçevesidir**. Kesin alım‑satım emri, garanti getiri veya kesin gelecek tahmini içermez.

---

## 1. Yönetici Özeti

| Alan | Değer |
|---|---|
| Veri çekilme tarihi | 20 Eylül 2026 |
| Analiz edilen TEFAS yatırım fonu (mutual) — toplam evren | 2.356 fon (1.057 "işleme açık" + 1.299 "işleme kapalı/serbest" grubu) |
| Analiz edilen BEFAS/emeklilik fonu (pension) — toplam evren | 427 fon (311 "BEFAS bayrağı açık" + 116 "klasik/BEFAS bayrağı kapalı" grup) |
| Kapsam dışı bırakılan fon tipleri | 37 Borsa Yatırım Fonu (BYF/exchange), 10 Gayrimenkul Yatırım Fonu (GYF/realestate) — bu rapor TEFAS yatırım fonları ve BEFAS emeklilik fonlarına odaklanır, bu iki grup ayrı bir çalışmayı hak eder ve burada sadece varlığı not edilmiştir |
| Derinlemesine performans/risk incelemesi yapılan fon sayısı | 173 fon (her kategori içindeki en büyük 3 fon; bkz. Bölüm 2 — Kısıtlar) |

### En önemli bulgular

- **TEFAS yatırım fonu evreni** toplam ~4,84 trilyon TL büyüklüğünde 1.057 "işleme açık" fondan oluşuyor; en büyük kategori grupları Döviz Fonları (~1,97 trilyon TL, 98 fon) ve Para Piyasası Fonları (~752 milyar TL, 73 fon).
- Fintables verisinde **"tefasa_acik" bayrağı false olan** 1.299 mutual fon arasında, bazı çok büyük ve yüksek yatırımcı sayılı **para piyasası fonları** da yer almaktadır (ör. İş Portföy Para Piyasası (TL) Fonu – TI1, ~207 milyar TL / 233 bin yatırımcı). Bu, alanın "TEFAS'ta işlem görüyor/görmüyor" anlamına doğrudan karşılık gelmeyebileceğini, muhtemelen "yeni yatırımcı girişine/güncel alım satıma açık mı" gibi farklı bir operasyonel durumu (ör. kapatılmış/yenilenmiş şemsiye fon) yansıtabileceğini gösteriyor. **Bu alanın kesin anlamı resmi TEFAS kaynağından doğrulanmalıdır** (bkz. Bölüm 2, Veri Kalitesi Uyarıları).
- **BEFAS/emeklilik evreninde** benzer bir örüntü var: Fintables'ta "tefasa_acik=true" işaretli 311 emeklilik fonu çoğunlukla OKS (Otomatik Katılım Sistemi) ve nispeten küçük fonlardan oluşurken, Garanti, Allianz, Anadolu Hayat, Agesa gibi kurumların **milyarlarca TL büyüklüğündeki klasik BES fonları** (ör. Garanti Emeklilik Para Piyasası – GEL, ~112 milyar TL / 429 bin yatırımcı) "tefasa_acik=false" grubunda yer alıyor. Bu nedenle rapor bu iki grubu **ayrı** göstermekte, aralarında doğrudan sıralama yapmamaktadır.
- Örneklem bazında (kategori başına en büyük 3 fon, 173 fon), 1 yıllık medyan getiriler kategoriye göre **%7 ile %71 arasında** değişmektedir; en yüksek medyan getiriler Gümüş Fonları ve Emtia Fonları kategorilerinde, en düşükler Tematik ve Kar Payı Ödeyen (Döviz) kategorilerinde gözlenmiştir. Getiri farklarının büyük kısmı varlık sınıfı ve döviz/altın duyarlılığından kaynaklanmaktadır, fon yöneticisi becerisinden değil.
- **Aykırı değer uyarısı:** TLY kodlu "Tera Portföy Birinci Serbest Fon" örneklemde 1 yıllık getiri olarak **%640** göstermektedir; bu, aynı kategorideki diğer fonların (medyan ~%46) çok üzerindedir ve **muhtemelen bir birim/pay değeri düzeltmesi, füzyon veya baz değişikliğinden kaynaklanan veri anomalisidir**. Bu fonun performansı, yatırım kararına dayanak yapılmadan önce resmi TEFAS verisiyle ayrıca doğrulanmalıdır.
- **Sharpe/Sortino oranları bu oturumda hesaplanamamıştır** — nedeni Bölüm 2'de açıklanmıştır. Bunun yerine, risksiz getiriye ihtiyaç duymayan **Calmar oranı (getiri / maksimum düşüş)** hesaplanmış ve tablolara eklenmiştir.

### Veri kalitesi uyarıları (özet)

- "tefasa_acik" alanının TEFAS/BEFAS işlem durumunu ne ölçüde birebir yansıttığı belirsizdir (yukarıda açıklanmıştır).
- 472 TEFAS yatırım fonu Fintables'ın kendi kategori sınıflandırmasında yer almamaktadır ("Kategorisiz" olarak işaretlenmiştir).
- BEFAS emeklilik fonları için Fintables'ın kategori tablosu yalnızca "OKS" başlığını içermektedir; bu raporda emeklilik fonu kategorisi olarak fonun **şemsiye fon (semsiye_fon)** alanı kullanılmıştır.
- Sharpe, Sortino, beta/korelasyon (BIST endeksine göre) ve maliyet kalemlerinden "giriş/çıkış komisyonu" bu oturumda hesaplanamamış veya bulunamamıştır; nedenleri Bölüm 2'de ayrı ayrı belirtilmiştir.
- Derinlemesine risk/getiri analizi, **evrenin tamamı için değil, her kategorideki en büyük 3 fon için** yapılmıştır (173 fon). Bu, aşağıda gerekçelendirilen bilinçli bir kapsam sınırlamasıdır.

### Kullanıcının eksik profil bilgileri

Bu rapor hazırlanırken kullanıcıdan **yatırım amacı, tutarı, vadesi, risk profili, likidite ihtiyacı, TEFAS/BEFAS tercihi, BES sözleşmesi durumu ve mevcut portföy bilgisi alınmamıştır**. Bu nedenle rapor **kişiye özel bir fon sıralaması veya oran önerisi içermemekte**, bunun yerine düşük/orta/yüksek risk için **örnek (model) profiller** sunmaktadır (Bölüm 8). Eksik profil bilgisi, kararın kişiselleştirme kalitesini doğrudan düşürmektedir; Bölüm 11'de bu bilgiler kullanıcıdan talep edilmektedir.

---

## 2. Veri ve Metodoloji

### Kaynaklar

- **Fintables MCP** — `yatirim_fonlari` veri seti: `fonlar`, `gunluk_fon_degerleri`, `gunluk_fon_varlik_sinifi_dagilimlari`, `fon_kategorileri`, `fon_kategori_iliskileri`, `portfoy_yonetim_sirketleri` tabloları.
- **Fintables MCP** — `ohlcv` veri seti: `mumlar_gunluk_gh` (günlük fon fiyatı/NAV serisi).
- Sorgular bu oturumda `mcp__Fintables__veri_sorgula` (salt okunur SQL) aracıyla doğrudan çalıştırılmıştır; ham SQL çıktıları oturum kayıtlarında saklıdır (denetlenebilirlik).
- Resmi TEFAS (tefas.gov.tr) ve SPK verisiyle **çapraz doğrulama bu oturumda yapılmamıştır** — bu, aşağıdaki Kısıtlar bölümünde açık bir sınırlama olarak belirtilmiştir. Fintables ile resmi kaynak arasında bir tutarsızlık şüphesi oluşan tek alan **"tefasa_acik"** bayrağıdır (Bölüm 1'de açıklanmıştır); bu alan kullanılmadan önce tefas.gov.tr üzerinden doğrulanmalıdır.

### Kullanılan tarih aralığı

- Kimlik/büyüklük/nakit akışı verileri: fon bazında en güncel kayıt (16–21 Eylül 2026 arası, fona göre değişir).
- Fiyat/getiri verileri: 20 Eylül 2026 tarihine göre geriye dönük 1 ay, 3 ay, 6 ay, yılbaşı (31 Aralık 2025), 1 yıl, 3 yıl, 5 yıl referans noktaları.
- Risk (volatilite, maksimum düşüş): son 1 yıllık günlük getiri serisi (~250 gözlem).

### Hesaplama yöntemleri

- **Getiri:** `(son fiyat / referans tarihindeki fiyat − 1) × 100`, basit (kümülatif) getiri olarak hesaplanmıştır; bileşik/yıllıklandırılmış değildir (1 ve 3 yıllık getiriler için yıllıklandırma yapılmamış, dönemin toplam getirisi verilmiştir — tablolarda "dönem getirisi" olarak etiketlenmiştir).
- **Yıllıklandırılmış volatilite:** Son 1 yıllık günlük basit getirilerin standart sapması × √252 × 100. Frekans: **günlük**. Yıllıklandırma varsayımı: 252 işlem günü.
- **Maksimum düşüş (1 yıl):** Son 1 yıllık pencerede, güne kadarki en yüksek fiyata (zirve) göre en büyük negatif sapma.
- **Calmar oranı (1 yıl):** 1 yıllık dönem getirisi / |1 yıllık maksimum düşüş|. Risksiz getiriye ihtiyaç duymadığı için hesaplanabilmiştir.
- **Sharpe / Sortino oranı: HESAPLANAMADI.** Gerekçe: Güvenilir, uzun ve tutarlı bir TL risksiz getiri (gösterge tahvil/TLREF) zaman serisi bu oturumda doğrulanabilir şekilde temin edilemedi (TLREF'i izleyen BYF'lerin fiyat geçmişi 1 yıldan kısa çıktı). Varsayımsal bir risksiz oran uydurmak yerine, talimatlar gereği bu metrik boş bırakılmış ve nedeniyle birlikte raporlanmıştır.
- **Beta / BIST endeksine korelasyon: HESAPLANAMADI** — bu oturumda endeks (ör. XU100) günlük getiri serisiyle eşleştirme yapılmadı; kapsam dışı bırakıldı.

### Eksik veri yaklaşımı

- Bir metrik hesaplanamadığında hücre **boş bırakılmış veya "hesaplanamadı"** yazılmış; ortalama ile doldurma yapılmamıştır.
- 1 yıllık risk penceresinde 30 günden az fiyat gözlemi olan fonlarda volatilite/maksimum düşüş **hesaplanmamıştır** (kısa geçmiş uyarısı).
- Fiyat/getiri verisi bulunamayan fonlar ayrı işaretlenmiştir (bu örneklemde 173 fonun tamamı için en az güncel fiyat bulunmuştur; 5 fon için 1 yıllık risk penceresi yeterli gözlem içermemiştir).

### Kategorilendirme yöntemi

- **TEFAS yatırım fonları:** Fintables'ın kendi fon kategorisi (`fon_kategorileri.baslik`) kullanılmıştır (43 kategori, bunlardan biri kategori atanmamışları temsil eden "Kategorisiz").
- **BEFAS emeklilik fonları:** Fintables kategori tablosu emeklilik fonları için yalnızca "OKS" içerdiğinden, bunun yerine fonun **şemsiye fon** alanı (Standart Fon, Katkı Fonu, Değişken Fon, Hisse Senedi Fonu, Başlangıç Fonu vb., 29 farklı değer) kategori olarak kullanılmıştır.

### Puanlama sistemi

Bu raporda **tek bir "en iyi fon" puanı/sıralaması üretilmemiştir**, çünkü (a) kullanıcının risk profili ve amacı bilinmediğinden Bölüm 6'daki ağırlıklandırılmış puanlama modeli anlamlı şekilde çalıştırılamaz, (b) maliyet ve likidite verisi tüm evren için tam değildir. Bunun yerine kategori içi karşılaştırma, risk‑getiri konumlandırması ve model portföy çerçeveleri sunulmuştur (Bölüm 5–8). Kullanıcı profili alındığında (Bölüm 11), Bölüm 6'daki puanlama modeli bu fonlara uygulanabilir.

### Kısıtlar (özet liste)

1. Derin performans/risk analizi ~2.783 fonun tamamında değil, **kategori başına en büyük 3 fon** (173 fon) üzerinde yapılmıştır — kapsam, oturumun sorgu/çıktı boyutu sınırları nedeniyle bilinçli olarak daraltılmıştır. Tüm evrenin kimlik/büyüklük/maliyet bilgisi ise CSV tablolarında eksiksiz sunulmuştur.
2. Sharpe, Sortino, beta ve korelasyon hesaplanamamıştır (gerekçe yukarıda).
3. "tefasa_acik" alanının tam anlamı resmi kaynaktan doğrulanmamıştır.
4. Giriş/çıkış komisyonu ve fon toplam gider oranı (TER) ayrı bir alan olarak Fintables veri setinde bulunamamıştır; sadece **yıllık yönetim ücreti** ve **stopaj** alanları mevcuttur.
5. Vergi/stopaj bilgisi genel oran olarak verilmiştir; yatırımcının kişisel vergi durumu dikkate alınmamıştır.
6. Kategori medyan/ortalama getiri ve volatilite rakamları, kategorideki **tüm fonlar değil, en büyük 3 fonun örneklemidir**; küçük fonların performansı farklı olabilir.

---

## 3. TEFAS Genel Görünüm

**Tablo 3 — TEFAS Kategori Karşılaştırma Tablosu** (veri tarihi: 16–21 Eylül 2026; işleme açık `tefasa_acik=true` mutual fonlar, n=1.057; tam tablo: `data/tefas_kategori_ozet.csv`)

| Kategori | Fon sayısı | Toplam büyüklük (TL) | Ortalama büyüklük (TL) |
|---|---:|---:|---:|
| Döviz Fon | 98 | 1.968.274.535.546 | 20.084.434.036 |
| Para Piyasası | 73 | 751.614.654.912 | 10.295.816.100 |
| Kategorisiz | 295 | 494.437.426.296 | 1.675.923.479 |
| Serbest Para Piyasası Fonları | 26 | 450.981.586.667 | 17.345.445.641 |
| Altın Fonları | 46 | 312.022.818.625 | 6.783.104.752 |
| Serbest Katılım Fonları | 40 | 264.999.503.179 | 6.624.987.579 |
| Yerli Hisse | 174 | 142.690.566.162 | 820.061.874 |
| Kısa Vadeli | 21 | 84.057.207.882 | 4.002.724.185 |
| Tematik Hisse | 74 | 80.364.485.055 | 1.086.006.555 |
| Kira Sertifikaları | 18 | 74.560.577.077 | 4.142.254.282 |
| Gümüş Fonları | 12 | 68.003.261.934 | 5.666.938.494 |
| Teknoloji | 61 | 36.836.498.250 | 603.876.201 |
| Yabancı Fonlar | 14 | 22.154.669.340 | 1.582.476.381 |
| *(diğer 12 küçük kategori)* | 90 | ~24.900.000.000 | — |
| **TOPLAM** | **1.057** | **~4.836.277.490.806** | — |

**Tablo 5 (kısmi) — TEFAS Risk‑Getiri Örneklemi** (kategori başına en büyük 3 fon, 1 yıllık dönem getirisi ve yıllıklandırılmış volatilite; veri tarihi 20 Eylül 2026; tam tablo: `data/kategori_getiri_risk_ornek_ozet.csv`)

| Kategori | Medyan 1 yıl getiri (%) | Ort. yıllık volatilite (%) | Ort. maks. düşüş 1 yıl (%) |
|---|---:|---:|---:|
| Gümüş Fonları | 71,39 | 54,87 | −49,08 |
| Emtia Fonları | 56,70 | 16,07 | −12,76 |
| Kısa Vadeli | 51,00 | 1,60 | 0,00 |
| Teknoloji | 49,35 | 25,75 | −14,64 |
| Serbest Para Piyasası Fonları | 47,87 | 1,49 | 0,00 |
| Borçlanma Araçları – Özel Sektör | 46,53 | 1,47 | −0,02 |
| Kategorisiz* | 46,52 | 8,14 | −1,41 |
| Para Piyasası | 46,21 | 1,54 | 0,00 |
| Mutlak Getiri Hedefli | 43,71 | 6,56 | −3,06 |
| Kira Sertifikaları | 42,99 | 1,36 | 0,00 |
| Sürdürülebilirlik | 37,85 | 19,38 | −10,91 |
| Altın Fonları | 36,33 | 26,56 | −23,62 |
| Yerli Hisse | 33,67 | 29,86 | −27,81 |
| Tematik Hisse | 32,39 | 24,88 | −15,93 |
| Döviz Fon | 22,21 | 1,29 | −0,14 |
| Kar Payı Ödeyen Fonlar | 15,27 | 11,19 | −12,48 |
| Tematik | 7,25 | 20,89 | −14,06 |

\* "Kategorisiz" medyanı TLY (%640,61 — aykırı değer, bkz. Bölüm 1) hariç tutulduğunda yaklaşık %35–40 seviyesindedir; TLY dahil edilmemiştir çünkü büyük olasılıkla veri anomalisidir.

**En iyi/en kötü performans gösterenler (örneklem içinde, 1 yıl):** En yüksek: IOG (%73,68, Yabancı Fon Sepeti), GTZ (%71,39, Gümüş), GMF (%70,83, Fon Sepeti) — hepsi yüksek volatiliteyle (%43–56) birlikte. En düşük: TGR ve YAS gibi bazı hisse/karma fonlar %4–8 bandında kalmıştır.

**Yüksek getiri/yüksek risk fonları:** Gümüş ve kıymetli maden temalı fonlar (GTZ, FMG, IOG, TTA, YKT) hem en yüksek getiriye hem en yüksek volatiliteye (%50+) ve en derin düşüşe (%−44 ile −50) sahiptir — tipik "yüksek getiri = yüksek risk" örüntüsü.

**Dengeli risk‑getiri fonları:** NSH, LPH, BHI, FEA gibi "serbest istatistiksel arbitraj" ve "mutlak getiri hedefli" fonlar, düşük volatilite (%2–4) ile %40+ getiri sunarak örneklemde en yüksek Calmar oranlarına sahiptir (bkz. Tablo 7).

---

## 4. BEFAS Genel Görünüm

BEFAS/emeklilik fonları, Fintables verisinde iki gruba ayrılmıştır (Bölüm 1'deki uyarıyla birlikte okunmalıdır):

**Tablo 4a — BEFAS "işleme açık" (tefasa_acik=true) Kategori Özeti** (n=311; tam tablo: `data/befas_islem_goren_kategori_ozet.csv`)

| Kategori (şemsiye fon) | Fon sayısı | Toplam büyüklük (TL) |
|---|---:|---:|
| Altın Katılım Fonu | 9 | 695.226.220.246 |
| Altın Fonu | 7 | 275.373.207.898 |
| Hisse Senedi Fonu | 34 | 189.358.053.746 |
| Değişken Fon | 112 | 188.231.409.940 |
| Fon Sepeti Fonu | 23 | 81.776.330.016 |
| OKS Katılım Standart Fon | 12 | 63.797.953.869 |
| Kamu Yabancı Para Borç. Araç. | 10 | 50.236.619.217 |
| Karma Fon | 9 | 48.375.143.704 |
| Borçlanma Araçları Fonu | 13 | 40.564.051.232 |
| *(diğer 14 küçük kategori)* | 82 | ~150.000.000.000 |
| **TOPLAM** | **311** | **~1.871.570.199.113** |

**Tablo 4b — BEFAS "klasik" (tefasa_acik=false) Kategori Özeti** (n=116, çoğu tanınmış BES şirketlerinin ana fonları; tam tablo: `data/befas_klasik_kategori_ozet.csv`)

| Kategori (şemsiye fon) | Fon sayısı | Toplam büyüklük (TL) |
|---|---:|---:|
| Para Piyasası Fonu | 14 | 397.976.491.829 |
| Devlet Katkısı Fonu | 12 | 253.967.801.388 |
| Belirtilmemiş | 13 | 76.479.228.206 |
| Katılım Katkı Fonu | 12 | 42.422.552.093 |
| Değişken Fon | 23 | 27.741.830.578 |
| Hisse Senedi Fonu | 4 | 9.173.737.441 |
| Başlangıç Katılım Fonu | 12 | 9.046.837.683 |
| Başlangıç Fonu | 10 | 7.786.384.521 |
| *(diğer 4 küçük kategori)* | 16 | ~10.000.000.000 |
| **TOPLAM** | **116** | **~835.435.152.195** |

**Risk‑getiri (örneklem, 1 yıl):** BEFAS_klasik grubunda para piyasası ve başlangıç fonları medyan %46–48 getiri ile düşük volatilite (%1,5–2) sunarken, BEFAS_islem_goren grubunda Fon Sepeti ve Katılım Fonu kategorileri %40+ getiri ile birlikte %33–35 volatilite taşımaktadır.

**BEFAS işlem durumu ve uyarılar:**

- BES fonlarında **devlet katkısı ve sözleşme koşulları fon performansından ayrı değerlendirilmelidir** — devlet katkısı bir yatırım getirisi değil, mevzuat gereği sağlanan ek bir kamu katkısıdır ve burada raporlanan getiri rakamlarına dahil değildir.
- BEFAS sözleşmesi, fon değiştirme sıklığı sınırı, kesinti (yönetim gider kesintisi, giriş kesintisi vb.) ve likidite/nakde dönüş koşulları bu oturumda ayrı bir "sözleşme koşulları" veri seti bulunmadığından **hesaplanamadı**; kullanıcı kendi BES sözleşmesindeki güncel şartları emeklilik şirketinden teyit etmelidir.

---

## 5. Fon Karşılaştırma Tabloları

Aşağıda, kategori başına en büyük 3 fon üzerinden oluşturulan **örnek karşılaştırma tablosu**nun bir kesiti verilmiştir (tam tablo: `data/one_cikan_fonlar_performans_risk.csv`, 173 satır, tüm sütunlarla). Valör, yönetim ücreti ve stopaj bilgileri `data/tefas_islem_goren_master.csv` ve `data/befas_islem_goren_master.csv` dosyalarından eşleştirilebilir (fon kodu anahtar alandır).

**Örnek — Yerli Hisse (TEFAS) kategorisi, en büyük 3 fon** (büyüklüğe göre; veri tarihi 20 Eylül 2026)

| Fon kodu | Fon adı (kısaltılmış) | Fon büyüklüğü (TL) | 1 yıl getiri (%) | YTD getiri (%) | Yıllık volatilite (%) | Maks. düşüş 1 yıl (%) | Calmar | Yön. ücreti (%) | Stopaj (%) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| THF | Tera Portföy Hisse Senedi (TL) Fonu | 40.452.359.335 | 38,39 | 15,62 | 33,04 | −35,06 | 1,09 | 2,25 | 0 |
| DOH | Tera Portföy Dördüncü Hisse Senedi Serbest (TL) Fon | 11.630.369.358 | 24,30 | 0,98 | 35,37 | −36,27 | 0,67 | 3,25 | 0 |
| AK3 | Ak Portföy Hisse Senedi (TL) Fonu | 8.022.980.633 | 33,67 | 28,22 | 21,16 | −12,10 | 2,78 | 3,40 | 0 |

Bu üç fon da benzer kategoriye (yerli hisse yoğun) rağmen belirgin şekilde farklı risk profilleri taşımaktadır: AK3, THF ve DOH'a göre daha düşük volatilite (%21 vs %33–35), daha düşük maksimum düşüş (−%12 vs −%35–36) ve daha iyi bir Calmar oranı (2,78) ile öne çıkmaktadır — üstelik en yüksek yönetim ücretine (%3,40) sahip olmasına rağmen. Bu, "aynı kategori" etiketinin ve "en düşük ücret" kıstasının tek başına yeterli bir karşılaştırma ölçütü olmadığını göstermektedir.

Kullanıcı belirli bir kategori için tam kırılım isterse (ör. sadece "Altın Fonları" veya sadece "Katılım Katkı Fonu"), bu, ilgili CSV dosyasından fon kodu bazında filtrelenebilir; talep edilirse ek sorgu ile derinleştirilebilir.

---

## 6. Risk‑Getiri Analizi

**Tablo 5 — TEFAS+BEFAS Risk‑Getiri Sıralaması (örneklem, Calmar oranına göre, en iyi 15)**

| Fon kodu | Grup | Kategori | 1 yıl getiri (%) | Volatilite (%) | Maks. düşüş (%) | Calmar |
|---|---|---|---:|---:|---:|---:|
| GEL | BEFAS_klasik | Para Piyasası Fonu | 47,34 | 1,50 | −0,11 | 437,84 |
| PAL | TEFAS | Döviz Fon | 22,20 | 1,31 | −0,13 | 172,34 |
| GRO | TEFAS | Döviz Fon | 22,21 | 1,28 | −0,14 | 160,40 |
| ONS | TEFAS | Döviz Fon | 22,27 | 1,28 | −0,14 | 158,75 |
| NSH | TEFAS | Serbest İstatistiksel Arbitraj | 45,25 | 2,76 | −0,30 | 148,93 |
| FEA | BEFAS_islem_goren | Özel Sektör Borç. Araç. | 42,27 | 1,70 | −0,29 | 147,63 |
| LPH | TEFAS | Serbest İstatistiksel Arbitraj | 64,51 | 3,55 | −0,46 | 139,73 |
| BHI | TEFAS | Mutlak Getiri Hedefli | 43,71 | 2,53 | −0,48 | 91,89 |
| VES | BEFAS_islem_goren | Borçlanma Araçları Fonu | 40,54 | 2,36 | −0,57 | 71,61 |
| ZHD | BEFAS_islem_goren | Kira Sertifikası Katılım | 19,48 | 1,81 | −0,54 | 35,91 |
| GKB | BEFAS_islem_goren | Kira Sertifikası Katılım | 32,98 | 2,58 | −0,97 | 33,98 |
| TJY | BEFAS_islem_goren | Yaşam Döngüsü/Hedef | 39,21 | 3,61 | −1,22 | 32,08 |
| AH8 | BEFAS_islem_goren | Karma Fon | 35,08 | 3,76 | −1,11 | 31,67 |
| VKE | BEFAS_klasik | Başlangıç Katılım Fonu | 48,95 | 2,81 | −1,90 | 25,71 |

*(TLY, veri anomalisi şüphesi nedeniyle bu sıralamadan hariç tutulmuştur.)*

**Aykırı fonlar / dikkat gerektirenler:**

- **TLY** — %640 getiri, aykırı değer şüphesi (Bölüm 1).
- **GTZ, FMG, IOG (gümüş/kıymetli maden temalı)** — %70'e yaklaşan getiri, ama %53–56 volatilite ve %48–50 maksimum düşüş; yüksek getiri yüksek riskten bağımsız değerlendirilmemelidir.
- **Kısa geçmişli fonlar** (AVH, AVY, KLV, KMP, TNE, EMY — 1 yıllık pencerede 90 gözlemden az) — volatilite/maks. düşüş rakamları güvenilir kabul edilmemelidir, performans istikrarı puanı sınırlı olmalıdır.

**Kategori medyanına göre konum:** Her kategori için medyan 1 yıllık getiri `data/kategori_getiri_risk_ornek_ozet.csv` dosyasında yer almaktadır; bir fonun kendi kategorisine göre üstte/altta kalıp kalmadığı bu dosyadan karşılaştırılabilir.

---

## 7. Fon Sepeti Analizi

Bu oturumda 173 fonun tamamı için ikili korelasyon matrisi **hesaplanmamıştır** (n×n = ~15.000 çift, kapsam dışı bırakılmıştır). Bunun yerine **varlık sınıfı dağılımı üzerinden niteliksel bir çeşitlendirme değerlendirmesi** yapılmıştır (veri kaynağı: `data/portfoy_dagilim_ornek.csv`, güncel varlık sınıfı dağılımı, %5 üstü kalemler):

- **Aşırı benzer fon grupları (aynı varlık sınıfında yoğunlaşan):** Altın/kıymetli maden temalı fonlar (TTA, YKT, KGC, KML, KJM, KZL, EMY, GEV, BGL, GGJ, VGD, VGA, OJK, AMZ, NHA) portföylerinin %60–100'ünü kıymetli madenlere ayırmıştır — bu fonlardan birden fazlasını aynı sepette tutmak çeşitlendirme sağlamaz, kıymetli maden riskini tekrarlar.
- Benzer şekilde, yabancı hisse senedine yoğunlaşan fonlar (AFA, AFT, YAY, OJT, TGR, IJC, IKL, IKP, GZH, GZL, GZY, TNE, TMG) birbirine yüksek ölçüde ikame niteliğindedir.
- **Çeşitlendirme sağlayabilecek fon örnekleri:** Devlet tahvili ağırlıklı fonlar (AE2, AK2, AG1, AZK, GUV — %75–95 devlet tahvili) ile hisse/döviz/altın ağırlıklı fonların bir araya getirilmesi, tek bir varlık sınıfına yoğunlaşmadan daha dengeli bir dağılım sunar.
- **Portföydeki toplam hassasiyet tahmini** (yalnızca bu 173 fonluk örneklem için, veri kapsamıyla sınırlı): örneklemdeki fonların ağırlıklı ortalamasına bakıldığında hisse senedi (yerli+yabancı) ağırlığı fonların önemli bir kısmında %60'ın üzerindedir; kıymetli maden ağırlığı özellikle "Altın/Gümüş/Kıymetli Maden" kategorilerinde %85–100 bandındadır. Bu tahminler **sadece örneklemdeki 173 fon için geçerlidir**, tüm TEFAS/BEFAS evrenine genellenemez.

---

## 8. Model Portföy Çerçeveleri (Yatırım Tavsiyesi Değildir)

Kullanıcı profili alınmadığı için burada verilen ağırlıklar **yalnızca örnektir** ve kişiye özel değildir.

### Düşük riskli örnek profil
- **Amaç:** Sermaye koruma, düşük dalgalanma, yüksek likidite.
- **İncelenecek fon grupları:** Para piyasası fonları (TEFAS: TP2, KLU, DLY, KSA — volatilite ~%1,3–1,6), kısa vadeli borçlanma fonları (KSV, KVS, PKV), düşük riskli katılım/emeklilik fonları (BEFAS_klasik: GEL, GDV, VKE — volatilite ~%1,4–2,8).
- **Beklenen risk:** Yıllıklandırılmış volatilite yaklaşık %1–3; maksimum düşüş genelde %0'a yakın (örneklemde gözlenen).
- **Ana riskler:** Enflasyona karşı reel getiri kaybı riski, TL değer kaybı riski (döviz pozisyonu yoksa).
- **Kime uygun olabilir:** Kısa vadeli (0–1 yıl), likidite ihtiyacı yüksek, geçici kayba tahammülü düşük yatırımcı.
- **Kime uygun olmayabilir:** Uzun vadeli reel getiri hedefleyen, enflasyonun üzerinde büyüme isteyen yatırımcı.

### Dengeli örnek profil
- **Amaç:** Enflasyonu aşma, orta düzey büyüme, risklerin varlık sınıflarına yayılması.
- **İncelenecek fon grupları:** Borçlanma araçları fonları (devlet tahvili ağırlıklı: AE2, AG1, AK2), değişken fonlar (BEFAS Değişken Fon kategorisi), altın (ölçülü ağırlıkla), hisse/yabancı varlık ağırlığı sınırlı fonlar (Fon Sepeti Fonu kategorisi — GMF, GBZ, GZE gibi çeşitlendirilmiş sepetler).
- **Beklenen risk:** Yıllıklandırılmış volatilite yaklaşık %8–20 bandı (örneklemdeki "Kategorisiz", "Sürdürülebilirlik", "Fon Sepeti" kategorileri referans alınmıştır).
- **Ana riskler:** Piyasa dalgalanmasına orta düzey duyarlılık, kategori içi fon seçimine bağlı getiri farkı.
- **Kime uygun olabilir:** Orta vadeli (1–5 yıl), orta düzey geçici kayıpları tolere edebilen yatırımcı.
- **Kime uygun olmayabilir:** Kısa vadede paraya ihtiyaç duyabilecek veya hiçbir dalgalanma istemeyen yatırımcı.

### Yüksek riskli örnek profil
- **Amaç:** Uzun vadeli büyüme, yüksek geçici kayıpları taşıyabilme.
- **İncelenecek fon grupları:** Yerli hisse fonları (Yerli Hisse kategorisi, volatilite ~%30), yabancı hisse fonları (Yabancı Fonlar, Teknoloji kategorileri, volatilite ~%16–26), altın/gümüş fonları (volatilite ~%25–56), yüksek hisse oranlı değişken fonlar, uzun vadeli BES hisse senedi grup fonları (AEB, AEH, AEU, AH5 — hisse ağırlığı %83–92).
- **Beklenen risk:** Yıllıklandırılmış volatilite %25'in üzerinde, maksimum düşüş dönemsel olarak %25–50 seviyesine ulaşabilir (gümüş/kıymetli maden fonlarında gözlenmiştir).
- **Ana riskler:** Yüksek kısa vadeli kayıp riski, tek varlık sınıfına (ör. kıymetli maden) yoğunlaşma riski, toparlanma süresinin uzun olabilmesi.
- **Kime uygun olabilir:** Uzun vadeli (5+ yıl), yüksek geçici kayba dayanıklı, likidite ihtiyacı olmayan yatırımcı.
- **Kime uygun olmayabilir:** Kısa/orta vadeli hedefi olan, düşük risk toleranslı veya emekliliğe yakın yatırımcı.

### TEFAS model sepeti / BEFAS model sepeti

Kullanıcı TEFAS mı, BEFAS mı, yoksa ikisini birlikte mi kullanacağını belirtmediği için, bu iki sepet ayrı ayrı değil, yukarıdaki üç risk profili çerçevesinde **hem TEFAS hem BEFAS fonlarından örnekler verilerek** birlikte sunulmuştur. Kullanıcı tercihini bildirdiğinde (Bölüm 11, soru 4), sepetler TEFAS‑only veya BEFAS‑only olarak yeniden daraltılabilir.

**Bu bölümdeki tüm oranlar "model portföy" örneğidir ve yatırım tavsiyesi değildir.**

---

## 9. İzleme ve Değişiklik Kuralları

Fon değişimi yalnızca kısa vadeli fiyat düşüşüne bağlanmamalıdır. Aşağıdaki durumlarda **yeniden inceleme** önerilir:

1. Fonun yatırım stratejisi veya şemsiye fon tipi değişirse.
2. Yönetim ücreti veya (varsa) toplam gider oranı önemli ölçüde artarsa (örn. mevcut fon çeşitleri arasında %0,5 puan üzeri sapma görülürse — bkz. `data/tefas_islem_goren_master.csv` yönetim ücreti sütunu).
3. Güncel varlık sınıfı dağılımı (`data/portfoy_dagilim_ornek.csv`), hedeflenen yapıdan (ör. kategori adının ima ettiği yapıdan) belirgin şekilde uzaklaşırsa.
4. Fon, kendi kategori medyanına göre birbirini izleyen dönemlerde sürekli zayıf kalırsa.
5. Maksimum düşüş ve toparlanma süresi, kategoriye göre aşırı bozulursa (ör. kategori ortalamasının 1,5 katından fazla düşüş).
6. Fon büyüklüğü veya yatırımcı sayısı ciddi biçimde azalırsa (likidite/operasyonel süreklilik riski).
7. Veri veya operasyon kalitesinde sorun oluşursa (ör. TLY'de gözlenen türden fiyat anomalisi tekrarlanırsa).
8. Yatırımcının amacı, vadesi veya risk toleransı değişirse.

---

## 10. Sonuç ve Uyarılar

- Bu raporda hiçbir fon için **"en iyi fon"** ifadesi kullanılmamıştır. Bunun yerine "bu fon şu profile ve şu role daha uygun görünüyor" biçiminde konumlandırmalar yapılmıştır (Bölüm 8).
- **Geçmiş performans gelecekteki getiriyi garanti etmez.** Bu raporda kullanılan tüm getiri rakamları geçmişe dönüktür.
- **En düşük risk değeri (ör. Kısa Vadeli/Para Piyasası fonları) risksizlik anlamına gelmez** — enflasyon, likidite ve karşı taraf riskleri geçerliliğini korur.
- Yatırım öncesinde fonların **güncel yatırımcı bilgi formu, izahname, valör, gider oranı ve vergi (stopaj) bilgileri** ilgili portföy yönetim şirketi/emeklilik şirketi veya TEFAS/BEFAS resmi kaynaklarından ayrıca teyit edilmelidir.
- Bu raporda kullanılan veriler **kısmen gecikmeli ve kısmen eksiktir** (bkz. Bölüm 2 – Kısıtlar): Sharpe/Sortino/beta hesaplanamamış, derin risk analizi tüm evren yerine 173 fonluk bir örneklemle sınırlı tutulmuş, "tefasa_acik" alanının anlamı resmi kaynakla doğrulanmamıştır. Karar verirken bu sınırlamalar göz önünde bulundurulmalıdır.

---

## Ekler — Üretilen Tablolar ve Veri Dosyaları

Aşağıdaki dosyalar `fon_analizi/data/` klasöründedir (hepsi CSV, UTF‑8, veri tarihi dosya içinde belirtilmiştir):

1. `tefas_islem_goren_master.csv` — **Tablo 1:** TEFAS işleme açık mutual fonlar ana veri tablosu (1.057 fon; kod, unvan, risk seviyesi, yönetim ücreti, stopaj, valör, PYŞ, kategori, büyüklük, yatırımcı sayısı, nakit akışı).
2. `befas_islem_goren_master.csv` + `befas_diger_emeklilik_master.csv` — **Tablo 2:** BEFAS/emeklilik fonları ana veri tablosu (311 + 116 = 427 fon, iki alt grup ayrı ayrı).
3. `tefas_kategori_ozet.csv` — **Tablo 3:** TEFAS kategori karşılaştırma tablosu.
4. `befas_islem_goren_kategori_ozet.csv`, `befas_klasik_kategori_ozet.csv` — **Tablo 4:** BEFAS kategori karşılaştırma tablosu.
5. `one_cikan_fonlar_performans_risk.csv` — **Tablo 5/6/7/9:** 173 fonluk örneklemde dönemsel getiriler (1 ay/3 ay/6 ay/YTD/1 yıl/3 yıl/5 yıl), yıllıklandırılmış volatilite, 1 yıllık maksimum düşüş, Calmar oranı — risk‑getiri sıralaması, en yüksek getirili/yüksek riskli fonlar ve (Sharpe hesaplanamadığından) Calmar bazlı "en iyi risk‑ayarlı" liste bu dosyadan türetilir.
6. `kategori_getiri_risk_ornek_ozet.csv` — Kategori bazında medyan/ortalama getiri ve risk özeti (örneklem).
7. `portfoy_dagilim_ornek.csv`  *(bkz. not)* — **Tablo 13 girdisi:** 173 fonun güncel varlık sınıfı dağılımı (%5 üstü kalemler).

> Not: Maliyet/likidite karşılaştırması (Tablo 10) ve fon büyüklüğü/nakit akışı tablosu (Tablo 11), Tablo 1–2 dosyalarındaki yönetim ücreti, stopaj, valör, büyüklük ve nakit akışı sütunlarından doğrudan türetilebilir; ayrı bir dosya olarak tekrar üretilmemiştir. Veri kalitesi ve eksik alanlar tablosu (Tablo 12) bu raporun Bölüm 2 – Kısıtlar bölümünde metinsel olarak sunulmuştur. Model portföy çerçeveleri (Tablo 13) ve izleme tablosu (Tablo 14) Bölüm 8 ve 9'da metin olarak verilmiştir.

---

## 11. Devam İçin Gerekli Bilgiler

Kişiselleştirilmiş bir fon sıralaması veya oran önerisi verebilmek için lütfen aşağıdaki soruları yanıtlayın:

1. Yatırım vadeniz nedir?
2. Geçici olarak yüzde kaç kaybı tolere edebilirsiniz?
3. Aylık yatırım tutarınız nedir?
4. TEFAS mı, BEFAS mı, ikisi birlikte mi kullanılacak?
5. Faizli veya faizsiz (katılım) fon şartınız var mı?
6. Mevcut hisse, altın, döviz ve kripto ağırlığınız nedir?
7. Paraya erişim ihtiyacınız ne kadar hızlı (likidite ihtiyacı)?
8. Portföyü ne sıklıkla takip edeceksiniz?
9. Tek fon mu, yoksa çeşitlendirilmiş bir sepet mi istiyorsunuz?

Bu bilgiler alınmadan kişiselleştirilmiş nihai fon sıralaması oluşturulmayacaktır.
