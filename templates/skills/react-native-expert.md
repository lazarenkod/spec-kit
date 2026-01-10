---
description: React Native expertise for cross-platform mobile development with native module integration
---

## User Input
$ARGUMENTS

## Purpose

Provides deep React Native expertise for building production-ready mobile applications. Covers feature-first architecture, state management with Redux/Zustand, native module integration, and Hermes engine optimization.

## When to Use

- Platform detected as `react-native` (via `platform-detection.md`)
- Project has `package.json` with `react-native` dependency
- Project has `metro.config.js` or similar RN configuration
- Code uses React/JSX with React Native components

## Quality Gates

| Gate ID | Purpose | Threshold |
|---------|---------|-----------|
| QG-RN-001 | Component tests for all screens | ≥ 80% |
| QG-RN-002 | Consistent state management | PASS/FAIL |
| QG-RN-003 | Native modules have TypeScript types | PASS/FAIL |
| QG-RN-004 | Hermes engine enabled | PASS/FAIL |

## Execution Steps

### 1. Validate Project Structure

```text
VERIFY structure:
  src/
  ├── core/                      # Shared utilities
  │   ├── api/                   # API client (axios/fetch)
  │   ├── hooks/                 # Custom hooks
  │   ├── navigation/            # React Navigation setup
  │   ├── store/                 # Global state (Redux/Zustand)
  │   └── theme/                 # Design tokens, styled-components
  ├── features/                  # Feature-first organization
  │   └── {feature}/
  │       ├── api/               # Feature-specific API calls
  │       ├── components/        # Feature components
  │       ├── hooks/             # Feature hooks
  │       ├── screens/           # Screen components
  │       └── store/             # Feature state (slice/store)
  ├── shared/                    # Shared components
  │   ├── components/            # Button, Input, Card, etc.
  │   └── utils/                 # Utility functions
  └── App.tsx

ios/                             # iOS native project
android/                         # Android native project

IF structure missing:
  RECOMMEND: Create feature directories
  PROVIDE: Navigation and state management setup
```

### 2. Configure Dependencies

```json
// package.json - Recommended dependencies
{
  "dependencies": {
    "react": "18.2.0",
    "react-native": "0.73.x",

    // Navigation
    "@react-navigation/native": "^6.1.9",
    "@react-navigation/native-stack": "^6.9.17",
    "@react-navigation/bottom-tabs": "^6.5.11",

    // State Management (choose one)
    "@reduxjs/toolkit": "^2.0.1",
    "react-redux": "^9.0.4",
    // OR
    "zustand": "^4.4.7",

    // Networking
    "axios": "^1.6.2",
    "@tanstack/react-query": "^5.17.0",

    // Local Storage
    "@react-native-async-storage/async-storage": "^1.21.0",

    // Utilities
    "react-native-mmkv": "^2.11.0",
    "react-native-reanimated": "^3.6.1",
    "react-native-gesture-handler": "^2.14.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.45",
    "@types/react-native": "^0.73.0",
    "@testing-library/react-native": "^12.4.3",
    "jest": "^29.7.0",
    "typescript": "^5.3.3"
  }
}
```

### 3. State Management with Zustand

```typescript
// src/features/library/store/libraryStore.ts
import { create } from 'zustand';
import { immer } from 'zustand/middleware/immer';
import { persist, createJSONStorage } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';

interface Book {
  id: string;
  title: string;
  author: string;
}

interface LibraryState {
  books: Book[];
  loading: boolean;
  error: string | null;
}

interface LibraryActions {
  loadBooks: () => Promise<void>;
  addBook: (book: Omit<Book, 'id'>) => Promise<void>;
  deleteBook: (id: string) => Promise<void>;
  clearError: () => void;
}

type LibraryStore = LibraryState & LibraryActions;

export const useLibraryStore = create<LibraryStore>()(
  persist(
    immer((set, get) => ({
      // State
      books: [],
      loading: false,
      error: null,

      // Actions
      loadBooks: async () => {
        set({ loading: true, error: null });
        try {
          const response = await api.getBooks();
          set({ books: response.data, loading: false });
        } catch (error) {
          set({ error: error.message, loading: false });
        }
      },

      addBook: async (book) => {
        try {
          const newBook = await api.addBook(book);
          set((state) => {
            state.books.push(newBook);
          });
        } catch (error) {
          set({ error: error.message });
        }
      },

      deleteBook: async (id) => {
        try {
          await api.deleteBook(id);
          set((state) => {
            state.books = state.books.filter((b) => b.id !== id);
          });
        } catch (error) {
          set({ error: error.message });
        }
      },

      clearError: () => set({ error: null }),
    })),
    {
      name: 'library-storage',
      storage: createJSONStorage(() => AsyncStorage),
      partialize: (state) => ({ books: state.books }), // Only persist books
    }
  )
);
```

