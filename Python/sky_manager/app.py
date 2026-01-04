import pandas as pd
import streamlit as st
from conversions import MM_TO_IN_TABLE, mm_to_in_table

EXCEL_PATH = "data.xlsx"
SHEET_NAME = "Planilha1"
REFRESH_SECONDS = 30

def load_data():
    df = pd.read_excel(EXCEL_PATH, sheet_name=SHEET_NAME)
    df.columns = [str(c).strip().upper() for c in df.columns]
    if "DATA" in df.columns:
        df["DATA"] = pd.to_datetime(df["DATA"], errors="coerce", dayfirst=True)
        df["DATA"] = df["DATA"].dt.normalize()
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="ignore")
    if "DIAMETRO CABECA (MM)" in df.columns:
        df["DIAMETRO CABECA (MM)"] = pd.to_numeric(df["DIAMETRO CABECA (MM)"], errors="coerce")
        df["DIAMETRO CABECA (IN)"] = df["DIAMETRO CABECA (MM)"].apply(mm_to_in_table)
    if "DIAMETRO ROSCA (MM)" in df.columns:
        df["DIAMETRO ROSCA (MM)"] = pd.to_numeric(df["DIAMETRO ROSCA (MM)"], errors="coerce")
        df["DIAMETRO ROSCA (IN)"] = df["DIAMETRO ROSCA (MM)"].apply(mm_to_in_table)
    if "COMPRIMENTO ROSCA (MM)" in df.columns:
        df["COMPRIMENTO ROSCA (MM)"] = pd.to_numeric(df["COMPRIMENTO ROSCA (MM)"], errors="coerce")
        df["COMPRIMENTO ROSCA (IN)"] = df["COMPRIMENTO ROSCA (MM)"].apply(mm_to_in_table)
    return df

def sidebar_filters(df):
    st.sidebar.header("Filtros")
    for col in df.columns:
        opts = sorted([x for x in df[col].dropna().astype(str).unique()])
        sel = st.sidebar.multiselect(f"{col}", opts)
        if sel:
            df = df[df[col].astype(str).isin(sel)]
    start_ts, end_ts = None, None
    if "DATA" in df.columns and df["DATA"].notna().any():
        df["DATA"] = pd.to_datetime(df["DATA"], errors="coerce")
        min_d = df["DATA"].min()
        max_d = df["DATA"].max()
        if pd.notnull(min_d) and pd.notnull(max_d):
            default_start = min_d.date()
            default_end = max_d.date()
            date_range = st.sidebar.date_input("", (default_start, default_end))
            if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
                start_date, end_date = date_range
            else:
                start_date = end_date = default_start
            start_ts = pd.Timestamp(start_date)
            end_ts = pd.Timestamp(end_date)
            df = df[(df["DATA"] >= start_ts) & (df["DATA"] <= end_ts)]
    if st.sidebar.button("Limpar filtros"):
        df = load_data()
        start_ts, end_ts = None, None
    return df, start_ts, end_ts

def main():
    st.set_page_config(page_title="Controle de Estoque", layout="wide")
    st.title("Controle de Estoque")
    # st.caption(f"Os dados são lidos do Excel e atualizados a cada {REFRESH_SECONDS}s")
    placeholder = st.empty()
    with placeholder.container():
        df = load_data()
        df, start, end = sidebar_filters(df)
        st.subheader("Tabela")
        cols = st.multiselect(
            "Escolha as colunas para exibir",
            list(df.columns),
            default=[c for c in df.columns if c in [
                "DATA",
                "DESCRICAO",
                "CATEGORIA / TIPO",
                # "DIAMETRO ROSCA (MM)",
                # "COMPRIMENTO ROSCA (MM)",
                "QUANTIDADE"
            ]]
        )
        df_display = df.copy()
        if "DATA" in df_display.columns:
            df_display["DATA"] = pd.to_datetime(df_display["DATA"], errors="coerce").dt.normalize()
        if "DESCRICAO" in df_display.columns:
            df_display = df_display.sort_values(by="DESCRICAO")
        st.dataframe(
            df_display[cols] if cols else df_display,
            use_container_width=True,
            height=400,
            column_config={
                "DATA": st.column_config.DateColumn("DATA", format="DD/MM/YYYY")
            },
            hide_index=True
        )
        st.subheader("Indicadores")
        kpi_cols = st.columns(3)
        total_itens = int(df["QUANTIDADE"].sum()) if "QUANTIDADE" in df.columns else len(df)
        valor_total = float(df["PRECO TOTAL"].sum()) if "PRECO TOTAL" in df.columns else 0.0
        distintos = df["DESCRICAO"].nunique() if "DESCRICAO" in df.columns else len(df.columns)
        kpi_cols[0].metric("Quantidade total", f"{total_itens:,}".replace(",", "."))
        kpi_cols[1].metric("Valor total (R$)", f"{valor_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        kpi_cols[2].metric("Itens distintos", f"{distintos}")
        st.subheader("Gráficos")
        obj_cols = df.select_dtypes(include="object").columns.tolist()
        num_cols = df.select_dtypes(include="number").columns.tolist()
        if obj_cols and num_cols:
            chart_dim = st.selectbox("Dimensão (eixo X)", obj_cols)
            metric = st.selectbox("Métrica (eixo Y)", num_cols)
            top_n = st.slider("Top N", 5, 50, 15)
            grp = df.groupby(chart_dim, dropna=False)[metric].sum().sort_values(ascending=False).head(top_n)
            st.bar_chart(grp)
        else:
            st.info("Sem colunas adequadas para gráfico após os filtros atuais.")
        st.subheader("Exportar")
        df_export = df.copy()
        if "DATA" in df_export.columns:
            df_export["DATA"] = pd.to_datetime(df_export["DATA"], errors="coerce").dt.strftime("%d/%m/%Y")
        if start is not None and end is not None:
            file_name = f"controle_de_estoque_{pd.to_datetime(start).strftime('%d-%m-%Y')}_a_{pd.to_datetime(end).strftime('%d-%m-%Y')}.csv"
        else:
            file_name = "controle_de_estoque_filtrado.csv"
        st.download_button(
            "Baixar dados filtrados (CSV)",
            df_export.to_csv(index=False).encode("utf-8"),
            file_name=file_name,
            mime="text/csv"
        )
    st.sidebar.info(f"Atualiza a cada {REFRESH_SECONDS}s.")

if __name__ == "__main__":
    main()
