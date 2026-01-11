# Feature Specification: User Management API

**Status**: ACTIVE
**Version**: 1.0
**Feature ID**: FEAT-001-user-management

---

## Feature Description

User management API with CRUD operations for user accounts.

---

## Functional Requirements

### FR-001: User Creation

**Description**: Create a new user account with email and name.

**Input**: UserData { email: string, name: string }
**Output**: User { id: string, email: string, name: string, createdAt: Date }

**Validation**:
- Email must be valid format
- Name required (non-empty)

---

### FR-002: User Password Reset

**Description**: Allow users to reset their password via email link.

**Input**: { email: string }
**Output**: { success: boolean, resetToken: string }

**Business Rules**:
- Reset token expires in 1 hour
- Send email with reset link

**Note**: This requirement is NOT implemented in code (forward drift scenario).

---

### FR-003: User Update

**Description**: Update user profile information (name and email).

**Input**: userId: string, updates: Partial<UserData>
**Output**: Updated User object

**Business Rules**:
- Email must be unique if changed
- Validate email format

**Note**: Implementation exists but behavior differs - it only updates name, not email (behavioral drift scenario).

---

## Out of Scope

- User deletion (not in current version)
- User authentication (separate feature)

---

## Acceptance Scenarios

### AS-1A: Create user successfully

**Given** valid user data with email "test@example.com" and name "John Doe"
**When** POST /api/users
**Then** return 201 with user object including generated ID

---

### AS-1B: Reject invalid email

**Given** user data with invalid email "notanemail"
**When** POST /api/users
**Then** return 400 with validation error

---

### AS-3A: Update user name

**Given** existing user with ID "123"
**When** PATCH /api/users/123 with { name: "Jane Doe" }
**Then** return 200 with updated user object

---
