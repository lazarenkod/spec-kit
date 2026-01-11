# Binding Test Generator Skill

This skill provides patterns and instructions for automated generation of binding tests for cross-platform mobile applications.

## Overview

**Purpose**: Generate platform-specific wrapper tests that verify iOS/Android bindings correctly call shared ViewModels.

**Scope**: Binding layer only (not business logic — that's tested in shared tests).

**Coverage Target**: 100% of public methods in shared ViewModels.

---

## Pattern 1: KMP → iOS (Swift/XCTest)

### Context
Kotlin Multiplatform (KMP) shared ViewModels are wrapped in Swift for iOS consumption. Binding tests verify these wrappers.

### Template Selection

| Return Type | Template |
|-------------|----------|
| `Unit` (void) | Fire-and-forget pattern |
| `T` (value) | Synchronous return pattern |
| `Flow<T>` | Async stream pattern (Combine publisher) |
| `suspend fun` | Async/await pattern (Task/async) |

### Example 1.1: Void Method

**Input** (Kotlin ViewModel):
```kotlin
// shared/src/commonMain/kotlin/AuthViewModel.kt
class AuthViewModel {
    fun logout() {
        // Clear session
    }
}
```

**Output** (Swift XCTest):
```swift
// ios/Tests/AuthViewModelBindingTests.swift
import XCTest
@testable import SharedKMP

class AuthViewModelBindingTests: XCTestCase {
    var sut: AuthViewModelWrapper!
    var mockViewModel: MockAuthViewModel!

    override func setUp() {
        super.setUp()
        mockViewModel = MockAuthViewModel()
        sut = AuthViewModelWrapper(viewModel: mockViewModel)
    }

    override func tearDown() {
        sut = nil
        mockViewModel = nil
        super.tearDown()
    }

    // @speckit:BINDING-TEST:AuthViewModel:logout
    func test_logout_callsViewModel() {
        // When
        sut.logout()

        // Then
        XCTAssertTrue(mockViewModel.logoutCalled, "logout() should call viewModel.logout()")
    }
}
```

### Example 1.2: Value-Returning Method

**Input** (Kotlin):
```kotlin
class AuthViewModel {
    fun isLoggedIn(): Boolean {
        return sessionManager.hasActiveSession()
    }
}
```

**Output** (Swift):
```swift
// @speckit:BINDING-TEST:AuthViewModel:isLoggedIn
func test_isLoggedIn_returnsViewModelValue() {
    // Given
    mockViewModel.isLoggedInReturnValue = true

    // When
    let result = sut.isLoggedIn()

    // Then
    XCTAssertTrue(result, "isLoggedIn() should return viewModel.isLoggedIn() value")
    XCTAssertTrue(mockViewModel.isLoggedInCalled, "isLoggedIn() should call viewModel.isLoggedIn()")
}
```

### Example 1.3: Flow → Combine Publisher

**Input** (Kotlin):
```kotlin
class AuthViewModel {
    fun observeUser(): Flow<User?> {
        return userRepository.observeUser()
    }
}
```

**Output** (Swift):
```swift
import Combine

// @speckit:BINDING-TEST:AuthViewModel:observeUser
func test_observeUser_publishesViewModelFlow() {
    // Given
    let expectedUser = User(id: "123", name: "Test User")
    mockViewModel.observeUserFlow = Just(expectedUser).eraseToAnyPublisher()
    var receivedUser: User?
    let expectation = expectation(description: "User received")

    // When
    let cancellable = sut.observeUser()
        .sink(receiveCompletion: { _ in },
              receiveValue: { user in
                  receivedUser = user
                  expectation.fulfill()
              })

    // Then
    wait(for: [expectation], timeout: 1.0)
    XCTAssertEqual(receivedUser?.id, expectedUser.id, "observeUser() should publish viewModel flow values")
    cancellable.cancel()
}
```

### Example 1.4: Suspend Function → Async/Await

**Input** (Kotlin):
```kotlin
class AuthViewModel {
    suspend fun login(email: String, password: String): Result<User> {
        return authRepository.login(email, password)
    }
}
```

**Output** (Swift):
```swift
// @speckit:BINDING-TEST:AuthViewModel:login
func test_login_callsViewModelSuspendFunction() async throws {
    // Given
    let expectedUser = User(id: "123", name: "Test")
    mockViewModel.loginResult = .success(expectedUser)

    // When
    let result = try await sut.login(email: "test@example.com", password: "pass123")

    // Then
    XCTAssertTrue(mockViewModel.loginCalled, "login() should call viewModel.login()")
    XCTAssertEqual(mockViewModel.loginEmail, "test@example.com")
    XCTAssertEqual(mockViewModel.loginPassword, "pass123")

    switch result {
    case .success(let user):
        XCTAssertEqual(user.id, expectedUser.id)
    case .failure:
        XCTFail("Expected success, got failure")
    }
}
```

---

## Pattern 2: KMP → Android (Kotlin/JUnit)

### Template Selection

| Return Type | Template |
|-------------|----------|
| `Unit` | Simple void test |
| `T` | Synchronous return test |
| `Flow<T>` | Turbine test (flow collection) |
| `suspend fun` | runTest coroutine test |

### Example 2.1: Void Method

**Input** (Kotlin shared ViewModel):
```kotlin
class AuthViewModel {
    fun logout() {
        sessionManager.clearSession()
    }
}
```

**Output** (Kotlin JUnit):
```kotlin
// android/app/src/test/kotlin/com/example/AuthViewModelBindingTest.kt
import org.junit.Before
import org.junit.Test
import org.mockito.kotlin.*
import kotlin.test.assertTrue

class AuthViewModelBindingTest {
    private lateinit var mockViewModel: AuthViewModel
    private lateinit var wrapper: AuthViewModelWrapper

    @Before
    fun setup() {
        mockViewModel = mock()
        wrapper = AuthViewModelWrapper(mockViewModel)
    }

    // @speckit:BINDING-TEST:AuthViewModel:logout
    @Test
    fun `logout calls viewModel logout`() {
        // When
        wrapper.logout()

        // Then
        verify(mockViewModel).logout()
    }
}
```

### Example 2.2: Flow Collection with Turbine

**Input** (Kotlin):
```kotlin
class AuthViewModel {
    fun observeUser(): Flow<User?> {
        return userRepository.observeUser()
    }
}
```

**Output** (Kotlin JUnit):
```kotlin
import app.cash.turbine.test
import kotlinx.coroutines.test.runTest

// @speckit:BINDING-TEST:AuthViewModel:observeUser
@Test
fun `observeUser emits viewModel flow values`() = runTest {
    // Given
    val expectedUser = User(id = "123", name = "Test User")
    whenever(mockViewModel.observeUser()).thenReturn(flowOf(expectedUser))

    // When/Then
    wrapper.observeUser().test {
        val item = awaitItem()
        assertEquals(expectedUser.id, item.id)
        awaitComplete()
    }

    verify(mockViewModel).observeUser()
}
```

### Example 2.3: Suspend Function

**Input** (Kotlin):
```kotlin
class AuthViewModel {
    suspend fun login(email: String, password: String): Result<User> {
        return authRepository.login(email, password)
    }
}
```

**Output** (Kotlin JUnit):
```kotlin
import kotlinx.coroutines.test.runTest

// @speckit:BINDING-TEST:AuthViewModel:login
@Test
fun `login calls viewModel suspend function with correct args`() = runTest {
    // Given
    val expectedResult = Result.success(User(id = "123", name = "Test"))
    whenever(mockViewModel.login(any(), any())).thenReturn(expectedResult)

    // When
    val result = wrapper.login("test@example.com", "pass123")

    // Then
    verify(mockViewModel).login(
        email = "test@example.com",
        password = "pass123"
    )
    assertTrue(result.isSuccess)
    assertEquals("123", result.getOrNull()?.id)
}
```

---

## Pattern 3: React Native → Native Module (Jest)

### Example 3.1: Promise-Based Method

**Input** (Native Module):
```typescript
// NativeAuthModule.ts
export interface NativeAuthModule {
  login(email: string, password: string): Promise<User>;
}
```

**Output** (Jest Test):
```typescript
// __tests__/NativeAuthModule.test.ts
import { NativeModules } from 'react-native';

const mockLogin = jest.fn();
NativeModules.AuthModule = {
  login: mockLogin,
};

describe('NativeAuthModule', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  // @speckit:BINDING-TEST:AuthModule:login
  it('should call native login with correct arguments', async () => {
    // Given
    const expectedUser = { id: '123', name: 'Test User' };
    mockLogin.mockResolvedValue(expectedUser);

    // When
    const result = await NativeModules.AuthModule.login(
      'test@example.com',
      'pass123'
    );

    // Then
    expect(mockLogin).toHaveBeenCalledWith('test@example.com', 'pass123');
    expect(result).toEqual(expectedUser);
  });
});
```

---

## Pattern 4: Flutter → Platform Channel (Dart)

### Example 4.1: Method Channel Call

**Input** (Platform Channel):
```dart
// lib/native_auth.dart
class NativeAuth {
  static const platform = MethodChannel('com.example/auth');

  Future<User?> login(String email, String password) async {
    final result = await platform.invokeMethod('login', {
      'email': email,
      'password': password,
    });
    return result != null ? User.fromJson(result) : null;
  }
}
```

**Output** (Dart Test):
```dart
// test/native_auth_test.dart
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  const channel = MethodChannel('com.example/auth');
  final nativeAuth = NativeAuth();

  setUp(() {
    TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger
        .setMockMethodCallHandler(channel, null);
  });

  // @speckit:BINDING-TEST:NativeAuth:login
  test('login calls platform channel with correct args', () async {
    // Given
    final expectedUser = {'id': '123', 'name': 'Test User'};
    TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger
        .setMockMethodCallHandler(channel, (MethodCall methodCall) async {
      if (methodCall.method == 'login') {
        expect(methodCall.arguments['email'], 'test@example.com');
        expect(methodCall.arguments['password'], 'pass123');
        return expectedUser;
      }
      return null;
    });

    // When
    final result = await nativeAuth.login('test@example.com', 'pass123');

    // Then
    expect(result?.id, '123');
  });
}
```

---

## Code Generation Algorithm

```python
def generate_binding_tests(viewmodel, platform):
    """
    Generate binding tests for a ViewModel on target platform.

    Args:
        viewmodel: Parsed ViewModel AST with methods
        platform: "ios", "android", "react_native", "flutter"

    Returns:
        test_file_content: Generated test code
    """
    test_cases = []

    for method in viewmodel.public_methods:
        # 1. Classify method complexity
        complexity = classify_method_complexity(method)

        # 2. Select template based on return type + platform
        template = select_template(method.return_type, platform)

        # 3. Generate test case
        if complexity == "SIMPLE":
            test_case = template.render(method=method, full_implementation=True)
        elif complexity == "COMPLEX":
            test_case = template.render(method=method, with_mock_setup=True)

        # 4. Verify completeness (QG-BIND-004)
        if has_stubs_or_todos(test_case):
            raise QualityGateViolation("QG-BIND-004: Generated test contains stubs")

        test_cases.append(test_case)

    # 5. Assemble test file
    return assemble_test_file(test_cases, platform)


def classify_method_complexity(method):
    """
    Classify method as SIMPLE or COMPLEX based on signature.

    SIMPLE: Primitives, strings, simple data classes
    COMPLEX: Generics, callbacks, suspend functions, Flows
    """
    if has_generics(method) or has_callbacks(method):
        return "COMPLEX"
    if method.is_suspend or is_flow_return(method):
        return "COMPLEX"
    return "SIMPLE"


def select_template(return_type, platform):
    """
    Select appropriate test template based on return type and platform.
    """
    templates = {
        "ios": {
            "Unit": "ios-void-test.swift.j2",
            "T": "ios-value-test.swift.j2",
            "Flow<T>": "ios-combine-test.swift.j2",
            "suspend": "ios-async-test.swift.j2",
        },
        "android": {
            "Unit": "android-void-test.kt.j2",
            "T": "android-value-test.kt.j2",
            "Flow<T>": "android-turbine-test.kt.j2",
            "suspend": "android-coroutine-test.kt.j2",
        },
    }
    return templates[platform].get(return_type, templates[platform]["T"])
```

---

## Quality Gate: QG-BIND-004

**Name**: No Stub Methods in Generated Code

**Phase**: Post-binding-test-generation

**Severity**: HIGH

**Threshold**: 0 stub methods, 0 TODO comments

**Check**:
```bash
# Scan for incomplete implementations
grep -r "// TODO: Implement" generated_tests/ && exit 1
grep -r "// FIXME" generated_tests/ && exit 1
grep -r "throw NotImplementedError" generated_tests/ && exit 1
grep -r "fatalError(" generated_tests/ && exit 1

# All checks passed
echo "QG-BIND-004: PASS"
```

**Rationale**: Generated binding tests must be complete and runnable immediately. No placeholders or manual work required.

---

## Verification Checklist

After generating binding tests, verify:

- [ ] Test file created for each ViewModel (iOS: `*BindingTests.swift`, Android: `*BindingTest.kt`)
- [ ] 100% method coverage (every public method has a test)
- [ ] All tests compile without errors
- [ ] No stub methods or TODO comments (QG-BIND-004)
- [ ] Tests follow platform conventions (naming, imports, assertions)
- [ ] Mocks properly configured for complex cases
- [ ] Test file contains setup/tearDown methods
- [ ] Tests use platform-appropriate test frameworks (XCTest, JUnit, Jest, flutter_test)

---

## Troubleshooting

### Issue: "Method has complex generic signature, can't generate test"
**Solution**: Generate test with mock setup, use type erasure if needed:
```swift
// For: fun <T> process(item: T): Flow<Result<T>>
func test_process_callsViewModel() {
    let anyItem: Any = "test"
    // ... type-erased test
}
```

### Issue: "Callback/closure parameters not supported"
**Solution**: Generate test with callback verification:
```kotlin
@Test
fun `method with callback verifies callback invoked`() {
    val callbackMock = mock<(Result<User>) -> Unit>()
    wrapper.method(callbackMock)
    verify(mockViewModel).method(any())
}
```

---

**Version**: 1.0.0
**Last Updated**: 2026-01-11
**Compatible with**: spec-kit v0.7.0+
