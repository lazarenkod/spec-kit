# Feature Specification: Product Catalog API

**Status**: ACTIVE
**Version**: 1.0
**Feature ID**: FEAT-002-product-catalog

---

## Feature Description

REST API for managing product catalog with CRUD operations.

---

## Functional Requirements

### FR-001: Product Creation

**Description**: Create a new product with name, description, price, and stock.

**Input**: ProductData { name: str, description: str, price: float, stock: int }
**Output**: Product { id: str, name: str, description: str, price: float, stock: int, created_at: datetime }

**Validation**:
- Name required (non-empty)
- Price must be positive
- Stock must be non-negative

---

### FR-002: Product Search

**Description**: Search products by name or description with pagination.

**Input**: { query: str, page: int = 1, page_size: int = 10 }
**Output**: { products: List[Product], total: int, page: int, pages: int }

**Business Rules**:
- Case-insensitive search
- Search in both name and description fields
- Default page size: 10 items

**Note**: This requirement is NOT implemented in code (forward drift scenario).

---

### FR-003: Product Update

**Description**: Update product information including price and stock levels.

**Input**: product_id: str, updates: Partial[ProductData]
**Output**: Updated Product object

**Business Rules**:
- Price changes require audit log entry
- Stock cannot go negative
- Update all provided fields

**Note**: Implementation exists but only updates price, ignores stock updates (behavioral drift scenario).

---

### FR-004: Product Deletion

**Description**: Soft-delete a product (mark as inactive rather than removing from database).

**Input**: product_id: str
**Output**: None (204 status)

**Business Rules**:
- Products with active orders cannot be deleted
- Deletion is reversible (soft delete)

---

## Out of Scope

- Product categories (separate feature)
- Product images (separate feature)
- Inventory management (separate feature)

---

## Acceptance Scenarios

### AS-1A: Create product successfully

**Given** valid product data with name "Laptop", price 999.99, stock 10
**When** POST /api/products
**Then** return 201 with product object including generated ID

---

### AS-1B: Reject negative price

**Given** product data with price -50.00
**When** POST /api/products
**Then** return 400 with validation error "Price must be positive"

---

### AS-3A: Update product price

**Given** existing product with ID "123"
**When** PATCH /api/products/123 with { price: 899.99 }
**Then** return 200 with updated product object
**And** audit log entry created

---

### AS-4A: Delete product

**Given** existing product with ID "456" and no active orders
**When** DELETE /api/products/456
**Then** return 204
**And** product marked as inactive

---
