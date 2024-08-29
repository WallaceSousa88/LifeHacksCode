
```mermaid
graph TD
    A([1. Usuário interage com o sistema]) --> B(2. Requisição enviada para a API)
    B --> C{3. Verificação no Cache}
    C -- Dados em Cache (Cache Hit) --> D(4. API recupera dados do Cache)
    D --> E([5. API retorna dados para o Navegador/Aplicativo])
    C -- Dados não encontrados (Cache Miss) --> F(6. API publica mensagem na fila)
    F --> G(7. Microserviço processa a mensagem)
    G --> H(8. Consulta ao Banco de Dados)
    H --> I(9. Microserviço retorna dados para a fila)
    I --> J(10. API processa os dados)
    J --> K(11. Armazenamento em Cache)
    K --> L(12. API retorna dados para o Navegador/Aplicativo)
    L --> M([13. Navegador/Aplicativo exibe dados para o Usuário])

    style A fill:#5cb85c80,stroke:#4cae4c,stroke-width:2px,text-align:center,font-weight:bold,font-size:12px
    style M fill:#5cb85c80,stroke:#4cae4c,stroke-width:2px,text-align:center,font-weight:bold,font-size:12px
    style C fill:#f0ad4e80,stroke:#eea236,stroke-width:2px,text-align:center,font-weight:bold,font-size:12px
    style E fill:#5cb85c80,stroke:#4cae4c,stroke-width:2px,text-align:center,font-weight:bold,font-size:12px
```

```mermaid
graph TD
    A([1. Usuário interage com o sistema]) --> B(2. Requisição enviada para API Gateway)
    B --> C{3. Autenticação/Autorização}
    C -- Válido --> D(4. API Gateway roteia para Microsserviço "Produto")
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
    N --> O(14. Microsserviço "Relatórios" processa mensagem)
    O --> P(15. Microsserviço "Relatórios" atualiza relatórios)

    style A fill:#5cb85c80,stroke:#4cae4c,stroke-width:2px,text-align:center,font-weight:bold,font-size:12px
    style M fill:#5cb85c80,stroke:#4cae4c,stroke-width:2px,text-align:center,font-weight:bold,font-size:12px
    style C fill:#f0ad4e80,stroke:#eea236,stroke-width:2px,text-align:center,font-weight:bold,font-size:12px
    style E fill:#f0ad4e80,stroke:#d9534f,stroke-width:2px,text-align:center,font-weight:bold,font-size:12px
    style H fill:#5cb85c80,stroke:#4cae4c,stroke-width:2px,text-align:center,font-weight:bold,font-size:12px
    style L fill:#4285f4,stroke:#4285f4,stroke-width:2px,text-align:center,font-weight:bold,font-size:12px
```