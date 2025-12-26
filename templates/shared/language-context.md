# Language Context

## Loading Project Language

Before generating artifacts, check `/memory/constitution.md` for the `language` setting in the **Project Settings** section.

```text
LANGUAGE_CODE = extract from constitution.md Project Settings table
IF not found: LANGUAGE_CODE = "en" (default)
```

## Language Behavior

| Language Code | Artifact Language | Technical Terms |
|---------------|-------------------|-----------------|
| `en` | English | English |
| `ru` | Russian | English (API, CRUD, JWT, etc.) |
| `de` | German | English |
| `fr` | French | English |
| `es` | Spanish | English |
| `zh` | Chinese | English |
| `ja` | Japanese | English |
| `ko` | Korean | English |
| `pt` | Portuguese | English |
| `it` | Italian | English |
| `pl` | Polish | English |
| `uk` | Ukrainian | English |
| `ar` | Arabic | English |
| `hi` | Hindi | English |

## What to Translate

**Always in configured language**:
- Section headers (## Functional Requirements → ## Функциональные требования)
- Requirement descriptions
- User stories and acceptance criteria
- Comments and notes
- Validation messages
- Error descriptions
- UX/UI text

**Always in English** (do not translate):
- IDs: FR-001, AS-001, EC-001, T1, etc.
- Technical terms: API, REST, JWT, CRUD, HTTP, SQL, etc.
- Code snippets and variable names
- File paths and URLs
- Dependency names and versions
- Protocol keywords: MUST, SHOULD, MAY (RFC 2119)

## Translation Examples

### English (en) - Default
```markdown
## Functional Requirements

### FR-001: User Authentication
The user MUST be able to log in using email and password.

**Acceptance Criteria**:
- Given a valid email and password, when the user submits, then a session is created
```

### Russian (ru)
```markdown
## Функциональные требования

### FR-001: Аутентификация пользователя
Пользователь MUST иметь возможность войти в систему используя email и пароль.

**Критерии приёмки**:
- Дано: валидные email и пароль; Когда: пользователь отправляет форму; Тогда: создаётся сессия
```

### German (de)
```markdown
## Funktionale Anforderungen

### FR-001: Benutzerauthentifizierung
Der Benutzer MUST sich mit E-Mail und Passwort anmelden können.

**Akzeptanzkriterien**:
- Gegeben: gültige E-Mail und Passwort; Wenn: Benutzer sendet ab; Dann: Sitzung wird erstellt
```

### French (fr)
```markdown
## Exigences fonctionnelles

### FR-001: Authentification utilisateur
L'utilisateur MUST pouvoir se connecter avec un email et un mot de passe.

**Critères d'acceptation**:
- Étant donné: email et mot de passe valides; Quand: l'utilisateur soumet; Alors: une session est créée
```

### Spanish (es)
```markdown
## Requisitos funcionales

### FR-001: Autenticación de usuario
El usuario MUST poder iniciar sesión usando email y contraseña.

**Criterios de aceptación**:
- Dado: email y contraseña válidos; Cuando: el usuario envía; Entonces: se crea una sesión
```

### Chinese (zh)
```markdown
## 功能需求

### FR-001: 用户认证
用户 MUST 能够使用电子邮件和密码登录。

**验收标准**:
- 给定：有效的电子邮件和密码；当：用户提交时；那么：创建会话
```

### Japanese (ja)
```markdown
## 機能要件

### FR-001: ユーザー認証
ユーザーは MUST メールアドレスとパスワードでログインできる必要があります。

**受け入れ基準**:
- 前提：有効なメールアドレスとパスワード；条件：ユーザーが送信する；結果：セッションが作成される
```

## Usage in Commands

Commands that generate artifacts should:

1. **Read language setting** at the start:
   ```text
   Read /memory/constitution.md
   Extract language from Project Settings table
   Default to "en" if not specified
   ```

2. **Apply language** during artifact generation:
   ```text
   Generate all prose content in {LANGUAGE}
   Keep IDs, technical terms, code in English
   ```

3. **Confirm language** in output:
   ```text
   "Generating spec.md in Russian (ru)..."
   ```