### 4. Redux Toolkit Alternative

```typescript
// src/features/library/store/librarySlice.ts
import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';

interface LibraryState {
  books: Book[];
  loading: boolean;
  error: string | null;
}

const initialState: LibraryState = {
  books: [],
  loading: false,
  error: null,
};

export const loadBooks = createAsyncThunk(
  'library/loadBooks',
  async (_, { rejectWithValue }) => {
    try {
      const response = await api.getBooks();
      return response.data;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const librarySlice = createSlice({
  name: 'library',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(loadBooks.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(loadBooks.fulfilled, (state, action: PayloadAction<Book[]>) => {
        state.books = action.payload;
        state.loading = false;
      })
      .addCase(loadBooks.rejected, (state, action) => {
        state.error = action.payload as string;
        state.loading = false;
      });
  },
});

export const { clearError } = librarySlice.actions;
export default librarySlice.reducer;
```

### 5. Screen Implementation

```typescript
// src/features/library/screens/LibraryScreen.tsx
import React, { useEffect } from 'react';
import {
  View,
  Text,
  FlatList,
  ActivityIndicator,
  StyleSheet,
  TouchableOpacity,
  RefreshControl,
} from 'react-native';
import { useLibraryStore } from '../store/libraryStore';
import { BookCard } from '../components/BookCard';
import { EmptyState } from '@/shared/components/EmptyState';
import { ErrorState } from '@/shared/components/ErrorState';

export function LibraryScreen() {
  const { books, loading, error, loadBooks, clearError } = useLibraryStore();

  useEffect(() => {
    loadBooks();
  }, []);

  if (loading && books.length === 0) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" />
      </View>
    );
  }

  if (error && books.length === 0) {
    return (
      <ErrorState
        message={error}
        onRetry={() => {
          clearError();
          loadBooks();
        }}
      />
    );
  }

  if (books.length === 0) {
    return <EmptyState message="No books in your library" />;
  }

  return (
    <FlatList
      data={books}
      keyExtractor={(item) => item.id}
      renderItem={({ item }) => <BookCard book={item} />}
      refreshControl={
        <RefreshControl refreshing={loading} onRefresh={loadBooks} />
      }
      contentContainerStyle={styles.list}
    />
  );
}

const styles = StyleSheet.create({
  center: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  list: {
    padding: 16,
    gap: 12,
  },
});
```

### 6. Native Module Integration

```typescript
// src/core/native/HapticFeedback.ts
import { NativeModules, Platform } from 'react-native';

interface HapticFeedbackModule {
  trigger(type: HapticType): void;
}

type HapticType = 'light' | 'medium' | 'heavy' | 'success' | 'warning' | 'error';

const { HapticFeedback: NativeHaptic } = NativeModules as {
  HapticFeedback: HapticFeedbackModule;
};

export const HapticFeedback = {
  trigger: (type: HapticType = 'light') => {
    if (Platform.OS === 'ios' || Platform.OS === 'android') {
      try {
        NativeHaptic?.trigger(type);
      } catch (error) {
        console.warn('Haptic feedback not available:', error);
      }
    }
  },
};

// iOS implementation: ios/YourApp/HapticFeedback.m
/*
#import <React/RCTBridgeModule.h>
#import <UIKit/UIKit.h>

@interface HapticFeedback : NSObject <RCTBridgeModule>
@end

@implementation HapticFeedback

RCT_EXPORT_MODULE();

RCT_EXPORT_METHOD(trigger:(NSString *)type) {
  dispatch_async(dispatch_get_main_queue(), ^{
    UIImpactFeedbackGenerator *generator;
    if ([type isEqualToString:@"light"]) {
      generator = [[UIImpactFeedbackGenerator alloc] initWithStyle:UIImpactFeedbackStyleLight];
    } else if ([type isEqualToString:@"medium"]) {
      generator = [[UIImpactFeedbackGenerator alloc] initWithStyle:UIImpactFeedbackStyleMedium];
    } else {
      generator = [[UIImpactFeedbackGenerator alloc] initWithStyle:UIImpactFeedbackStyleHeavy];
    }
    [generator impactOccurred];
  });
}

@end
*/
```

### 7. Navigation Setup

