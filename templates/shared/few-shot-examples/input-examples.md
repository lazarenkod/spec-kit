# Input Examples (Few-Shot)

High-quality form input implementations with accessibility, validation, and error handling.

## Example 1: Text Input with Label

### Specification
- **Purpose**: Single-line text entry with label
- **States**: Default, focus, error, disabled, readonly
- **Accessibility**: Associated label, error messaging, keyboard support
- **Validation**: Real-time feedback

### Code
```tsx
import { InputHTMLAttributes, forwardRef } from 'react';
import { cn } from '@/lib/utils';

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label: string;
  error?: string;
  helperText?: string;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ label, error, helperText, className, id, ...props }, ref) => {
    const inputId = id || `input-${label.replace(/\s+/g, '-').toLowerCase()}`;
    const errorId = `${inputId}-error`;
    const helperId = `${inputId}-helper`;

    return (
      <div className="flex flex-col gap-1.5">
        <label
          htmlFor={inputId}
          className="text-sm font-medium text-foreground"
        >
          {label}
          {props.required && (
            <span className="ml-1 text-destructive" aria-label="required">
              *
            </span>
          )}
        </label>

        <input
          ref={ref}
          id={inputId}
          className={cn(
            // Base styles
            'flex h-11 w-full rounded-md px-3 py-2',
            'text-base transition-colors',

            // Token-based colors
            'bg-background text-foreground',
            'border-2 border-input',
            'placeholder:text-muted-foreground',

            // Focus state
            'focus-visible:outline-none focus-visible:ring-2',
            'focus-visible:ring-primary focus-visible:ring-offset-2',

            // Error state
            error && 'border-destructive focus-visible:ring-destructive',

            // Disabled state
            'disabled:cursor-not-allowed disabled:opacity-50',

            className
          )}
          aria-invalid={error ? 'true' : 'false'}
          aria-describedby={cn(
            error && errorId,
            helperText && helperId
          )}
          {...props}
        />

        {error && (
          <p id={errorId} className="text-sm text-destructive" role="alert">
            {error}
          </p>
        )}

        {helperText && !error && (
          <p id={helperId} className="text-sm text-muted-foreground">
            {helperText}
          </p>
        )}
      </div>
    );
  }
);

Input.displayName = 'Input';
```

### Why This Works
- **Label Association**: `htmlFor` + `id` creates screen reader link (prevents AP-A11Y-008)
- **Error Messaging**: `aria-invalid` + `aria-describedby` for accessibility
- **Touch Target**: 44px height for mobile usability (prevents AP-A11Y-002)
- **Focus Indicator**: Clear ring on focus (prevents AP-A11Y-004)
- **Token Usage**: No hardcoded colors (prevents AP-VIS-001)
- **Required Indicator**: Visual and screen reader asterisk

---

## Example 2: Password Input with Toggle

### Specification
- **Purpose**: Password entry with show/hide toggle
- **States**: Hidden/visible, focus, error
- **Accessibility**: Toggle button with aria-label
- **Security**: Type switches between password/text

### Code
```tsx
import { useState } from 'react';
import { Eye, EyeOff } from 'lucide-react';

export function PasswordInput({
  label = 'Password',
  ...props
}: Omit<InputProps, 'type'>) {
  const [isVisible, setIsVisible] = useState(false);

  return (
    <div className="relative">
      <Input
        {...props}
        label={label}
        type={isVisible ? 'text' : 'password'}
        className="pr-12"
      />

      <button
        type="button"
        onClick={() => setIsVisible(!isVisible)}
        aria-label={isVisible ? 'Hide password' : 'Show password'}
        className={cn(
          'absolute right-2 top-[2.125rem]',  // Aligned with input
          'h-8 w-8 rounded-md',
          'inline-flex items-center justify-center',
          'text-muted-foreground hover:text-foreground',
          'focus-visible:outline-none focus-visible:ring-2',
          'focus-visible:ring-primary'
        )}
      >
        {isVisible ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
      </button>
    </div>
  );
}
```

### Why This Works
- **Accessibility**: Toggle button has aria-label (prevents AP-A11Y-003)
- **UX**: Users can verify typed password
- **Security**: Default to hidden state
- **Touch Target**: Toggle button is 32×32px (acceptable for secondary action)
- **Focus Management**: Both input and toggle are keyboard accessible

---

## Example 3: Search Input with Clear Button

### Specification
- **Purpose**: Search with instant clear functionality
- **States**: Empty, filled, focus
- **Accessibility**: Clear button with aria-label
- **UX**: X button appears when input has value

