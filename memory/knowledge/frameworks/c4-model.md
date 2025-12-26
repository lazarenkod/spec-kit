# C4 Model Architecture Documentation Guide

## Overview

The C4 model is a way to visualize software architecture at different levels of abstraction. Created by Simon Brown, it provides a hierarchical approach to diagramming that helps communicate architecture to different audiences.

**C4 stands for**: Context, Containers, Components, Code

## The Four Levels

```text
Level 1: System Context    ──► Big picture: system + external actors
         ↓
Level 2: Container         ──► Inside the system: applications, data stores
         ↓
Level 3: Component         ──► Inside a container: modules, services
         ↓
Level 4: Code              ──► Inside a component: classes, functions
```

## Level 1: System Context Diagram

**Purpose**: Show the system in context — who uses it and what it interacts with.

**Audience**: Everyone — technical and non-technical stakeholders.

### Elements

| Element | Symbol | Description |
|---------|--------|-------------|
| Person | Stick figure | A user of the system |
| Software System | Box | Your system or external systems |
| Relationship | Arrow | How they interact |

### Example

```text
┌────────────────────────────────────────────────────────────────┐
│                     SYSTEM CONTEXT                              │
│                                                                │
│    ┌─────────┐                                                 │
│    │ Customer│                                                 │
│    │  (User) │                                                 │
│    └────┬────┘                                                 │
│         │ Uses                                                 │
│         ▼                                                      │
│    ┌────────────────────┐                                      │
│    │   E-Commerce       │                                      │
│    │   Platform         │                                      │
│    │   [Software Sys]   │                                      │
│    └─────────┬──────────┘                                      │
│              │                                                 │
│       ┌──────┴──────────┐                                      │
│       ▼                 ▼                                      │
│ ┌───────────────┐  ┌───────────────┐                           │
│ │ Payment       │  │ Shipping      │                           │
│ │ Provider      │  │ Provider      │                           │
│ │ [External]    │  │ [External]    │                           │
│ └───────────────┘  └───────────────┘                           │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

### Template

```markdown
## System Context: [System Name]

### Purpose
[What does this system do?]

### Users
| Actor | Description | Interaction |
|-------|-------------|-------------|
| [User type] | [Who they are] | [How they use system] |

