#!/usr/bin/env python3
"""
dxf-analyzer1 – Extrator de dados de desenhos técnicos DXF.
"""

import sys
from pathlib import Path

try:
    import ezdxf
except ImportError:
    print("Instale a dependência: pip install ezdxf")
    sys.exit(1)

def extrair_info_dxf(caminho_arquivo):
    """Extrai informações básicas de um arquivo DXF."""
    try:
        doc = ezdxf.readfile(caminho_arquivo)
        msp = doc.modelspace()
        entidades = list(msp)
        total = len(entidades)
        linhas = [e for e in entidades if e.dxftype() == 'LINE']
        circulos = [e for e in entidades if e.dxftype() == 'CIRCLE']
        polilinhas = [e for e in entidades if e.dxftype() in ('POLYLINE', 'LWPOLYLINE')]
        
        comprimento_total = 0.0
        for e in linhas:
            if hasattr(e.dxf, 'length'):
                comprimento_total += e.dxf.length
        for e in polilinhas:
            if hasattr(e, 'length'):
                comprimento_total += e.length
        
        print(f"\n📊 Resumo do arquivo: {caminho_arquivo}")
        print(f"Total de entidades: {total}")
        print(f"Linhas: {len(linhas)}")
        print(f"Círculos (furos): {len(circulos)}")
        print(f"Polilinhas: {len(polilinhas)}")
        print(f"Comprimento total de linhas/polilinhas: {comprimento_total:.2f} unidades")
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python src/analyzer.py caminho/arquivo.dxf")
        sys.exit(1)
    extrair_info_dxf(sys.argv[1])
