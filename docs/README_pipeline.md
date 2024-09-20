
# Pipeline de Automação - Consulta Rápida

## Estrutura do Projeto
- **Configurações de Ambiente**: Usamos variáveis de ambiente `ENV` para definir o ambiente de execução.
  - `development`: Ambiente de desenvolvimento.
  - `testing`: Ambiente de teste.
  - `production`: Ambiente de produção.

---

## 1. Ativar o Virtual Environment (venv)

### Criar e Ativar o venv:
```bash
python -m venv venv
```

### Ativar o venv:
- **Windows**:
  ```bash
  .\venv\Scripts\activate
  ```
- **Linux/Mac**:
  ```bash
  source venv/bin/activate
  ```

---

## 2. Ambiente de Desenvolvimento

### Definir ambiente:
- **Windows (PowerShell)**:
  ```bash
  $Env:ENV="development"
  ```
- **Linux/Mac**:
  ```bash
  export ENV=development
  ```

### Executar o pipeline:
```bash
python etl/pipeline_data_amazon.py
```

### Rodar Streamlit:
```bash
streamlit run app_main.py
```

---

## 3. Controle de Versão (Desenvolvimento)

### Inicializar Git e trabalhar no branch `develop`:
```bash
git init
git checkout develop
```

### Verificar mudanças e fazer commit:
```bash
git status
git add .
git commit -m "Adiciona documento de consulta para o pipeline"
```

### Enviar para o repositório remoto:
```bash
git push origin develop
```

---

## 4. Ambiente de Teste

### Definir ambiente:
- **Windows (PowerShell)**:
  ```bash
  $Env:ENV="testing"
  ```
- **Linux/Mac**:
  ```bash
  export ENV=testing
  ```

### Fazer merge do `develop` no `testing`:
```bash
git checkout testing
git merge develop
```

### Enviar para o repositório remoto:
```bash
git push origin testing
```

### Restaurar arquivos (opcional):
Caso queira descartar mudanças não desejadas:
```bash
git restore <nome_do_arquivo>
```

### Testar o código no ambiente de teste:
1. Executar o pipeline e o Streamlit com a variável `ENV=testing`.
2. Se os testes forem bem-sucedidos, mesclar para produção.

---

## 5. Ambiente de Produção

### Definir ambiente:
- **Windows (PowerShell)**:
  ```bash
  $Env:ENV="production"
  ```
- **Linux/Mac**:
  ```bash
  export ENV=production
  ```

### Fazer merge do `testing` no `main` (produção):
```bash
git checkout main
git merge testing
```

### Enviar para o repositório remoto:
```bash
git push origin main
```

---

## 6. Pipeline para Criação de Novas Funcionalidades

### 1. Criar um branch de funcionalidade:
Sempre crie uma nova branch a partir do `develop` para desenvolver novas funcionalidades.
```bash
git checkout develop
git checkout -b feature/<nome-da-funcionalidade>
```

### 2. Desenvolver e fazer commit:
```bash
git add .
git commit -m "Implementando <nome-da-funcionalidade>"
```

### 3. Fazer merge da funcionalidade no `develop`:
```bash
git checkout develop
git merge feature/<nome-da-funcionalidade>
```

### 4. Enviar as alterações para o repositório remoto:
```bash
git push origin develop
```

### 5. Testar no branch `testing`:
```bash
git checkout testing
git merge develop
git push origin testing
```

### 6. Realizar testes no ambiente de `testing`:
Teste as alterações e, se necessário, faça ajustes no branch `develop` e repita o processo de merge e testes.

---

## 7. Fazer Merge para Produção (main)

### Quando os testes forem concluídos com sucesso:
```bash
git checkout main
git merge testing
```

### Enviar para o repositório remoto:
```bash
git push origin main
```

---

## 8. Criar uma Nova Tag para a Versão de Produção

Após o merge no branch `main`, crie uma tag para marcar a versão de produção:
```bash
git tag -a v1.2.0 -m "Release versão 1.2.0"
git push origin v1.2.0
```

---


### Notas Finais:
- Sempre utilize as variáveis de ambiente para configurar corretamente cada ambiente.
- Mantenha a organização do fluxo de desenvolvimento com branches claros: `develop`, `testing` e `main`.
- Use o branch `testing` para garantir que o código esteja pronto antes de movê-lo para produção.
- Não esqueça de criar tags para cada versão de produção, seguindo o versionamento semântico.