### External Systems
| System | Description | Integration |
|--------|-------------|-------------|
| [System] | [What it does] | [How we integrate] |
```

---

## Level 2: Container Diagram

**Purpose**: Show the high-level technology choices — the applications and data stores that make up the system.

**Audience**: Technical people — developers, architects.

**Note**: "Container" here means a runtime unit (application, database), NOT Docker container.

### Elements

| Element | Examples |
|---------|----------|
| Web Application | React SPA, Angular app |
| Server-side Application | API, backend service |
| Mobile Application | iOS app, Android app |
| Database | PostgreSQL, MongoDB |
| File System | S3 bucket, file storage |
| Message Queue | RabbitMQ, Kafka |

### Example

```text
┌────────────────────────────────────────────────────────────────────┐
│                     CONTAINER DIAGRAM                               │
│                     E-Commerce Platform                             │
│                                                                    │
│    ┌─────────┐                                                     │
│    │ Customer│                                                     │
│    └────┬────┘                                                     │
│         │ HTTPS                                                    │
│         ▼                                                          │
│    ┌───────────────────┐        ┌───────────────────┐              │
│    │    Web App        │        │   Mobile App      │              │
│    │    [React SPA]    │        │   [React Native]  │              │
│    └─────────┬─────────┘        └─────────┬─────────┘              │
│              │                            │                        │
│              └──────────┬─────────────────┘                        │
│                         │ HTTPS/JSON                               │
│                         ▼                                          │
│              ┌───────────────────┐                                 │
│              │     API           │                                 │
│              │     [Node.js]     │                                 │
│              └─────────┬─────────┘                                 │
│                        │                                           │
│         ┌──────────────┼──────────────┐                            │
│         │              │              │                            │
│         ▼              ▼              ▼                            │
│   ┌───────────┐  ┌───────────┐  ┌───────────┐                      │
│   │ Database  │  │ Cache     │  │ Queue     │                      │
│   │[PostgreSQL│  │ [Redis]   │  │ [RabbitMQ]│                      │
│   └───────────┘  └───────────┘  └───────────┘                      │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

### Template

```markdown
## Container Diagram: [System Name]

### Containers

| Container | Technology | Purpose | Scaling |
|-----------|------------|---------|---------|
| Web App | React | Customer UI | CDN, static |
| API | Node.js/Express | Business logic | Horizontal |
| Database | PostgreSQL | Data persistence | Primary/Replica |

### Communication

| From | To | Protocol | Purpose |
|------|-----|----------|---------|
| Web App | API | HTTPS/REST | Data operations |
| API | Database | TCP/5432 | Data storage |
```

---

## Level 3: Component Diagram

**Purpose**: Show the internal structure of a container — the major components and their relationships.

**Audience**: Developers working on that container.

### Elements

| Element | Description |
|---------|-------------|
| Component | A grouping of related functionality (module, service) |
| Interface | How components communicate |

### Example

```text
┌────────────────────────────────────────────────────────────────────┐
│                     COMPONENT DIAGRAM                               │
│                     API Container                                   │
│                                                                    │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                        API Layer                              │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │  │
│  │  │   Orders     │  │   Products   │  │   Users      │        │  │
│  │  │  Controller  │  │  Controller  │  │  Controller  │        │  │
│  │  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘        │  │
│  └─────────┼─────────────────┼─────────────────┼────────────────┘  │
│            │                 │                 │                   │
│  ┌─────────┼─────────────────┼─────────────────┼────────────────┐  │
│  │         ▼                 ▼                 ▼                │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │  │
│  │  │   Orders     │  │   Products   │  │   Users      │        │  │
│  │  │   Service    │  │   Service    │  │   Service    │        │  │
│  │  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘        │  │
│  │         │                 │                 │  Service Layer │  │
│  └─────────┼─────────────────┼─────────────────┼────────────────┘  │
│            │                 │                 │                   │
│  ┌─────────┼─────────────────┼─────────────────┼────────────────┐  │
│  │         ▼                 ▼                 ▼                │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │  │
│  │  │   Orders     │  │   Products   │  │   Users      │        │  │
│  │  │  Repository  │  │  Repository  │  │  Repository  │        │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘        │  │
│  │                                            Data Access Layer │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                              │                                     │
│                              ▼                                     │
│                    ┌──────────────────┐                            │
│                    │    PostgreSQL    │                            │
│                    └──────────────────┘                            │
└────────────────────────────────────────────────────────────────────┘
```

### Template

```markdown
## Component Diagram: [Container Name]

### Components

| Component | Responsibility | Dependencies |
|-----------|----------------|--------------|
| OrdersController | Handle order API requests | OrdersService |
| OrdersService | Order business logic | OrdersRepository, PaymentGateway |
| OrdersRepository | Order data access | Database |

### Interfaces

| Interface | Protocol | Consumers |
|-----------|----------|-----------|
| /api/orders | REST | Web App, Mobile App |
```

---

## Level 4: Code Diagram

**Purpose**: Show the internal structure of a component — classes, interfaces, relationships.

**Audience**: Developers working on that specific component.

**Note**: Often generated from code (UML class diagrams) rather than manually maintained.

### When to Use

| Use | Don't Use |
|-----|-----------|
| Complex domain models | Simple CRUD |
| Key algorithms | Self-documenting code |
| Onboarding new developers | Rapidly changing code |

### Example

```text
┌────────────────────────────────────────────────────────────────┐
│                     CODE DIAGRAM                                │
│                     Order Domain                                │
│                                                                │
│  ┌─────────────────────┐      ┌─────────────────────┐          │
│  │     <<interface>>   │      │      Order          │          │
│  │   OrderRepository   │◄─────│                     │          │
│  ├─────────────────────┤      ├─────────────────────┤          │
│  │ + findById(id)      │      │ - id: UUID          │          │
│  │ + save(order)       │      │ - status: Status    │          │
│  │ + findByCustomer()  │      │ - items: OrderItem[]│          │
│  └─────────────────────┘      │ - total: Money      │          │
│                               ├─────────────────────┤          │
│                               │ + addItem()         │          │
│                               │ + removeItem()      │          │
│                               │ + calculateTotal()  │          │
│                               │ + submit()          │          │
│                               └──────────┬──────────┘          │
│                                          │                     │
│                                          │ 1..*                │
│                                          ▼                     │
│                               ┌─────────────────────┐          │
│                               │     OrderItem       │          │
│                               ├─────────────────────┤          │
│                               │ - product: Product  │          │
│                               │ - quantity: int     │          │
│                               │ - price: Money      │          │
│                               └─────────────────────┘          │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

---

## Supplementary Diagrams

### Deployment Diagram

**Purpose**: Show where containers run in production.

```text
┌────────────────────────────────────────────────────────────────┐
│                     DEPLOYMENT DIAGRAM                          │
│                                                                │
│  ┌────────────────────────────────────────────────────────┐    │
│  │                    AWS                                  │    │
│  │                                                        │    │
│  │  ┌──────────────┐    ┌──────────────────────────────┐  │    │
│  │  │ CloudFront   │    │      ECS Cluster             │  │    │
│  │  │  (CDN)       │    │                              │  │    │
│  │  │ ┌──────────┐ │    │  ┌────────┐  ┌────────┐     │  │    │
│  │  │ │ Web App  │ │    │  │  API   │  │  API   │     │  │    │
│  │  │ │ (Static) │ │    │  │ (x3)   │  │ (x3)   │     │  │    │
│  │  │ └──────────┘ │    │  └────────┘  └────────┘     │  │    │
│  │  └──────────────┘    └──────────────────────────────┘  │    │
│  │                                   │                     │    │
│  │                                   ▼                     │    │
│  │                      ┌──────────────────────┐          │    │
│  │                      │     RDS (Multi-AZ)   │          │    │
│  │                      │     PostgreSQL       │          │    │
│  │                      └──────────────────────┘          │    │
│  │                                                        │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

### Dynamic Diagram

**Purpose**: Show how containers/components interact for a specific use case.

```text
┌────────────────────────────────────────────────────────────────┐
│                     DYNAMIC: Order Placement                    │
│                                                                │
│   User    Web App      API        Orders      Payment          │
│    │         │          │         Service      Gateway         │
│    │         │          │            │            │            │
│    │ Click   │          │            │            │            │
│    │ Buy     │          │            │            │            │
│    ├────────►│          │            │            │            │
│    │         │ POST     │            │            │            │
│    │         │ /orders  │            │            │            │
│    │         ├─────────►│            │            │            │
│    │         │          │ Create     │            │            │
│    │         │          │ Order      │            │            │
│    │         │          ├───────────►│            │            │
│    │         │          │            │ Charge     │            │
│    │         │          │            ├───────────►│            │
│    │         │          │            │            │            │
│    │         │          │            │◄───────────┤ Success    │
│    │         │          │◄───────────┤            │            │
│    │         │◄─────────┤ 201        │            │            │
│    │◄────────┤          │            │            │            │
│    │ Show    │          │            │            │            │
│    │ Success │          │            │            │            │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

---

## Best Practices

### General Guidelines

| Do | Don't |
|-----|-------|
| Start with Context | Start with details |
| Use consistent notation | Mix different notation styles |
| Show runtime containers | Show code packages |
| Include technology choices | Leave technology ambiguous |
| Update diagrams with code | Let diagrams become stale |

### Diagram Content

| Include | Exclude |
|---------|---------|
| Names and descriptions | Implementation details |
| Technology choices | Code-level details in L1-L2 |
| Key relationships | Every relationship |
| Direction of data flow | Internal mechanisms |

### Notation

```text
[Person]           = User or role
[Software System]  = Your system (box)
[External System]  = External system (box, different color)
[Container]        = Runtime unit (box with technology)
[Component]        = Logical grouping (box)
───────►           = Synchronous relationship
- - - - ►          = Asynchronous relationship
```

---

## Tooling

### Diagramming Tools

| Tool | Type | C4 Support |
|------|------|------------|
| Structurizr | DSL-based | Native |
| PlantUML | Text-based | Via extension |
| Mermaid | Text-based | Limited |
| Draw.io | Visual | Templates |
| Lucidchart | Visual | Templates |

### Structurizr DSL Example

```dsl
workspace {
    model {
        customer = person "Customer"

        ecommerce = softwareSystem "E-Commerce Platform" {
            webapp = container "Web Application" "React SPA"
            api = container "API" "Node.js/Express" {
                ordersController = component "Orders Controller"
                ordersService = component "Orders Service"
            }
            database = container "Database" "PostgreSQL"
        }

        customer -> webapp "Uses"
        webapp -> api "API calls"
        api -> database "Reads/Writes"
    }

    views {
        systemContext ecommerce {
            include *
            autoLayout
        }

        container ecommerce {
            include *
            autoLayout
        }
    }
}
```

---

## Resources

- **Official Website**: [c4model.com](https://c4model.com)
- **Structurizr**: [structurizr.com](https://structurizr.com)
- **Book**: "Software Architecture for Developers" by Simon Brown
- **Video**: Simon Brown's talks on C4 model
