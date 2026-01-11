/**
 * User Management API
 * This file contains user CRUD operations
 */

export interface User {
  id: string;
  email: string;
  name: string;
  createdAt: Date;
}

export interface UserData {
  email: string;
  name: string;
}

/**
 * Create a new user account
 * @speckit:FR:FR-001
 */
export async function createUser(data: UserData): Promise<User> {
  // Validate email format
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(data.email)) {
    throw new Error('Invalid email format');
  }

  // Validate name
  if (!data.name || data.name.trim().length === 0) {
    throw new Error('Name is required');
  }

  // Create user (mock implementation)
  const user: User = {
    id: generateId(),
    email: data.email,
    name: data.name,
    createdAt: new Date()
  };

  // Save to database
  await saveUser(user);

  return user;
}

/**
 * Update user profile information
 * @speckit:FR:FR-003
 *
 * NOTE: This implementation only updates name, not email
 * This is BEHAVIORAL DRIFT - spec says it should update both
 */
export async function updateUser(userId: string, updates: Partial<UserData>): Promise<User> {
  const user = await getUserById(userId);

  if (!user) {
    throw new Error('User not found');
  }

  // DRIFT: Only updating name, ignoring email updates
  if (updates.name) {
    user.name = updates.name;
  }

  await saveUser(user);
  return user;
}

/**
 * Delete a user account permanently
 *
 * NOTE: This API is NOT in spec.md (reverse drift scenario)
 * It's implemented but not documented in requirements
 */
export async function deleteUser(userId: string): Promise<void> {
  const user = await getUserById(userId);

  if (!user) {
    throw new Error('User not found');
  }

  // Soft delete
  await markUserAsDeleted(userId);

  // Send deletion confirmation email
  await sendDeletionEmail(user.email);
}

/**
 * Archive inactive users (internal function)
 * @internal
 */
export async function archiveInactiveUsers(daysInactive: number): Promise<number> {
  // This is an internal function - should be ignored by drift detection
  const users = await findInactiveUsers(daysInactive);

  for (const user of users) {
    await archiveUser(user.id);
  }

  return users.length;
}

// Helper functions (mock implementations)
function generateId(): string {
  return Math.random().toString(36).substring(7);
}

async function saveUser(user: User): Promise<void> {
  // Mock database save
  console.log('Saving user:', user);
}

async function getUserById(id: string): Promise<User | null> {
  // Mock database query
  return {
    id,
    email: 'test@example.com',
    name: 'Test User',
    createdAt: new Date()
  };
}

async function markUserAsDeleted(userId: string): Promise<void> {
  // Mock soft delete
  console.log('Marking user as deleted:', userId);
}

async function sendDeletionEmail(email: string): Promise<void> {
  // Mock email sending
  console.log('Sending deletion email to:', email);
}

async function findInactiveUsers(daysInactive: number): Promise<User[]> {
  // Mock query
  return [];
}

async function archiveUser(userId: string): Promise<void> {
  // Mock archive
  console.log('Archiving user:', userId);
}
