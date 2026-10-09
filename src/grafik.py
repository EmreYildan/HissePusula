
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def fiyat_grafigi_olustur(analiz, hisse_kodu):

    fig = go.Figure()

    # Kapanis fiyati
    fig.add_trace(go.Scatter(
        x=analiz.index,
        y=analiz["Close"],
        mode="lines",
        name="Kapanis"
    ))

    # 20 gunluk hareketli ortalama
    fig.add_trace(go.Scatter(
        x=analiz.index,
        y=analiz["MA20"],
        mode="lines",
        name="MA20"
    ))

    # 50 gunluk hareketli ortalama
    fig.add_trace(go.Scatter(
        x=analiz.index,
        y=analiz["MA50"],
        mode="lines",
        name="MA50"
    ))

    # Bollinger ust bant
    fig.add_trace(go.Scatter(
        x=analiz.index,
        y=analiz["BB_Ust"],
        mode="lines",
        name="Bollinger Ust"
    ))

    
    # Bollinger alt bant
    fig.add_trace(go.Scatter(
        x=analiz.index,
        y=analiz["BB_Alt"],
        mode="lines",
        name="Bollinger Alt",
        fill="tonexty",
        fillcolor="rgba(100, 149, 237, 0.12)"
    ))


    fig.update_layout(
        title=f"{hisse_kodu} - Fiyat ve Teknik Gostergeler",
        xaxis_title="Tarih",
        yaxis_title="Fiyat (TL)",
        hovermode="x unified",
        template="plotly_white"
    )

    fig.show()


    
def rsi_grafigi_olustur(analiz, hisse_kodu):

    fig = go.Figure()

    # RSI14 cizgisi
    fig.add_trace(go.Scatter(
        x=analiz.index,
        y=analiz["RSI14"],
        mode="lines",
        name="RSI14",
        line=dict(color="purple", width=2)
    ))

    # Asiri alim seviyesi
    fig.add_hline(
        y=70,
        line_dash="dash",
        line_color="red",
        annotation_text="Asiri Alim (70)"
    )

    # Asiri satim seviyesi
    fig.add_hline(
        y=30,
        line_dash="dash",
        line_color="green",
        annotation_text="Asiri Satim (30)"
    )

    fig.update_layout(
        title=f"{hisse_kodu} - RSI14 Grafigi",
        xaxis_title="Tarih",
        yaxis_title="RSI Degeri",
        yaxis=dict(range=[0, 100]),
        hovermode="x unified",
        template="plotly_white"
    )

    fig.show()


    
def macd_grafigi_olustur(analiz, hisse_kodu):

    fig = go.Figure()

    # MACD cizgisi
    fig.add_trace(go.Scatter(
        x=analiz.index,
        y=analiz["MACD"],
        mode="lines",
        name="MACD",
        line=dict(color="blue", width=2)
    ))

    # Sinyal cizgisi
    fig.add_trace(go.Scatter(
        x=analiz.index,
        y=analiz["MACD_Sinyal"],
        mode="lines",
        name="Sinyal",
        line=dict(color="orange", width=2)
    ))

    # MACD histogrami
    histogram = analiz["MACD_Histogram"]

    fig.add_trace(go.Bar(
        x=analiz.index,
        y=histogram,
        name="Histogram",
        marker_color=[
            "green" if deger >= 0 else "red"
            for deger in histogram
        ]
    ))

    # Sifir cizgisi
    fig.add_hline(
        y=0,
        line_dash="dash",
        line_color="gray"
    )

    fig.update_layout(
        title=f"{hisse_kodu} - MACD Grafigi",
        xaxis_title="Tarih",
        yaxis_title="MACD Degeri",
        hovermode="x unified",
        template="plotly_white"
    )

    # Hafta sonlarini tarih ekseninden kaldir
    fig.update_xaxes(
        rangebreaks=[
            dict(bounds=["sat", "mon"])
        ]
    )

    fig.show()




