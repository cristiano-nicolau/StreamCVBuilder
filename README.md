# StreamCVBuilder

Um gerador automático de currículos usando Streamlit, YAML e JSON.

## 🚀 Funcionalidades

- **Interface intuitiva** - Interface web com Streamlit
- **Templates flexíveis** - Seções configuráveis via YAML
- **Dados estruturados** - Armazenamento em JSON
- **Export PDF** - Geração automática de PDFs profissionais
- **Templates múltiplos** - Diferentes estilos de currículo

## 📁 Estrutura do Projeto

```
/StreamCVBuilder
├── src/
│   ├── streamlit_app.py      # Aplicação principal
│   ├── cv_generator.py       # Lógica de geração de CV
│   ├── pdf_export.py         # Exportação para PDF
│   └── utils/
│       ├── data_manager.py   # Gestão de dados JSON
│       └── template_loader.py # Carregamento de templates
├── templates/
│   ├── sections.yaml         # Definição das seções
│   ├── cv_templates/         # Templates de CV
│   └── styles/               # CSS para templates
├── data/
│   ├── user_profiles/        # Perfis de usuário
│   └── projects/             # Projetos salvos
├── assets/
│   └── images/              # Imagens e ícones
└── docs/
    └── examples/            # Exemplos de uso
```

## 🛠️ Instalação

1. Clone o repositório:
```bash
git clone https://github.com/cristiano-nicolau/StreamCVBuilder.git
cd StreamCVBuilder
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute a aplicação:
```bash
streamlit run src/streamlit_app.py
```

## 📖 Como Usar

1. **Configurar Perfil** - Adicione suas informações pessoais
2. **Escolher Seções** - Selecione as seções que deseja incluir
3. **Preencher Dados** - Complete as informações de cada seção
4. **Escolher Template** - Selecione o design do currículo
5. **Gerar PDF** - Exporte seu currículo profissional

## 🎨 Templates Disponíveis

- **Moderno** - Design clean e minimalista
- **Clássico** - Formato tradicional
- **Criativo** - Para áreas criativas
- **Técnico** - Para áreas de tecnologia

## 📄 Licença

MIT License - veja [LICENSE](LICENSE) para detalhes.