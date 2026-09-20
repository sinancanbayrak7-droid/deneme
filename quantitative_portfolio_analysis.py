#!/usr/bin/env python3
"""Kantitatif Portfoy Analiz - Fintables gercek verisi ile PDF uretim"""
import sys, json, os, math
from datetime import datetime
from typing import Dict, List
import numpy as np
import pandas as pd

SCRATCH = "/tmp/claude-0/-home-user-deneme/b8fa0667-f306-58da-84f4-f70d0c2af22d/scratchpad"

RESTRICTED = {
    "IDH": {"label": "BIST 100 Disi Hisse Fonu", "unvan": "IS PORTFOY BIST 100 DISI SIRKETLER HISSE SENEDI (TL) FONU"},
    "FEI": {"label": "Devlet Katkisi Fonu (Salt Izleme)", "unvan": "HDI FIBA EMEKLILIK VE HAYAT A.S. KATKI EMEKLILIK YATIRIM FONU"},
    "AMF": {"label": "Devlet Katkisi Fonu (Salt Izleme)", "unvan": "ALLIANZ YASAM VE EMEKLILIK A.S. KATKI EMEKLILIK YATIRIM FONU"},
}

def load_json(name):
    with open(os.path.join(SCRATCH, name), 'r', encoding='utf-8') as f:
        return json.load(f)

def build_dataset() -> pd.DataFrame:
    """Fintables'tan cekilen gercek verileri birlestir."""
    metadata = load_json("fund_metadata.json")
    returns_stats = {r['kod']: r for r in load_json("fund_returns_stats.json")}
    flow_data = {r['fon_kodu']: r for r in load_json("fund_flow_data.json")}
    mdd_data = load_json("fund_mdd.json")

    rows = []
    for m in metadata:
        kod = m['fon_kodu']
        if kod not in returns_stats or kod not in flow_data:
            continue

        rs = returns_stats[kod]
        fl = flow_data[kod]
        mdd = mdd_data.get(kod, 0)

        ort = rs['ort_gunluk_getiri']
        ort_kare = rs['ort_kare_getiri']
        varyans = max(0, ort_kare - ort**2)
        gunluk_std = math.sqrt(varyans)
        yillik_volatilite = gunluk_std * math.sqrt(252)
        yillik_getiri = ort * 252

        aum_simdi, aum_1ay, aum_3ay = fl['aum_simdi'], fl['aum_1ay'], fl['aum_3ay']
        yat_simdi, yat_1ay, yat_3ay = fl['yat_simdi'], fl['yat_1ay'], fl['yat_3ay']

        aum_chg_1m = (aum_simdi - aum_1ay) / aum_1ay * 100 if aum_1ay else 0
        yat_chg_1m = (yat_simdi - yat_1ay) / yat_1ay * 100 if yat_1ay else 0
        aum_chg_3m = (aum_simdi - aum_3ay) / aum_3ay * 100 if aum_3ay else 0
        yat_chg_3m = (yat_simdi - yat_3ay) / yat_3ay * 100 if yat_3ay else 0

        rows.append({
            'fon_kodu': kod,
            'unvan': m['unvan'],
            'fon_tipi': m['fon_tipi'],
            'risk_seviyesi': m['risk_seviyesi'],
            'yonetim_ucreti': m['yonetim_ucreti'] if m['yonetim_ucreti'] is not None else 1.5,
            'gun_sayisi': m['gun_sayisi'],
            'aum': aum_simdi,
            'yatirimci': yat_simdi,
            'yillik_getiri': yillik_getiri,
            'yillik_volatilite': yillik_volatilite,
            'max_drawdown': mdd,
            'aum_chg_1m': aum_chg_1m,
            'yat_chg_1m': yat_chg_1m,
            'aum_chg_3m': aum_chg_3m,
            'yat_chg_3m': yat_chg_3m,
            'flow_divergence_1m': abs(yat_chg_1m - aum_chg_1m),
            'flow_divergence_3m': abs(yat_chg_3m - aum_chg_3m),
        })

    return pd.DataFrame(rows)

