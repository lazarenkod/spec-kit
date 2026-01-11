/**
 * Tests for User Management API
 */

import { createUser, updateUser, deleteUser } from './api';

/**
 * [TEST:AS-1A] Create user successfully
 */
describe('createUser', () => {
  it('should create user with valid data', async () => {
    const userData = {
      email: 'test@example.com',
      name: 'John Doe'
    };

    const user = await createUser(userData);

    expect(user.id).toBeDefined();
    expect(user.email).toBe('test@example.com');
    expect(user.name).toBe('John Doe');
    expect(user.createdAt).toBeInstanceOf(Date);
  });

  /**
   * [TEST:AS-1B] Reject invalid email
   */
  it('should reject invalid email format', async () => {
    const userData = {
      email: 'notanemail',
      name: 'John Doe'
    };

    await expect(createUser(userData)).rejects.toThrow('Invalid email format');
  });

  it('should reject empty name', async () => {
    const userData = {
      email: 'test@example.com',
      name: ''
    };

    await expect(createUser(userData)).rejects.toThrow('Name is required');
  });
});

/**
 * [TEST:AS-3A] Update user name
 */
describe('updateUser', () => {
  it('should update user name', async () => {
    const userId = '123';
    const updates = {
      name: 'Jane Doe'
    };

    const user = await updateUser(userId, updates);

    expect(user.name).toBe('Jane Doe');
  });

  // NOTE: No test for email update because implementation doesn't support it
  // This demonstrates the behavioral drift
});

/**
 * Test for deleteUser - but this function is not in spec.md!
 * This is reverse drift - code exists without spec
 */
describe('deleteUser', () => {
  it('should delete user by ID', async () => {
    const userId = '123';

    await expect(deleteUser(userId)).resolves.toBeUndefined();
  });

  it('should throw error for non-existent user', async () => {
    const userId = 'nonexistent';

    await expect(deleteUser(userId)).rejects.toThrow('User not found');
  });
});

// NOTE: No tests for FR-002 (password reset) because it's not implemented
// This demonstrates forward drift
