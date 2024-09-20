# Pipeline de Automação - Consulta Rápida

## Estrutura do Projeto
- **Configurações de Ambiente**: Usamos variáveis de ambiente `ENV` para definir se estamos em ambiente de desenvolvimento, teste ou produção.
  - `development`: Ambiente de desenvolvimento.
  - `testing`: Ambiente de teste.
  - `production`: Ambiente de produção.
  
## ATIVAR VENV
python -m venv venv
.\venv\Scripts\activate
source venv/bin/activate
  
### AMBIENTE DE DESENVOLVIMENTO

  - **Windows**:powershell `set ENV=development`
  $Env:ENV="development"

- Para executar o pipeline:
  ```bash
  python etl/pipeline_data_amazon.py

  Rodar o strimilit no terminal:
streamlit run app_main.py

## ATIVAR GIT HUB (Desenvolvimento)
git init
git checkout develop * Para branch de dev
git status
git add .
git status
git commit -m "Adiciona documento de consulta para o pipeline"
git push origin develop

### AMBIENTE DE TESTE
POWERSHELL: $Env:ENV="testing"

git checkout testing
git merge develop
*
git push origin testing


*git restore app_main.py (Caso não deseja subir as alterações feitas)
Se os testes forem bem-sucedidos e tudo funcionar conforme esperado, podemos seguir para a mesclagem para produção no branch main.
Se houver algum problema, faça as correções necessárias no branch develop, e depois volte a testar.

### PRODUÇÃO

git checkout main
git merge testing
git push origin main

git tag -a v1.2.0 -m "Release versão 1.2.0"

git push origin v1.2.0

POWERSHELL: $Env:ENV="production"

Melhor prática:
Versionamento semântico: siga o formato vX.Y.Z, onde:
X é a versão principal (major) — aumenta para mudanças de grande impacto.
Y é a versão secundária (minor) — aumenta para adição de funcionalidades sem quebrar compatibilidade.
Z é a versão de patch — aumenta para correções de bugs e pequenas melhorias.

## Pipeline para Criação de Novas Funcionalidades
Sempre que você for criar uma nova funcionalidade ou corrigir um bug, siga este pipeline de trabalho:

1. Criar um Branch de Funcionalidade
Sempre crie uma nova branch a partir do branch develop para desenvolver a nova funcionalidade. A convenção comum é nomear as branches de funcionalidades como feature/<nome-da-funcionalidade>.
Comando:
bash
Copiar código
git checkout develop
git checkout -b feature/<nome-da-funcionalidade>
2. Desenvolver a Funcionalidade
Faça as alterações no código na branch de funcionalidade. Teste localmente e, uma vez que as alterações estejam prontas, faça o commit.
Comando:
bash
Copiar código
git add .
git commit -m "Implementando <nome-da-funcionalidade>"
3. Fazer Merge da Funcionalidade no Branch develop
Depois que o desenvolvimento da funcionalidade for concluído, faça o merge do branch de funcionalidade no branch develop.
Comando:
bash
Copiar código
git checkout develop
git merge feature/<nome-da-funcionalidade>
4. Enviar as Alterações para o Repositório Remoto
Envie as alterações para o branch develop no GitHub.
Comando:
bash
Copiar código
git push origin develop
5. Testar no Branch testing
Quando o branch develop estiver estável e pronto para testes, faça o merge no branch testing para realizar os testes em um ambiente separado.

Comando:

bash
Copiar código
git checkout testing
git merge develop
Envie as alterações para o repositório remoto.

bash
Copiar código
git push origin testing
6. Testes
Realize todos os testes necessários no branch testing. Faça ajustes se necessário no branch develop e repita o processo de merge e testes.
7. Fazer Merge para Produção (main)
Depois que os testes forem concluídos com sucesso, faça o merge no branch main para mover o código para produção.

Comando:

bash
Copiar código
git checkout main
git merge testing
Envie as alterações para o repositório remoto.

bash
Copiar código
git push origin main
8. Criar uma Nova Tag para a Versão de Produção
Após o merge no branch main, crie uma nova tag para marcar a versão de produção.
Comando:
bash
Copiar código
git tag -a v1.2.0 -m "Release versão 1.2.0"
git push origin v1.2.0

###########################################################################################################################