```typescript
// src/core/navigation/RootNavigator.tsx
import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';

import { LibraryScreen } from '@/features/library/screens/LibraryScreen';
import { ReaderScreen } from '@/features/reader/screens/ReaderScreen';
import { SettingsScreen } from '@/features/settings/screens/SettingsScreen';

export type RootStackParamList = {
  Main: undefined;
  Reader: { bookId: string };
};

export type MainTabParamList = {
  Library: undefined;
  Settings: undefined;
};

const Stack = createNativeStackNavigator<RootStackParamList>();
const Tab = createBottomTabNavigator<MainTabParamList>();

function MainTabs() {
  return (
    <Tab.Navigator>
      <Tab.Screen
        name="Library"
        component={LibraryScreen}
        options={{
          tabBarIcon: ({ color }) => <LibraryIcon color={color} />,
        }}
      />
      <Tab.Screen
        name="Settings"
        component={SettingsScreen}
        options={{
          tabBarIcon: ({ color }) => <SettingsIcon color={color} />,
        }}
      />
    </Tab.Navigator>
  );
}

export function RootNavigator() {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen
          name="Main"
          component={MainTabs}
          options={{ headerShown: false }}
        />
        <Stack.Screen
          name="Reader"
          component={ReaderScreen}
          options={{ headerShown: false }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
```

### 8. Performance Optimization

```typescript
// Performance best practices

// 1. Memoize components
const BookCard = React.memo(function BookCard({ book }: { book: Book }) {
  return (
    <View>
      <Text>{book.title}</Text>
    </View>
  );
});

// 2. Use callbacks correctly
const handlePress = useCallback((id: string) => {
  deleteBook(id);
}, [deleteBook]);

// 3. Optimize FlatList
<FlatList
  data={books}
  keyExtractor={(item) => item.id}
  renderItem={renderItem}
  getItemLayout={(data, index) => ({
    length: ITEM_HEIGHT,
    offset: ITEM_HEIGHT * index,
    index,
  })}
  removeClippedSubviews={true}
  maxToRenderPerBatch={10}
  windowSize={5}
  initialNumToRender={10}
/>

// 4. Enable Hermes in android/gradle.properties
// hermesEnabled=true

// 5. Use react-native-mmkv for fast storage
import { MMKV } from 'react-native-mmkv';
const storage = new MMKV();
storage.set('user.token', token); // 30x faster than AsyncStorage
```

### 9. Testing Patterns

```typescript
// __tests__/features/library/screens/LibraryScreen.test.tsx
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react-native';
import { LibraryScreen } from '@/features/library/screens/LibraryScreen';
import { useLibraryStore } from '@/features/library/store/libraryStore';

jest.mock('@/features/library/store/libraryStore');

describe('LibraryScreen', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('shows loading indicator initially', () => {
    (useLibraryStore as jest.Mock).mockReturnValue({
      books: [],
      loading: true,
      error: null,
      loadBooks: jest.fn(),
    });

    render(<LibraryScreen />);

    expect(screen.getByTestId('loading-indicator')).toBeTruthy();
  });

  it('displays books when loaded', async () => {
    const mockBooks = [
      { id: '1', title: 'Test Book', author: 'Test Author' },
    ];

    (useLibraryStore as jest.Mock).mockReturnValue({
      books: mockBooks,
      loading: false,
      error: null,
      loadBooks: jest.fn(),
    });

    render(<LibraryScreen />);

    expect(screen.getByText('Test Book')).toBeTruthy();
  });

  it('shows error state on failure', () => {
    (useLibraryStore as jest.Mock).mockReturnValue({
      books: [],
      loading: false,
      error: 'Network error',
      loadBooks: jest.fn(),
      clearError: jest.fn(),
    });

    render(<LibraryScreen />);

    expect(screen.getByText('Network error')).toBeTruthy();
  });
});
```

## Common Pitfalls

| Issue | Cause | Solution |
|-------|-------|----------|
| Slow app startup | Large bundle, no Hermes | Enable Hermes, code splitting |
| Memory leak | Event listeners not removed | Use useEffect cleanup |
| FlatList janky | Heavy renderItem | Use React.memo, getItemLayout |
| Bridge bottleneck | Too many native calls | Batch calls, use TurboModules |
| Hot reload broken | State in module scope | Use React context or stores |

## Verification Commands

```bash
# Run tests
npm test

# Run with coverage
npm test -- --coverage

# Lint code
npm run lint

# Type check
npx tsc --noEmit

# Build Android
cd android && ./gradlew assembleRelease

# Build iOS
cd ios && xcodebuild -scheme YourApp -configuration Release
```

## Output

This skill produces:
- Feature-first project structure
- Zustand/Redux state management setup
- Navigation configuration
- Native module integration patterns
- Component test templates
- Performance optimization checklist

## Integration with Spec Kit

- **`/speckit.plan`**: Recommends React Native patterns when detected
- **`/speckit.tasks`**: Generates RN-specific implementation tasks
- **`/speckit.implement`**: Uses React Native patterns
- **`/speckit.analyze`**: Validates QG-RN gates
