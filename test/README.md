
```mermaid
graph TD
    A([1. Usuário interage com o sistema]) --> B(2. Requisição enviada para API Gateway)
    B --> C{3. Autenticação/Autorização}
    C -- Válido --> D(4. API Gateway roteia para Microsserviço 'Produto')
    C -- Inválido --> E([5. Retorno de erro para o Usuário])
    D --> F{6. Verificação no Cache}
    F -- Dados em Cache (Cache Hit) --> G(7. API recupera dados do Cache)
    G --> H([8. API retorna dados para o Navegador/Aplicativo])
    F -- Dados não encontrados (Cache Miss) --> I(9. Microsserviço consulta Banco de Dados)
    I --> J(10. Microsserviço retorna dados)
    J --> K(11. Armazenamento em Cache)
    K --> L(12. API retorna dados para API Gateway)
    L --> H
    J --> N(13. Publica mensagem no RabbitMQ)
    N --> O(14. Microsserviço 'Relatórios' processa mensagem)
    O --> P(15. Microsserviço 'Relatórios' atualiza relatórios)
    P --> H

    style A fill:#5cb85c80,stroke:#4cae4c,stroke-width:2px,text-align:center,font-size:12px
    style C fill:#f0ad4e80,stroke:#eea236,stroke-width:2px,text-align:center,font-size:12px
    style E fill:#5cb85c80,stroke:#d9534f,stroke-width:2px,text-align:center,font-size:12px
    style F fill:#f0ad4e80,stroke:#eea236,stroke-width:2px,text-align:center,font-size:12px
    style H fill:#5cb85c80,stroke:#4cae4c,stroke-width:2px,text-align:center,font-size:12px
```

# Arquitetura da Solução

Interface Web: Onde o usuário interage com o sistema.
API Gateway: Ponto de entrada para todas as requisições, responsável por autenticação, autorização e roteamento.
Microsserviço “Produto”: Gerencia as operações relacionadas aos medicamentos.
Banco de Dados (SQL Server): Armazena os dados dos medicamentos.
RabbitMQ: Sistema para comunicação assíncrona entre microsserviços.
Microsserviço “Relatórios”: Atualiza e gera relatórios de estoque.

# Fluxo de Interação

Usuário interage com o sistema: Acessa o sistema via Navegador/Aplicativo.
Requisição enviada para a API: O Navegador/Aplicativo envia a requisição para a API (API Gateway).
Autenticação/Autorização: A API Gateway valida a autenticação do usuário e verifica as permissões.
Roteamento para Microsserviço ‘Produto’: A API Gateway roteia a requisição para o microsserviço “Produto”.
Verificação no Cache: A API verifica se os dados solicitados estão presentes no Cache (Redis).
Dados em Cache (Cache Hit): Se os dados estiverem no cache, a API recupera os dados do Cache e retorna para o Navegador/Aplicativo.
Dados não encontrados no Cache (Cache Miss): Se os dados não estiverem no cache, a API publica uma mensagem na fila (RabbitMQ).
Consulta ao Banco de Dados: O Microsserviço consulta o Banco de Dados (SQL Server) pelos dados.
Retorno dos dados: O Microsserviço retorna os dados para a fila (RabbitMQ).
Armazenamento em Cache: A API armazena os dados no Cache (Redis) para futuras requisições.
Retorno para o Usuário: A API retorna os dados para o Navegador/Aplicativo.
Publicação de mensagem no RabbitMQ: O Microsserviço “Produto” envia uma mensagem para o RabbitMQ informando a criação/atualização do medicamento.
Processamento de mensagem pelo Microsserviço ‘Relatórios’: O Microsserviço “Relatórios” recebe a mensagem e atualiza os relatórios de estoque.

# Verificação do Fluxograma

Interação do Usuário: Representado pelo item A.
Requisição para API Gateway: Representado pelo item B.
Autenticação/Autorização: Representado pelo item C.
Roteamento para Microsserviço ‘Produto’: Representado pelo item D.
Verificação no Cache: Representado pelo item F.
Cache Hit e Miss: Representado pelos itens G e I.
Consulta ao Banco de Dados: Representado pelo item I.
Retorno dos dados e Armazenamento em Cache: Representado pelos itens J e K.
Publicação de mensagem no RabbitMQ: Representado pelo item N.
Processamento de mensagem pelo Microsserviço ‘Relatórios’: Representado pelos itens O e P.