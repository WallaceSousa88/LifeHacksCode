## Teste

```mermaid
graph TD
    A(1. Usuário envia requisição) --> B(2. API)
    B --> C(3. Autenticação JWT)
    C -- Válido --> D(4. API roteia para o endpoint)
    C -- Inválido --> E(5. Retorno 401 Unauthorized)
    D --> F(6. Controlador processa a requisição)
    F --> G(7. Serviço de Negócio)
    G --> H(8. Repositório AppDbContext)
    H --> I(9. Banco de Dados SQL Server)
    I --> H
    H --> G
    G --> F
    F --> J(10. Formatação da Resposta)
    J --> K(11. API)
    K --> L(12. Resposta enviada ao Usuário)

    style A fill:#5cb85c80,stroke:#4cae4c,stroke-width:2px,text-align:center,font-size:12px
    style C fill:#f0ad4e80,stroke:#eea236,stroke-width:2px,text-align:center,font-size:12px
    style E fill:#5cb85c80,stroke:#d9534f,stroke-width:2px,text-align:center,font-size:12px
    style F fill:#f0ad4e80,stroke:#eea236,stroke-width:2px,text-align:center,font-size:12px
    style J fill:#f0ad4e80,stroke:#eea236,stroke-width:2px,text-align:center,font-size:12px
    style L fill:#5cb85c80,stroke:#4cae4c,stroke-width:2px,text-align:center,font-size:12px
```