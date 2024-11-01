#### Diagramas de Classes

```mermaid
classDiagram
    class Usuario {
        +int id
        +string nomeUsuario
        +string senha
    }

    class Fornecedor {
        +int id
        +string nomeFantasia
        +string CNPJ
        +string telefone
        +string email
    }

    class Medicamento {
        +int id
        +string nomeComercial
        +decimal precoCusto
        +decimal precoVenda
        +int? fornecedorId
        +byte[]? imagem
    }

    class Lote {
        +int id
        +int quantidade
        +DateTime dataFabricacao
        +DateTime dataValidade
        +int? medicamentoId
    }

    class Entrada {
        +int id
        +DateTime dataEntrada
        +int quantidadeRecebida
        +int loteId
    }

    class Saida {
        +int id
        +DateTime dataSaida
        +int quantidadeSaida
        +int loteId
    }

    Fornecedor "1" --> "0..*" Medicamento : fornece
    Medicamento "1" --> "0..*" Lote : contém
    Lote "1" --> "0..*" Entrada : tem
    Lote "1" --> "0..*" Saida : tem
```

#### Diagramas de Entidade-Relacionamento (ER)

```mermaid
erDiagram
    USUARIO {
        int id
        string nomeUsuario
        string senha
    }

    FORNECEDOR {
        int id
        string nomeFantasia
        string CNPJ
        string telefone
        string email
    }

    MEDICAMENTO {
        int id
        string nomeComercial
        decimal precoCusto
        decimal precoVenda
        int fornecedorId
        byte[] imagem
    }

    LOTE {
        int id
        int quantidade
        DateTime dataFabricacao
        DateTime dataValidade
        int medicamentoId
    }

    ENTRADA {
        int id
        DateTime dataEntrada
        int quantidadeRecebida
        int loteId
    }

    SAIDA {
        int id
        DateTime dataSaida
        int quantidadeSaida
        int loteId
    }

    FORNECEDOR ||--o{ MEDICAMENTO : "fornece"
    MEDICAMENTO ||--o{ LOTE : "contém"
    LOTE ||--o{ ENTRADA : "tem"
    LOTE ||--o{ SAIDA : "tem"
```