def birlesik_grafik_olustur(analiz, hisse_kodu):

    
    fig = make_subplots(
        rows=4,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        row_heights=[0.4, 0.2, 0.2, 0.2],
        subplot_titles=[
            "Fiyat ve Teknik Gostergeler",
            "RSI14",
            "MACD",
            "Islem Hacmi"
        ]
    )


    # 1. Grafik: Kapanis fiyati
    fig.add_trace(
        go.Scatter(
            x=analiz.index,
            y=analiz["Close"],
            mode="lines",
            name="Kapanis"
        ),
        row=1,
        col=1
    )

    # 2. Grafik: RSI14
    fig.add_trace(
        go.Scatter(
            x=analiz.index,
            y=analiz["RSI14"],
            mode="lines",
            name="RSI14",
            line=dict(color="purple")
        ),
        row=2,
        col=1
    )

    # RSI asiri alim seviyesi
    fig.add_hline(
        y=70,
        line_dash="dash",
        line_color="red",
        annotation_text="Asiri Alim (70)",
        row=2,
        col=1
    )

    # RSI asiri satim seviyesi
    fig.add_hline(
        y=30,
        line_dash="dash",
        line_color="green",
        annotation_text="Asiri Satim (30)",
        row=2,
        col=1
    )

    # RSI eksenini 0-100 arasinda sabitle
    fig.update_yaxes(
        range=[0, 100],
        row=2,
        col=1
    )

    # 3. Grafik: MACD
    fig.add_trace(
        go.Scatter(
            x=analiz.index,
            y=analiz["MACD"],
            mode="lines",
            name="MACD",
            line=dict(color="blue")
        ),
        row=3,
        col=1
    )
    
    # MACD sinyal cizgisi
    fig.add_trace(
        go.Scatter(
            x=analiz.index,
            y=analiz["MACD_Sinyal"],
            mode="lines",
            name="MACD Sinyal",
            line=dict(color="orange", width=2)
        ),
        row=3,
        col=1
    )

    # MACD histogrami
    histogram = analiz["MACD_Histogram"]

    fig.add_trace(
        go.Bar(
            x=analiz.index,
            y=histogram,
            name="MACD Histogram",
            marker_color=[
                "green" if deger >= 0 else "red"
                for deger in histogram
            ]
        ),
        row=3,
        col=1
    )

    # MACD sifir referans cizgisi
    fig.add_hline(
        y=0,
        line_dash="dash",
        line_color="gray",
        row=3,
        col=1
    )

    # MA20 cizgisi
    fig.add_trace(
        go.Scatter(
            x=analiz.index,
            y=analiz["MA20"],
            mode="lines",
            name="MA20",
            line=dict(color="orange")
        ),
        row=1,
        col=1
    )

    # MA50 cizgisi
    fig.add_trace(
        go.Scatter(
            x=analiz.index,
            y=analiz["MA50"],
            mode="lines",
            name="MA50",
            line=dict(color="red")
        ),
        row=1,
        col=1
    )

    # Bollinger ust bant
    fig.add_trace(
        go.Scatter(
            x=analiz.index,
            y=analiz["BB_Ust"],
            mode="lines",
            name="Bollinger Ust",
            line=dict(color="rgba(70, 130, 180, 0.6)")
        ),
        row=1,
        col=1
    )

    # Bollinger alt bant
    fig.add_trace(
        go.Scatter(
            x=analiz.index,
            y=analiz["BB_Alt"],
            mode="lines",
            name="Bollinger Alt",
            line=dict(color="rgba(70, 130, 180, 0.6)"),
            fill="tonexty",
            fillcolor="rgba(100, 149, 237, 0.12)"
        ),
        row=1,
        col=1
    )

    # 4. Grafik: Gunluk islem hacmi
    fig.add_trace(
        go.Bar(
            x=analiz.index,
            y=analiz["Volume"],
            name="Gunluk Hacim",
            marker_color="steelblue"
        ),
        row=4,
        col=1
    )

    # 20 gunluk ortalama hacim
    fig.add_trace(
        go.Scatter(
            x=analiz.index,
            y=analiz["Hacim_MA20"],
            mode="lines",
            name="Ortalama Hacim (20)",
            line=dict(color="orange", width=2)
        ),
        row=4,
        col=1
    )


    fig.update_layout(
        title=f"{hisse_kodu} - Birlesik Teknik Analiz",
        height=1100,
        hovermode="x unified",
        template="plotly_white"
    )

    # Hafta sonlarini tarih ekseninden kaldir
    fig.update_xaxes(
        rangebreaks=[
            dict(bounds=["sat", "mon"])
        ]
    )

    fig.show()
