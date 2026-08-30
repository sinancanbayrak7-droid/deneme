# Borsa İstanbul BIST 100 Stock Scanner

Teknik ve temel analiz verilerine dayalı Borsa İstanbul hisse senedi tarayıcısı.

## 📋 Proje Amacı

Borsa İstanbul'da işlem gören BIST 100 şirketleri arasından, **sağlıklı finansal göstergelere** ve **teknik analiz sinyallerine** sahip olan hisse senetlerini otomatik olarak taramak.

## 🔍 Tarama Kriterleri

### 1. Teknik Analiz (Zamanlama - Timing)
**MA 50 > MA 200 Kesişimi**
- Kısa vadeli hareketli ortalama (50 gün), uzun vadeli hareketli ortalamanın (200 gün) üzerinde
- **Anlamı**: Yukarı yönlü trend sinyali
- **Kullanım**: Giriş zamanlaması için ideal noktaları belirler

```
     ↑ Fiyat
     |
     |  MA50 (Kısa vadeli)
     |  /
     | / ← Golden Cross (Alış sinyali)
     |/
     /--- MA200 (Uzun vadeli)
    /
```

### 2. Temel Analiz (Sağlık Kontrolü - Fundamentals)

#### A. Nakit Akışı Pozitif ✅
- **Metrik**: FREE_CASH_FLOW_TTM > 0
- **Anlamı**: Şirketin operasyonlarından pozitif nakit çıkışı var
- **Neden önemli**: 
  - Temettü ödeyebilecek likiditeyi gösterir
  - Şirket işletme bazında karlı
  - Borç ödemesi yapabilecek kapasitesi var

#### B. Kârlılık Artışı (YoY Growth) 📈
- **Metrik**: NET_INCOME_TTM_YOY_GROWTH > 0
- **Anlamı**: Net kâr, bir yıl öncesine göre artmış
- **Neden önemli**:
  - Şirketin performansı iyileşiyor
  - İş büyüyor ve verimlilik artıyor
  - Pozitif momentum göstergesi

#### C. Net Gelir Pozitif 💰
- **Metrik**: NET_INCOME_TTM > 0
- **Anlamı**: Şirket kârlı
- **Neden önemli**:
  - Temel şart: Zarar eden şirketler filtreleniyor
  - Yatırım için temel ön koşul

## 📊 Ek Finansal Göstergeler

Scanner çıktısında gösterilen diğer metrikler:

| Gösterge | Açıklama | Yorum |
|----------|----------|-------|
| **P/E Oranı** | Fiyat / Kâr | Düşük = İlginç, Yüksek = Pahalı |
| **ROE (%)** | Özsermaye Getirisi | Yüksek = Verimli, Düşük = Zayıf |
| **Pazar Değeri** | Market Cap | Likidite göstergesi |
| **MA50 / MA200** | Hareketli Ortalamalar | Trend yönü |

## 🚀 Kullanım

### Kurulum

```bash
# Alt modülü indir
git submodule update --init --recursive

# Bağımlılıkları yükle
cd tradingview-screener
npm install

# TypeScript derle
npm run build
```

### Tarayıcıyı Çalıştır

```bash
# TypeScript üzerinden doğrudan çalıştır
npm run example:bist100

# Veya derlenmiş JavaScript ile
node dist/examples/bist100-scanner.js
```

### Çıktı Örneği

```
╔══════════════════════════════════════════════════════════════╗
║  Borsa İstanbul BIST 100 - Hisse Senedi Tarayıcısı          ║
║  Technical + Fundamental Analysis                           ║
╚══════════════════════════════════════════════════════════════╝

Tarama Kriterleri:
📊 Teknik Analiz:
   • MA 50 > MA 200 (Yukarı trend sinyali)

📈 Temel Analiz (BIST 100 şirketleri):
   • Nakit akışı pozitif (Sağlıklı nakit akışı)
   • Kârlılık yıllık büyümesi pozitif (Kâr artışı)
   • Net gelir pozitif (Kârlı şirketler)

✅ Sonuç: 42 şirket bulundu

[Tablo ile Sonuçlar]

📊 İstatistiksel Analiz
📊 Ortalama P/E Oranı: 12.45
📊 Ortalama ROE: 18.32%
📊 Ortalama Kâr Büyümesi: 15.68%
```

