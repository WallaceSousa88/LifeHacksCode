### NUGET

| Pacote | Versão |
|--------|--------|
| NETStandard.Library | 2.0.3 |
| Xamarin.Essentials | 1.8.1 |
| Xamarin.Forms | 5.0.0.2662 |
| Xamarin.Google.MLKit.TextRecognition | 116.0.0.5 |
| DotNet.ReproducibleBuilds | 1.2.4 |
| Microsoft.NETFramework.ReferenceAssemblies | 1.0.0 |
| Xamarin.AndroidX.Camera.Camera2 | 1.3.0 |
| Xamarin.AndroidX.Camera.Lifecycle | 1.3.0 |
| Xamarin.AndroidX.Camera.View | 1.3.0 |
| Xamarin.AndroidX.Fragment.Ktx | 1.6.2 |
| Xamarin.AndroidX.Lifecycle.LiveData | 2.6.2.2 |

## Tecnologias Utilizadas

- Linguagem de Programação: C# (Backend) / HTML, CSS, JS (Frontend).
- Framework Backend: ASP.NET Core (para criação de APIs RESTful).
- Framework Frontend: React (para interface web responsiva) / React Native (para aplicativo móvel).
- Banco de Dados: SQL Server (confiabilidade e robustez).
- Cache: Redis (armazenamento em memória para alta performance).
- Message Broker: RabbitMQ (comunicação assíncrona e escalabilidade).
- IDEs: Visual Studio, Visual Studio Code.
- Ferramentas: Git (controle de versão), Swagger (documentação da API).

| Passo | Ação | Detalhes |
|---|---|---|
| 1 | Usuário interage com o sistema | Acessa o sistema via Navegador/Aplicativo. |
| 2 | Requisição enviada para a API | O Navegador/Aplicativo envia a requisição para a API (ASP.NET Core). |
| 3 | Verificação no Cache | A API verifica se os dados solicitados estão presentes no Cache (Redis). |
| 4 | Dados em Cache (Cache Hit) | Se os dados estiverem no cache: <br> - A API recupera os dados do Cache. <br> - A API retorna os dados para o Navegador/Aplicativo. |
| 5 | Dados não encontrados no Cache (Cache Miss) | Se os dados não estiverem no cache: <br> - A API publica uma mensagem na fila (RabbitMQ). |
| 6 | Microserviço processa a mensagem | O Microserviço (C#) consome a mensagem da fila. |
| 7 | Consulta ao Banco de Dados | O Microserviço consulta o Banco de Dados (SQL Server) pelos dados. |
| 8 | Retorno dos dados | O Microserviço retorna os dados para a fila (RabbitMQ). |
| 9 | API processa os dados | A API consome a mensagem da fila com os dados. | 
| 10 | Armazenamento em Cache | A API armazena os dados no Cache (Redis) para futuras requisições. |
| 11 | Retorno para o Usuário | A API retorna os dados para o Navegador/Aplicativo, que os exibe para o Usuário. |

```mermaid
graph TD
    A[1. Usuário interage com o sistema] --> B(2. Requisição enviada para a API)
    B --> C{3. Verificação no Cache}
    C -- Dados em Cache (Cache Hit) --> D(4. API recupera dados do Cache)
    D --> E(4. API retorna dados para o Navegador/Aplicativo)
    C -- Dados não encontrados (Cache Miss) --> F(5. API publica mensagem na fila)
    F --> G(6. Microserviço processa a mensagem)
    G --> H(7. Consulta ao Banco de Dados)
    H --> I(8. Microserviço retorna dados para a fila)
    I --> J(9. API processa os dados)
    J --> K(10. Armazenamento em Cache)
    K --> L(11. API retorna dados para o Navegador/Aplicativo)
    L --> M(11. Navegador/Aplicativo exibe dados para o Usuário)

    style A fill:#5cb85c,stroke:#4cae4c
    style M fill:#5cb85c,stroke:#4cae4c
    style C fill:#f0ad4e,stroke:#eea236
    style E fill:#5cb85c,stroke:#4cae4c
    style L fill:#5cb85c,stroke:#4cae4c

## Hospedagem