#!/usr/bin/env python3
"""
Teste rápido do sistema de controle por salas
"""

from csv_manager import list_salas_summary
from sala_config import get_available_salas, get_sala_config

def test_sistema():
    """Teste básico do sistema."""
    print("🧪 TESTE RÁPIDO DO SISTEMA DE CONTROLE POR SALAS")
    print("="*50)
    
    # 1. Teste de carregamento do CSV
    print("\n1️⃣ Testando carregamento do CSV...")
    salas = list_salas_summary()
    if salas:
        print(f"✅ CSV carregado com {len(salas)} salas:")
        for sala, count in salas.items():
            print(f"   🏫 {sala}: {count} computadores")
    else:
        print("❌ Erro no carregamento do CSV")
        return
    
    # 2. Teste de configurações
    print("\n2️⃣ Testando configurações das salas...")
    salas_config = get_available_salas()
    print(f"⚙️  Salas configuradas: {len(salas_config)}")
    
    for sala in salas_config:
        config = get_sala_config(sala)
        print(f"   🔧 {sala}: {config['os']} - {config['username']}@port{config['ssh_port']}")
    
    # 3. Teste com uma sala (se existir)
    if salas:
        test_sala = list(salas.keys())[0]
        print(f"\n3️⃣ Testando funcionalidades com sala '{test_sala}'...")
        
        # Teste de configuração
        config = get_sala_config(test_sala)
        if config:
            print(f"✅ Configuração encontrada: {config['os']}")
        else:
            print(f"⚠️  Sala '{test_sala}' não tem configuração definida")
        
        # Exemplo de Wake-on-LAN (apenas mostra o que faria)
        print(f"📡 Exemplo: wake_computers_by_sala('{test_sala}')")
        
        # Exemplo de conectividade (apenas mostra o que faria)
        print(f"🔍 Exemplo: test_ssh_connection_by_sala('{test_sala}')")
    
    print("\n✅ Teste concluído! Sistema parece estar funcionando.")
    print("\n💡 Para usar o sistema completo, execute: python main.py")

if __name__ == "__main__":
    test_sistema()