## 🛠️ Proje Yapısı

```
deneme/
├── BIST100_SCANNER.md              ← Ana dokümantasyon (bu dosya)
├── tradingview-screener/           ← Git submodule
│   ├── examples/
│   │   ├── bist100-scanner.ts      ← Borsa İstanbul tarayıcısı
│   │   ├── technical-analysis.ts
│   │   ├── value-investing.ts
│   │   └── quickstart.ts
│   ├── src/
│   │   ├── fields/
│   │   │   └── StockField.ts       ← 3,500+ finansal gösterge
│   │   ├── screeners/
│   │   │   └── StockScreener.ts    ← Tarama motoru
│   │   └── index.ts
│   └── package.json
└── .git/
```

## 📈 Çalışma Mantığı

### Adım 1: Veri Çekme
TradingView API'sinden Borsa İstanbul şirketlerinin finansal verileri alınır.

### Adım 2: Filtreleme
Aşağıdaki kriterler sırayla uygulanır:
1. ✅ Exchange = BIST (Borsa İstanbul)
2. ✅ MA50 > MA200 (Teknik trend)
3. ✅ FREE_CASH_FLOW_TTM > 0 (Nakit pozitif)
4. ✅ NET_INCOME_TTM > 0 (Kârlı)
5. ✅ NET_INCOME_YOY_GROWTH > 0 (Büyüme)
6. ✅ Market Cap > $100M (Likidite)

### Adım 3: Sıralama ve Görüntüleme
- Şirketler pazar değerine göre sıralanır
- İlk 50 şirket gösterilir
- İstatistiksel analiz yapılır
- En iyi performans gösterenler listelenir

## 🎯 Yatırım Stratejisi

### Kısaca
**"Sağlıklı ve büyüyen şirketleri, yukarı trend oluşturdukları zaman satın al"**

### Detaylı
1. **Temel Analiz**: Şirketin finansal sağlığını kontrol et
   - Nakit akışı pozitif mi?
   - Kâr büyüyor mü?
   - Verimli mi (ROE)?

2. **Teknik Analiz**: Uygun zamanı bul
   - MA50 > MA200 olduğunda = Giriş sinyali
   - Trend devam ettiği sürece tut
   - Trend kırıldığında çık

## 💡 İpuçları

- **Sadece tarama aracı**: Tarayıcı, yatırım tavsiyeleri değil, araştırma aracıdır
- **Bağlam araştır**: Seçilen şirketler hakkında ek araştırma yap
- **Çeşitlendirme**: Tüm çıktılara birden yatırım yapmayın
- **Periyodik tekrar**: Haftada bir kez çalıştır ve trendleri izle

## 🔧 Özelleştirme

### Farklı Sektöre Odaklan
```typescript
.where(StockField.SECTOR.eq('Technology'))
```

### Daha Yüksek Büyüme Kriteri
```typescript
.where(StockField.NET_INCOME_TTM_YOY_GROWTH.gt(20)) // %20+ büyüme
```

### Daha Düşük P/E Oranı
```typescript
.where(StockField.PRICE_TO_EARNINGS_RATIO_TTM.lt(10))
```

### ROE Kriteri Ekle
```typescript
.where(StockField.RETURN_ON_EQUITY_TTM.gt(15)) // %15+ ROE
```

## 📚 Referanslar

- **TradingView Screener**: https://github.com/jmargieh/tradingview-screener
- **Borsa İstanbul**: https://www.borsaistanbul.com/
- **BIST 100 Index**: https://www.borsaistanbul.com/en/indices/equity-indices/bist-100

## 📝 Notlar

- Veri kaynağı: TradingView API
- Güncelleme sıklığı: Her tarama çalıştırılışında gerçek zamanlı veri
- Tarihsel veri: TTM (Trailing Twelve Months) ölçüsü kullanılır
- API sınırlaması: TradingView'in rate limiting kurallarına tabi

## 👨‍💻 Geliştirme

### Test Çalıştır
```bash
cd tradingview-screener
npm run test
npm run test:watch
```

### Type Check
```bash
npm run type-check
```

### Dokümantasyon
```bash
npm run docs:build
```

---

**Hazırlayan**: Claude Code  
**Tarih**: Ağustos 2026  
**Dil**: TypeScript  
**Lisans**: MIT