### Code
```tsx
import { Search, X } from 'lucide-react';
import { useState, forwardRef } from 'react';

interface SearchInputProps extends Omit<InputProps, 'type'> {
  onClear?: () => void;
}

export const SearchInput = forwardRef<HTMLInputElement, SearchInputProps>(
  ({ onClear, ...props }, ref) => {
    const [value, setValue] = useState(props.value || '');

    const handleClear = () => {
      setValue('');
      onClear?.();
    };

    return (
      <div className="relative">
        <Search
          className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground"
          aria-hidden="true"
        />

        <input
          ref={ref}
          type="search"
          value={value}
          onChange={(e) => setValue(e.target.value)}
          className={cn(
            'flex h-11 w-full rounded-md pl-10 pr-10 py-2 text-base',
            'bg-background text-foreground',
            'border-2 border-input',
            'placeholder:text-muted-foreground',
            'focus-visible:outline-none focus-visible:ring-2',
            'focus-visible:ring-primary focus-visible:ring-offset-2',
            'disabled:cursor-not-allowed disabled:opacity-50'
          )}
          {...props}
        />

        {value && (
          <button
            type="button"
            onClick={handleClear}
            aria-label="Clear search"
            className={cn(
              'absolute right-2 top-1/2 -translate-y-1/2',
              'h-7 w-7 rounded-md',
              'inline-flex items-center justify-center',
              'text-muted-foreground hover:text-foreground hover:bg-accent',
              'focus-visible:outline-none focus-visible:ring-2',
              'focus-visible:ring-primary'
            )}
          >
            <X className="h-4 w-4" />
          </button>
        )}
      </div>
    );
  }
);

SearchInput.displayName = 'SearchInput';
```

### Why This Works
- **Icon Context**: Search icon provides visual context (prevents confusion)
- **Clear UX**: X button only shows when needed (progressive disclosure)
- **Controlled State**: React-controlled for predictable behavior (prevents AP-COMP-009)
- **Aria-hidden**: Decorative icon hidden from screen readers
- **Spacing**: Padding accounts for icons (prevents text overlap)

---

## Example 4: Numeric Input with Step Controls

### Specification
- **Purpose**: Number entry with increment/decrement buttons
- **States**: Default, focus, min/max limits
- **Accessibility**: Screen reader announces value changes
- **Validation**: Enforces min, max, step constraints

### Code
```tsx
import { Minus, Plus } from 'lucide-react';
import { useState, useEffect } from 'react';

interface NumberInputProps extends Omit<InputProps, 'type'> {
  min?: number;
  max?: number;
  step?: number;
  onValueChange?: (value: number) => void;
}

export function NumberInput({
  label,
  min = 0,
  max = 100,
  step = 1,
  value: controlledValue,
  onValueChange,
  ...props
}: NumberInputProps) {
  const [value, setValue] = useState(Number(controlledValue) || min);

  useEffect(() => {
    if (controlledValue !== undefined) {
      setValue(Number(controlledValue));
    }
  }, [controlledValue]);

  const handleIncrement = () => {
    const newValue = Math.min(value + step, max);
    setValue(newValue);
    onValueChange?.(newValue);
  };

  const handleDecrement = () => {
    const newValue = Math.max(value - step, min);
    setValue(newValue);
    onValueChange?.(newValue);
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = Number(e.target.value);
    if (!isNaN(newValue) && newValue >= min && newValue <= max) {
      setValue(newValue);
      onValueChange?.(newValue);
    }
  };

  return (
    <div className="flex flex-col gap-1.5">
      <label className="text-sm font-medium text-foreground">
        {label}
      </label>

      <div className="relative flex items-center">
        <button
          type="button"
          onClick={handleDecrement}
          disabled={value <= min}
          aria-label={`Decrease ${label}`}
          className={cn(
            'absolute left-0 h-11 w-11 rounded-l-md',
            'inline-flex items-center justify-center',
            'border-2 border-r-0 border-input',
            'bg-background hover:bg-accent',
            'text-foreground',
            'disabled:opacity-50 disabled:cursor-not-allowed',
            'focus-visible:outline-none focus-visible:ring-2',
            'focus-visible:ring-primary focus-visible:z-10'
          )}
        >
          <Minus className="h-4 w-4" />
        </button>

        <input
          type="number"
          value={value}
          onChange={handleInputChange}
          min={min}
          max={max}
          step={step}
          aria-valuemin={min}
          aria-valuemax={max}
          aria-valuenow={value}
          className={cn(
            'h-11 w-full px-12 text-center text-base',
            'bg-background text-foreground',
            'border-2 border-input',
            'focus-visible:outline-none focus-visible:ring-2',
            'focus-visible:ring-primary focus-visible:z-10',
            '[appearance:textfield]',
            '[&::-webkit-outer-spin-button]:appearance-none',
            '[&::-webkit-inner-spin-button]:appearance-none'
          )}
          {...props}
        />

        <button
          type="button"
          onClick={handleIncrement}
          disabled={value >= max}
          aria-label={`Increase ${label}`}
          className={cn(
            'absolute right-0 h-11 w-11 rounded-r-md',
            'inline-flex items-center justify-center',
            'border-2 border-l-0 border-input',
            'bg-background hover:bg-accent',
            'text-foreground',
            'disabled:opacity-50 disabled:cursor-not-allowed',
            'focus-visible:outline-none focus-visible:ring-2',
            'focus-visible:ring-primary focus-visible:z-10'
          )}
        >
          <Plus className="h-4 w-4" />
        </button>
      </div>
    </div>
  );
}
```

