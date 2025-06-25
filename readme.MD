# PokeBrothers

PokeBrothers é um sistema de gerenciamento de coleções de cartas Pokémon, permitindo que colecionadores cadastrem, gerenciem inventário, listas de desejos e simulem trocas de cartas. O sistema utiliza interface gráfica com CustomTkinter e integra APIs externas para busca de cartas e cotação do dólar.

## Estrutura de Pastas

```
PokeBrothers/
├── colecionadores.db           # Banco de dados dos colecionadores
├── inventario.db               # Banco de dados do inventário e lista de desejos
├── main.py                     # Arquivo principal, inicializa a aplicação
├── requirements.txt            # Dependências do projeto
├── readme.MD                   # Este arquivo
├── models/                     # Modelos de domínio (MVC)
│   ├── Carta.py                # Modelo de carta Pokémon
│   ├── Colecionador.py         # Modelo de colecionador
│   ├── ItemInventario.py       # Item do inventário
│   ├── ItemListadeDesejos.py   # Item da lista de desejos
│   ├── ItemTroca.py            # Item de troca
│   └── Simulacao.py            # Simulação de trocas
├── pages/                      # Telas da interface gráfica
│   ├── Inventario.py           # Página de inventário
│   ├── lista_desejos.py        # Página de lista de desejos
│   ├── local_search_cards.py   # Busca local de cartas
│   ├── login.py                # Tela de login
│   ├── navbar.py               # Barra de navegação
│   ├── profile.py              # Perfil do usuário
│   ├── register.py             # Tela de cadastro
│   ├── search_cards.py         # Busca de cartas via API
│   └── simulacao.py            # Simulação de trocas
├── services/                   # Serviços e repositórios
│   ├── dollarapi_service.py    # Serviço de cotação do dólar
│   ├── inventario_repo.py      # Repositório do inventário
│   ├── lista_desejos_repo.py   # Repositório da lista de desejos
│   └── pokeapi_service.py      # Integração com Pokémon TCG API
```

## Descrição dos Arquivos

### Arquivos Raiz
- **main.py**: Ponto de entrada da aplicação. Gerencia a navegação entre telas, inicializa bancos de dados e conecta os componentes principais.
- **requirements.txt**: Lista de dependências Python necessárias para rodar o projeto.
- **colecionadores.db / inventario.db**: Bancos SQLite para persistência dos dados dos usuários, inventário e listas de desejos.

### models/
- **Carta.py**: Define o modelo de uma carta Pokémon, com atributos como nome, tipo, raridade, coleção, preços e imagem.
- **Colecionador.py**: Modelo do usuário colecionador, com dados pessoais, inventário, lista de desejos e histórico de trocas.
- **ItemInventario.py**: Representa um item do inventário, associando uma carta e quantidade.
- **ItemListadeDesejos.py**: Item da lista de desejos, associando uma carta desejada.
- **ItemTroca.py**: Item utilizado em simulações de troca, com carta e quantidade.
- **Simulacao.py**: Gerencia o estado de uma simulação de troca, calculando equilíbrio e regras.

### pages/
- **login.py**: Tela de login do usuário, valida credenciais no banco.
- **register.py**: Tela de cadastro de novo colecionador.
- **profile.py**: Tela de perfil, permite editar nome e visualizar email.
- **Inventario.py**: Página para visualizar, adicionar e remover cartas do inventário.
- **lista_desejos.py**: Página para gerenciar a lista de desejos do colecionador.
- **search_cards.py**: Busca cartas na API Pokémon TCG e exibe resultados.
- **local_search_cards.py**: Permite busca e filtragem de cartas já cadastradas localmente.
- **simulacao.py**: Tela para simular trocas de cartas entre colecionadores, mostrando equilíbrio da troca.
- **navbar.py**: Barra de navegação entre as páginas principais.

### services/
- **dollarapi_service.py**: Serviço para obter a cotação do dólar em tempo real via AwesomeAPI.
- **pokeapi_service.py**: Integração com a Pokémon TCG API para buscar cartas, coleções, tipos e raridades.
- **inventario_repo.py**: Repositório para persistência e recuperação do inventário no banco SQLite.
- **lista_desejos_repo.py**: Repositório para persistência e recuperação da lista de desejos.

## Como Executar

1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
2. Execute o sistema:
   ```bash
   python main.py
   ```

## Observações
- É necessário acesso à internet para buscar cartas e cotação do dólar.
- O sistema utiliza CustomTkinter para uma interface moderna e responsiva.

---
