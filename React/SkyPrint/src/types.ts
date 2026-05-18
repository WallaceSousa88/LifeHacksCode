export type UserRole = 'manager' | 'operator';

export interface UserProfile {
  uid: string;
  email: string;
  displayName: string;
  role: UserRole;
}

export interface Printer {
  id: string;
  name: string;
}

export interface Service {
  id: string;
  description: string;
  status: 'pending' | 'completed';
  order: number;
  printerId: string;
  createdAt: any; // ServerTimestamp
  completedAt?: any;
  completedBy?: string;
  completedByEmail?: string;
}

export enum OperationType {
  CREATE = 'create',
  UPDATE = 'update',
  DELETE = 'delete',
  LIST = 'list',
  GET = 'get',
  WRITE = 'write',
}

export interface FirestoreErrorInfo {
  error: string;
  operationType: OperationType;
  path: string | null;
  authInfo: {
    userId?: string | null;
    email?: string | null;
    emailVerified?: boolean | null;
    isAnonymous?: boolean | null;
  }
}