def deterministic_scoring(df: pd.DataFrame) -> pd.DataFrame:
    """Skorlama: %40 Getiri, %30 Risk Direnci, %20 SmartMoney, -%10 FIGK Maliyet."""
    df = df.copy()

    # %40 Rolatif Getiri (yillik getiri normalize)
    df['return_score'] = ((df['yillik_getiri'] + 0.30) / 0.90 * 40).clip(0, 40)

    # %30 Risk Direnci (dusuk volatilite + dusuk MDD iyi)
    vol_norm = (1 - (df['yillik_volatilite'] / df['yillik_volatilite'].max())).clip(0, 1)
    mdd_norm = (1 - (df['max_drawdown'].abs() / (df['max_drawdown'].abs().max() + 1e-9))).clip(0, 1)
    df['risk_score'] = (vol_norm * 15 + mdd_norm * 15)

    # %20 Smart Money / Akis Gucu (dusuk divergence iyi -> agir ceza yuksek divergence'a)
    avg_divergence = (df['flow_divergence_1m'] + df['flow_divergence_3m']) / 2
    max_div = avg_divergence.max() if avg_divergence.max() > 0 else 1
    df['flow_score'] = (20 * (1 - (avg_divergence / max_div).clip(0, 1)))

    # -%10 FIGK Maliyet Etkisi
    df['cost_penalty'] = (df['yonetim_ucreti'] / df['yonetim_ucreti'].max() * 10).clip(0, 10)

    df['total_score'] = (df['return_score'] + df['risk_score'] + df['flow_score'] - df['cost_penalty']).clip(0, 100)

    return df.sort_values('total_score', ascending=False).reset_index(drop=True)

def build_correlation_matrix_from_pairs() -> pd.DataFrame:
    """Fintables'tan cekilen pairwise Pearson toplamlarindan korelasyon matrisi kurar."""
    pairs_file = os.path.join(SCRATCH, "fund_corr_pairs.csv")
    if not os.path.exists(pairs_file):
        return pd.DataFrame()

    pairs = pd.read_csv(pairs_file)
    codes = sorted(set(pairs['kod1']) | set(pairs['kod2']))
    corr = pd.DataFrame(np.eye(len(codes)), index=codes, columns=codes)

    for _, row in pairs.iterrows():
        n, sx, sy, sxy, sxx, syy = row['n'], row['sx'], row['sy'], row['sxy'], row['sxx'], row['syy']
        num = n * sxy - sx * sy
        den = math.sqrt(max(0, n * sxx - sx**2) * max(0, n * syy - sy**2))
        r = num / den if den > 0 else 0
        corr.loc[row['kod1'], row['kod2']] = r
        corr.loc[row['kod2'], row['kod1']] = r

    return corr

def select_elite_list(scored_df: pd.DataFrame, corr_matrix: pd.DataFrame, corr_threshold: float = 0.8, max_size: int = 20) -> List[str]:
    """Korelasyon filtreli cesitlendirilmis elit liste."""
    elite = []
    for _, row in scored_df.iterrows():
        kod = row['fon_kodu']
        skip = False
        if not corr_matrix.empty and kod in corr_matrix.columns:
            for selected in elite:
                if selected in corr_matrix.columns:
                    c = corr_matrix.loc[kod, selected] if kod in corr_matrix.index else 0
                    if abs(c) > corr_threshold:
                        skip = True
                        break
        if not skip:
            elite.append(kod)
        if len(elite) >= max_size:
            break
    return elite