### Why This Works
- **Aria Attributes**: `aria-valuemin/max/now` for screen readers
- **Button Labels**: Clear aria-labels for increment/decrement (prevents AP-A11Y-003)
- **Validation**: Enforces constraints in both UI and input (prevents invalid states)
- **Touch Targets**: 44×44px buttons for mobile (prevents AP-A11Y-002)
- **Disabled State**: Buttons disabled at limits (prevents invalid actions)
- **Native Spinners Hidden**: Custom UI more accessible and styled

---

## Example 5: Textarea with Character Counter

### Specification
- **Purpose**: Multi-line text entry with length limit
- **States**: Default, focus, approaching limit, at limit, error
- **Accessibility**: Counter announced to screen readers
- **UX**: Visual feedback as limit approaches

### Code
```tsx
import { TextareaHTMLAttributes, forwardRef, useState } from 'react';

interface TextareaProps extends TextareaHTMLAttributes<HTMLTextAreaElement> {
  label: string;
  maxLength?: number;
  error?: string;
}

export const Textarea = forwardRef<HTMLTextAreaElement, TextareaProps>(
  ({ label, maxLength, error, className, ...props }, ref) => {
    const [count, setCount] = useState(0);
    const isApproachingLimit = maxLength && count >= maxLength * 0.8;
    const isAtLimit = maxLength && count >= maxLength;

    return (
      <div className="flex flex-col gap-1.5">
        <div className="flex items-center justify-between">
          <label className="text-sm font-medium text-foreground">
            {label}
            {props.required && (
              <span className="ml-1 text-destructive">*</span>
            )}
          </label>

          {maxLength && (
            <span
              className={cn(
                'text-sm',
                isAtLimit && 'text-destructive font-medium',
                isApproachingLimit && !isAtLimit && 'text-warning',
                !isApproachingLimit && 'text-muted-foreground'
              )}
              aria-live="polite"
              aria-atomic="true"
            >
              {count} / {maxLength}
            </span>
          )}
        </div>

        <textarea
          ref={ref}
          maxLength={maxLength}
          onChange={(e) => setCount(e.target.value.length)}
          className={cn(
            'flex min-h-[120px] w-full rounded-md px-3 py-2',
            'text-base transition-colors resize-vertical',
            'bg-background text-foreground',
            'border-2 border-input',
            'placeholder:text-muted-foreground',
            'focus-visible:outline-none focus-visible:ring-2',
            'focus-visible:ring-primary focus-visible:ring-offset-2',
            error && 'border-destructive focus-visible:ring-destructive',
            'disabled:cursor-not-allowed disabled:opacity-50',
            className
          )}
          {...props}
        />

        {error && (
          <p className="text-sm text-destructive" role="alert">
            {error}
          </p>
        )}
      </div>
    );
  }
);

Textarea.displayName = 'Textarea';
```

### Why This Works
- **Live Updates**: `aria-live="polite"` announces count changes to screen readers
- **Progressive Feedback**: Color changes as limit approaches (80% = warning, 100% = error)
- **Non-Blocking**: maxLength is enforced but provides visual warning before blocking
- **Resize**: `resize-vertical` allows height adjustment (better UX)
- **Min Height**: 120px ensures adequate space (prevents AP-LAY-003)

---

## Common Anti-Patterns to Avoid

- ❌ Inputs without associated labels (AP-A11Y-008)
- ❌ Icon-only buttons without aria-label (AP-A11Y-003)
- ❌ Hardcoded error colors like `text-red-500` (AP-VIS-001)
- ❌ Inputs smaller than 44px height (AP-A11Y-002)
- ❌ Missing error messages or validation feedback (AP-A11Y-008)
- ❌ Using placeholder as label (AP-A11Y-008)
- ❌ Missing focus indicators (AP-A11Y-004)

## Accessibility Checklist

- ✓ Every input has an associated `<label>`
- ✓ Error messages use `role="alert"` and `aria-describedby`
- ✓ Required fields indicated visually and programmatically
- ✓ Minimum 44px height for touch targets
- ✓ Visible focus indicators (ring)
- ✓ 4.5:1 color contrast for text and borders
- ✓ Disabled states prevent interaction
- ✓ Icon buttons have aria-labels

---

**Version:** v0.2.0
**Last Updated:** 2026-01-10