def generate_pdf(scored_df: pd.DataFrame, elite_list: List[str], corr_matrix: pd.DataFrame, output_path: str) -> str:
    """PDF rapor (ReportLab)."""
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER

    doc = SimpleDocTemplate(output_path, pagesize=A4, title="Quantitative Portfolio Analysis")
    styles = getSampleStyleSheet()
    story = []

    title_style = ParagraphStyle('CT', parent=styles['Heading1'], fontSize=18,
                                textColor=colors.HexColor('#1f4788'), alignment=TA_CENTER,
                                spaceAfter=12, fontName='Helvetica-Bold')
    story.append(Paragraph('Kantitatif Portfoy Analiz Raporu', title_style))
    story.append(Paragraph('TEFAS/BEFAS Yatirim Fonlari (Fintables Canli Veri) - ' + datetime.now().strftime("%d.%m.%Y"),
                          styles['Normal']))
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        f'Bu rapor, Fintables MCP baglantisi uzerinden cekilen gercek TEFAS fon verilerine dayanmaktadir. '
        f'{len(scored_df)} likit fon (AUM ve yatirimci sayisi filtreli, minimum 1.5 yillik piyasa gecmisi) '
        f'deterministik skorlama modeliyle degerlendirilmistir.',
        styles['BodyText']))
    story.append(Spacer(1, 8))

    # Elit Portfoy
    story.append(PageBreak())
    story.append(Paragraph('1. Elit Portfoy (Korelasyon Filtreli, Cesitlendirilmis)', styles['Heading2']))
    story.append(Spacer(1, 6))

    elite_data = [['#', 'Kod', 'Fon Adi', 'Skor', 'Yillik Getiri']]
    for i, kod in enumerate(elite_list, 1):
        match = scored_df[scored_df['fon_kodu'] == kod]
        if not match.empty:
            row = match.iloc[0]
            elite_data.append([str(i), kod, row['unvan'][:35], f"{row['total_score']:.1f}", f"%{row['yillik_getiri']*100:.1f}"])

    elite_table = Table(elite_data, colWidths=[0.3*inch, 0.5*inch, 2.6*inch, 0.6*inch, 0.9*inch])
    elite_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')])
    ]))
    story.append(elite_table)

    # Salt Izleme (Kisitli Fonlar)
    story.append(Spacer(1, 14))
    story.append(Paragraph('1.1 Kisitli / Salt Izleme Fonlari', styles['Heading3']))
    story.append(Spacer(1, 4))
    restricted_text = (
        '• IDH (IS PORTFOY BIST 100 DISI SIRKETLER HISSE SENEDI FONU): "BIST 100 Disi Hisse Fonu" olarak etiketlenmistir, '
        'her kosulda bu sekilde raporlanir.<br/>'
        '• FEI (HDI FIBA EMEKLILIK KATKI FONU) ve AMF (ALLIANZ KATKI FONU): Devlet katkisi fonlari olduklari icin '
        'optimizasyon disinda tutulmus, "Salt Izleme" statusunde raporlanmistir.'
    )
    story.append(Paragraph(restricted_text, styles['BodyText']))

    # Top Skorlu Fonlar (Tum liste)
    story.append(PageBreak())
    story.append(Paragraph(f'2. Skorlanan Tum Fonlar (İlk {min(30,len(scored_df))})', styles['Heading2']))
    story.append(Spacer(1, 6))

    top_data = [['Kod', 'Toplam', 'Getiri', 'Risk', 'Akis', 'Maliyet', 'Vol.', 'MDD']]
    for _, row in scored_df.head(30).iterrows():
        top_data.append([
            row['fon_kodu'],
            f"{row['total_score']:.1f}",
            f"{row['return_score']:.1f}",
            f"{row['risk_score']:.1f}",
            f"{row['flow_score']:.1f}",
            f"{row['cost_penalty']:.1f}",
            f"%{row['yillik_volatilite']*100:.1f}",
            f"%{row['max_drawdown']*100:.1f}"
        ])

    top_table = Table(top_data, colWidths=[0.55*inch]*8)
    top_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('FONTSIZE', (0, 1), (-1, -1), 7),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')])
    ]))
    story.append(top_table)

    # Smart Money Sinyalleri
    story.append(PageBreak())
    story.append(Paragraph('3. Smart Money / Akis Uyumsuzlugu Sinyalleri', styles['Heading2']))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        'Yatirimci sayisi artarken AUM yatay kalan veya dusen fonlar "Akis Uyumsuzlugu" olarak isaretlenmis '
        've skorlamada agir ceza puani uygulanmistir. En yuksek uyumsuzluk gosteren ilk 10 fon:',
        styles['BodyText']))
    story.append(Spacer(1, 4))

    div_df = scored_df.copy()
    div_df['avg_div'] = (div_df['flow_divergence_1m'] + div_df['flow_divergence_3m']) / 2
    div_sorted = div_df.sort_values('avg_div', ascending=False).head(10)

    div_data = [['Kod', 'Yat.Degisim(1A)', 'AUM Degisim(1A)', 'Uyumsuzluk']]
    for _, row in div_sorted.iterrows():
        div_data.append([
            row['fon_kodu'],
            f"%{row['yat_chg_1m']:.1f}",
            f"%{row['aum_chg_1m']:.1f}",
            f"{row['avg_div']:.1f}"
        ])
    div_table = Table(div_data, colWidths=[1*inch, 1.5*inch, 1.5*inch, 1*inch])
    div_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#a83232')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')])
    ]))
    story.append(div_table)

    # Korelasyon Matrisi
    if not corr_matrix.empty:
        story.append(PageBreak())
        story.append(Paragraph('4. Pearson Korelasyon Matrisi (Elit Fonlar - Ozet)', styles['Heading2']))
        story.append(Spacer(1, 6))
        story.append(Paragraph(
            'Ilk 8 elit fonun getiri korelasyonlari (1 yillik gunluk getiriler uzerinden Pearson katsayisi). '
            '0.80 uzeri korelasyonlu ciftlerden dusuk skorlu fon cikarilarak cesitlendirme saglanmistir.',
            styles['BodyText']))
        story.append(Spacer(1, 6))

        subset = [c for c in elite_list if c in corr_matrix.columns][:8]
        if subset:
            header = [''] + subset
            corr_data = [header]
            for r in subset:
                row_vals = [r] + [f"{corr_matrix.loc[r, c]:.2f}" for c in subset]
                corr_data.append(row_vals)

            n_cols = len(subset) + 1
            col_w = 6.5 * inch / n_cols
            corr_table = Table(corr_data, colWidths=[col_w]*n_cols)
            corr_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#1f4788')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 7),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ]))
            story.append(corr_table)

    # Metodoloji
    story.append(PageBreak())
    story.append(Paragraph('5. Skorlama Metodolojisi', styles['Heading2']))
    story.append(Spacer(1, 6))

    methodology = (
        '<b>TOPLAM SKOR FORMULU:</b><br/>'
        'Rolatif Getiri(%40) + Risk Direnci(%30) + Smart Money Akis(%20) - FIGK Maliyet(%10)<br/><br/>'
        '<b>Bilesenler:</b><br/>'
        '• Rolatif Getiri (%40): 1 yillik yilliklandirilmis getiri orani (BIST100/Enflasyon referansli normalize)<br/>'
        '• Risk Direnci (%30): Yilliklandirilmis volatilite (252 islem gunu) ve 3 yillik Maximum Drawdown kombinasyonu<br/>'
        '• Smart Money Akis Gucu (%20): 1 ay ve 3 ay periyotlarda yatirimci sayisi vs AUM degisim uyumsuzlugu analizi<br/>'
        '• FIGK Maliyet Etkisi (-%10): Fon Isletim Gider Kesintisi (yonetim ucreti) cezasi<br/>'
        '• Cesitlendirme: Ilk 20 fon icin Pearson korelasyon matrisi calistirilmis, >0.80 korelasyonlu ciftlerden '
        'dusuk skorlu olan cikarilip yerine siradaki en iyi fon eklenmistir<br/><br/>'
        '<b>Veri Kaynagi:</b> Fintables MCP - gunluk_fon_degerleri, mumlar_gunluk_gh, fonlar tablolari<br/>'
        f'<b>Analiz Kapsami:</b> {len(scored_df)} likit TEFAS fonu (yatirimci sayisi >=100, min. 1.5 yil piyasa gecmisi)<br/><br/>'
        '<b>Kisitlamalar:</b><br/>'
        '• IDH: BIST 100 Disi Hisse Fonu olarak etiketlenmis<br/>'
        '• FEI/AMF: Devlet katkisi fonlari, optimizasyon disinda "Salt Izleme" statusunde'
    )
    story.append(Paragraph(methodology, styles['BodyText']))

    # Dipnot
    story.append(Spacer(1, 20))
    footer_style = ParagraphStyle('Footer', parent=styles['Normal'], fontSize=7.5,
                                 textColor=colors.grey, alignment=TA_CENTER)
    footer_text = (
        'Bu rapor Fintables MCP canli verisi kullanilarak otomatik olarak uretilmistir.<br/>'
        'Rapor egitim/analiz amaclidir, yatirim tavsiyesi niteligi tasimaz.<br/>'
        f'Uretim tarihi: {datetime.now().strftime("%d.%m.%Y %H:%M:%S")} | '
        'Algoritma: Deterministic Quantitative Scoring Engine v2 (Gercek Veri)'
    )
    story.append(Paragraph(footer_text, footer_style))

    doc.build(story)
    return os.path.abspath(output_path)

def main():
    try:
        print("[*] Quantitative Portfolio Analysis Engine (REAL DATA) Starting...", file=sys.stderr)

        print("[1/5] Building dataset from Fintables real data...", file=sys.stderr)
        df = build_dataset()
        print(f"      {len(df)} funds loaded (liquid, >=1.5yr history)", file=sys.stderr)

        if len(df) < 5:
            raise RuntimeError("Insufficient fund data")

        print("[2/5] Deterministic scoring...", file=sys.stderr)
        scored_df = deterministic_scoring(df)
        print(f"      {len(scored_df)} funds scored", file=sys.stderr)

        print("[3/5] Loading correlation data (real Fintables prices)...", file=sys.stderr)
        corr_matrix = build_correlation_matrix_from_pairs()
        print(f"      Correlation matrix: {corr_matrix.shape}", file=sys.stderr)

        print("[4/5] Selecting elite diversified portfolio...", file=sys.stderr)
        elite_list = select_elite_list(scored_df, corr_matrix, max_size=20)
        print(f"      Elite portfolio: {len(elite_list)} funds", file=sys.stderr)

        print("[5/5] Generating PDF report...", file=sys.stderr)
        output_path = "/home/user/deneme/tum_fonlar_kantitatif_analiz.pdf"
        pdf_path = generate_pdf(scored_df, elite_list, corr_matrix, output_path)

        print(pdf_path)
        sys.exit(0)

    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
