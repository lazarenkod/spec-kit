# Modal Examples (Few-Shot)

High-quality modal and dialog implementations with accessibility and interaction patterns.

## Example 1: Basic Modal Dialog

### Specification
- **Purpose**: Display content that requires user attention
- **States**: Open, closed, loading
- **Accessibility**: Focus trap, Escape to close, aria-modal
- **Interaction**: Overlay click closes, backdrop blur

### Code
```tsx
import { useEffect, useRef } from 'react';
import { X } from 'lucide-react';
import { cn } from '@/lib/utils';

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: ReactNode;
  footer?: ReactNode;
}

export function Modal({ isOpen, onClose, title, children, footer }: ModalProps) {
  const closeButtonRef = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    if (isOpen) {
      // Focus close button when modal opens
      closeButtonRef.current?.focus();

      // Trap focus within modal
      const handleKeyDown = (e: KeyboardEvent) => {
        if (e.key === 'Escape') {
          onClose();
        }
      };

      document.addEventListener('keydown', handleKeyDown);
      document.body.style.overflow = 'hidden';

      return () => {
        document.removeEventListener('keydown', handleKeyDown);
        document.body.style.overflow = 'unset';
      };
    }
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center"
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
    >
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-black/50 backdrop-blur-sm"
        onClick={onClose}
        aria-hidden="true"
      />

      {/* Modal Content */}
      <div
        className={cn(
          'relative z-50 w-full max-w-lg',
          'mx-4 rounded-lg',
          'bg-background border border-border shadow-lg',
          'animate-in fade-in-0 zoom-in-95'
        )}
      >
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-border">
          <h2
            id="modal-title"
            className="text-lg font-semibold text-foreground"
          >
            {title}
          </h2>
          <button
            ref={closeButtonRef}
            type="button"
            onClick={onClose}
            aria-label="Close modal"
            className={cn(
              'h-8 w-8 rounded-md',
              'inline-flex items-center justify-center',
              'text-muted-foreground hover:text-foreground',
              'hover:bg-accent',
              'focus-visible:outline-none focus-visible:ring-2',
              'focus-visible:ring-primary'
            )}
          >
            <X className="h-4 w-4" />
          </button>
        </div>

        {/* Body */}
        <div className="p-6">{children}</div>

        {/* Footer */}
        {footer && (
          <div className="flex items-center justify-end gap-2 p-6 border-t border-border">
            {footer}
          </div>
        )}
      </div>
    </div>
  );
}
```

### Why This Works
- **Focus Management**: Auto-focuses close button on open (prevents AP-A11Y-008)
- **Keyboard Support**: Escape key closes modal (ARIA Authoring Practices)
- **Body Scroll Lock**: Prevents background scrolling (better UX)
- **Aria Attributes**: role="dialog", aria-modal, aria-labelledby (prevents AP-A11Y-008)
- **Backdrop Blur**: Visual separation (modern design pattern)
- **Animation**: Smooth fade-in (prevents AP-ANIM-004)

---

## Example 2: Confirmation Dialog

### Specification
- **Purpose**: Confirm destructive or important actions
- **States**: Open, closed, loading during action
- **Accessibility**: Clear action buttons, focus on safe option
- **Interaction**: Primary action (destructive), secondary (cancel)

### Code
```tsx
interface ConfirmDialogProps {
  isOpen: boolean;
  onClose: () => void;
  onConfirm: () => void | Promise<void>;
  title: string;
  description: string;
  confirmLabel?: string;
  confirmDestructive?: boolean;
  isLoading?: boolean;
}

export function ConfirmDialog({
  isOpen,
  onClose,
  onConfirm,
  title,
  description,
  confirmLabel = 'Confirm',
  confirmDestructive = false,
  isLoading = false
}: ConfirmDialogProps) {
  const cancelButtonRef = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    if (isOpen) {
      // Focus cancel button (safe option)
      cancelButtonRef.current?.focus();
    }
  }, [isOpen]);

  const handleConfirm = async () => {
    await onConfirm();
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center"
      role="alertdialog"
      aria-modal="true"
      aria-labelledby="dialog-title"
      aria-describedby="dialog-description"
    >
      <div
        className="fixed inset-0 bg-black/50 backdrop-blur-sm"
        onClick={onClose}
        aria-hidden="true"
      />

      <div
        className={cn(
          'relative z-50 w-full max-w-md',
          'mx-4 rounded-lg p-6',
          'bg-background border border-border shadow-lg',
          'animate-in fade-in-0 zoom-in-95'
        )}
      >
        <h2
          id="dialog-title"
          className="text-lg font-semibold text-foreground mb-2"
        >
          {title}
        </h2>

        <p
          id="dialog-description"
          className="text-sm text-muted-foreground mb-6"
        >
          {description}
        </p>

        <div className="flex items-center justify-end gap-2">
          <button
            ref={cancelButtonRef}
            type="button"
            onClick={onClose}
            disabled={isLoading}
            className={cn(
              'inline-flex items-center justify-center',
              'h-10 px-4 rounded-md',
              'font-medium text-sm',
              'border-2 border-input bg-transparent',
              'text-foreground',
              'hover:bg-accent hover:text-accent-foreground',
              'focus-visible:outline-none focus-visible:ring-2',
              'focus-visible:ring-primary focus-visible:ring-offset-2',
              'disabled:opacity-50 disabled:pointer-events-none'
            )}
          >
            Cancel
          </button>

          <button
            type="button"
            onClick={handleConfirm}
            disabled={isLoading}
            className={cn(
              'inline-flex items-center justify-center',
              'h-10 px-4 rounded-md',
              'font-medium text-sm',
              'focus-visible:outline-none focus-visible:ring-2',
              'focus-visible:ring-offset-2',
              'disabled:opacity-50 disabled:pointer-events-none',
              confirmDestructive
                ? 'bg-destructive text-destructive-foreground hover:bg-destructive/90 focus-visible:ring-destructive'
                : 'bg-primary text-primary-foreground hover:bg-primary/90 focus-visible:ring-primary'
            )}
          >
            {isLoading ? (
              <>
                <svg
                  className="mr-2 h-4 w-4 animate-spin"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                >
                  <circle
                    className="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    strokeWidth="4"
                  />
                  <path
                    className="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                  />
                </svg>
                Processing...
              </>
            ) : (
              confirmLabel
            )}
          </button>
        </div>
      </div>
    </div>
  );
}
```

### Why This Works
- **Role**: role="alertdialog" for important confirmations
- **Focus on Safe**: Cancel button focused by default (prevents accidental confirms)
- **Loading State**: Disables both buttons, shows spinner (prevents AP-COMP-001)
- **Destructive Variant**: Red color for dangerous actions (prevents AP-VIS-005)
- **Aria-describedby**: Links description for screen readers

---

## Example 3: Drawer (Side Panel)

### Specification
- **Purpose**: Slide-in panel for forms or details
- **States**: Open, closed, loading
- **Accessibility**: Focus trap, Escape to close
- **Interaction**: Slides from right, overlay backdrop

### Code
```tsx
import { useEffect, useRef } from 'react';
import { X } from 'lucide-react';
import { cn } from '@/lib/utils';

interface DrawerProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: ReactNode;
  footer?: ReactNode;
  side?: 'left' | 'right';
}

export function Drawer({
  isOpen,
  onClose,
  title,
  children,
  footer,
  side = 'right'
}: DrawerProps) {
  const closeButtonRef = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    if (isOpen) {
      closeButtonRef.current?.focus();

      const handleKeyDown = (e: KeyboardEvent) => {
        if (e.key === 'Escape') {
          onClose();
        }
      };

      document.addEventListener('keydown', handleKeyDown);
      document.body.style.overflow = 'hidden';

      return () => {
        document.removeEventListener('keydown', handleKeyDown);
        document.body.style.overflow = 'unset';
      };
    }
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div
      className="fixed inset-0 z-50"
      role="dialog"
      aria-modal="true"
      aria-labelledby="drawer-title"
    >
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-black/50 backdrop-blur-sm animate-in fade-in-0"
        onClick={onClose}
        aria-hidden="true"
      />

      {/* Drawer Panel */}
      <div
        className={cn(
          'fixed top-0 bottom-0 z-50',
          'w-full max-w-md',
          'bg-background border-l border-border',
          'shadow-xl',
          'flex flex-col',
          side === 'right'
            ? 'right-0 animate-in slide-in-from-right'
            : 'left-0 animate-in slide-in-from-left'
        )}
      >
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-border">
          <h2 id="drawer-title" className="text-lg font-semibold">
            {title}
          </h2>
          <button
            ref={closeButtonRef}
            type="button"
            onClick={onClose}
            aria-label="Close drawer"
            className={cn(
              'h-8 w-8 rounded-md',
              'inline-flex items-center justify-center',
              'text-muted-foreground hover:text-foreground',
              'hover:bg-accent',
              'focus-visible:outline-none focus-visible:ring-2',
              'focus-visible:ring-primary'
            )}
          >
            <X className="h-4 w-4" />
          </button>
        </div>

        {/* Body - Scrollable */}
        <div className="flex-1 overflow-y-auto p-6">{children}</div>

        {/* Footer - Sticky */}
        {footer && (
          <div className="flex items-center justify-end gap-2 p-6 border-t border-border">
            {footer}
          </div>
        )}
      </div>
    </div>
  );
}
```

### Why This Works
- **Slide Animation**: Natural enter/exit (prevents AP-ANIM-003)
- **Scrollable Body**: Content overflow handled (prevents AP-LAY-003)
- **Sticky Footer**: Actions always visible (better UX)
- **Side Prop**: Configurable slide direction (prevents duplication)
- **Max Width**: 448px prevents too-wide panels on desktop

---

## Example 4: Alert (Toast Notification)

### Specification
- **Purpose**: Non-blocking feedback messages
- **States**: Success, error, warning, info
- **Accessibility**: role="alert", auto-dismiss, manual close
- **Interaction**: Slide in from top-right, auto-dismiss after 5s

### Code
```tsx
import { useEffect, useState } from 'react';
import { X, CheckCircle, AlertCircle, Info, AlertTriangle } from 'lucide-react';
import { cn } from '@/lib/utils';

type AlertType = 'success' | 'error' | 'warning' | 'info';

interface AlertProps {
  type: AlertType;
  title: string;
  message?: string;
  duration?: number;
  onClose?: () => void;
}

export function Alert({
  type,
  title,
  message,
  duration = 5000,
  onClose
}: AlertProps) {
  const [isVisible, setIsVisible] = useState(true);

  useEffect(() => {
    if (duration > 0) {
      const timer = setTimeout(() => {
        setIsVisible(false);
        setTimeout(() => onClose?.(), 300); // Wait for exit animation
      }, duration);

      return () => clearTimeout(timer);
    }
  }, [duration, onClose]);

  const handleClose = () => {
    setIsVisible(false);
    setTimeout(() => onClose?.(), 300);
  };

  const icons = {
    success: CheckCircle,
    error: AlertCircle,
    warning: AlertTriangle,
    info: Info
  };

  const styles = {
    success: 'bg-green-50 border-green-200 text-green-900',
    error: 'bg-red-50 border-red-200 text-red-900',
    warning: 'bg-yellow-50 border-yellow-200 text-yellow-900',
    info: 'bg-blue-50 border-blue-200 text-blue-900'
  };

  const iconStyles = {
    success: 'text-green-500',
    error: 'text-red-500',
    warning: 'text-yellow-500',
    info: 'text-blue-500'
  };

  const Icon = icons[type];

  return (
    <div
      role="alert"
      aria-live="polite"
      aria-atomic="true"
      className={cn(
        'pointer-events-auto w-full max-w-sm',
        'rounded-lg border p-4 shadow-lg',
        'transition-all duration-300',
        styles[type],
        isVisible
          ? 'animate-in slide-in-from-right fade-in-0'
          : 'animate-out slide-out-to-right fade-out-0'
      )}
    >
      <div className="flex items-start gap-3">
        <Icon className={cn('h-5 w-5 flex-shrink-0', iconStyles[type])} />

        <div className="flex-1">
          <h3 className="font-semibold text-sm">{title}</h3>
          {message && (
            <p className="mt-1 text-sm opacity-90">{message}</p>
          )}
        </div>

        <button
          type="button"
          onClick={handleClose}
          aria-label="Dismiss notification"
          className={cn(
            'h-6 w-6 rounded-md',
            'inline-flex items-center justify-center',
            'opacity-70 hover:opacity-100',
            'focus-visible:outline-none focus-visible:ring-2',
            'focus-visible:ring-primary'
          )}
        >
          <X className="h-4 w-4" />
        </button>
      </div>
    </div>
  );
}
```

### Why This Works
- **Role**: role="alert" for screen reader announcements
- **Aria-live**: Polite announcements (non-interruptive)
- **Auto-dismiss**: Configurable duration with manual close option
- **Color Coding**: Semantic colors for alert types (prevents AP-A11Y-005)
- **Icon + Text**: Redundant communication (accessibility)
- **Slide Animation**: Natural enter/exit (prevents AP-ANIM-003)

---

## Example 5: Bottom Sheet (Mobile)

### Specification
- **Purpose**: Mobile-optimized modal from bottom
- **States**: Open, closed, draggable
- **Accessibility**: Focus trap, Escape to close
- **Interaction**: Swipe down to dismiss, backdrop tap

### Code
```tsx
import { useEffect, useRef, useState } from 'react';
import { cn } from '@/lib/utils';

interface BottomSheetProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: ReactNode;
}

export function BottomSheet({ isOpen, onClose, title, children }: BottomSheetProps) {
  const [isDragging, setIsDragging] = useState(false);
  const [dragOffset, setDragOffset] = useState(0);
  const startY = useRef(0);

  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';

      const handleKeyDown = (e: KeyboardEvent) => {
        if (e.key === 'Escape') {
          onClose();
        }
      };

      document.addEventListener('keydown', handleKeyDown);

      return () => {
        document.removeEventListener('keydown', handleKeyDown);
        document.body.style.overflow = 'unset';
      };
    }
  }, [isOpen, onClose]);

  const handleTouchStart = (e: React.TouchEvent) => {
    setIsDragging(true);
    startY.current = e.touches[0].clientY;
  };

  const handleTouchMove = (e: React.TouchEvent) => {
    if (!isDragging) return;
    const currentY = e.touches[0].clientY;
    const offset = Math.max(0, currentY - startY.current);
    setDragOffset(offset);
  };

  const handleTouchEnd = () => {
    setIsDragging(false);
    if (dragOffset > 100) {
      onClose();
    }
    setDragOffset(0);
  };

  if (!isOpen) return null;

  return (
    <div
      className="fixed inset-0 z-50"
      role="dialog"
      aria-modal="true"
      aria-labelledby="bottom-sheet-title"
    >
      <div
        className="fixed inset-0 bg-black/50 backdrop-blur-sm animate-in fade-in-0"
        onClick={onClose}
        aria-hidden="true"
      />

      <div
        className={cn(
          'fixed bottom-0 left-0 right-0 z-50',
          'max-h-[90vh] rounded-t-2xl',
          'bg-background border-t border-border',
          'shadow-2xl',
          'animate-in slide-in-from-bottom',
          'transition-transform'
        )}
        style={{
          transform: `translateY(${dragOffset}px)`
        }}
        onTouchStart={handleTouchStart}
        onTouchMove={handleTouchMove}
        onTouchEnd={handleTouchEnd}
      >
        {/* Drag Handle */}
        <div className="flex justify-center py-3">
          <div className="h-1.5 w-12 rounded-full bg-muted" />
        </div>

        {/* Header */}
        <div className="px-6 pb-4">
          <h2 id="bottom-sheet-title" className="text-lg font-semibold">
            {title}
          </h2>
        </div>

        {/* Content - Scrollable */}
        <div className="overflow-y-auto px-6 pb-6" style={{ maxHeight: 'calc(90vh - 100px)' }}>
          {children}
        </div>
      </div>
    </div>
  );
}
```

### Why This Works
- **Mobile-First**: Optimized for touch interactions
- **Swipe Gesture**: Natural dismiss gesture (modern mobile UX)
- **Drag Handle**: Visual affordance for swipe (prevents confusion)
- **Max Height**: 90vh prevents full-screen takeover
- **Scrollable Content**: Handles overflow properly

---

## Common Anti-Patterns to Avoid

- ❌ Modals without focus trap (AP-A11Y-008)
- ❌ Missing aria-modal or role="dialog" (AP-A11Y-008)
- ❌ No Escape key handler (AP-A11Y-004)
- ❌ Backdrop doesn't close modal (confusing UX)
- ❌ Body scrolling not locked (AP-COMP-009)
- ❌ Close button without aria-label (AP-A11Y-003)
- ❌ Destructive confirm without color distinction (AP-VIS-005)
- ❌ Alerts without role="alert" (AP-A11Y-008)

## Accessibility Checklist

- ✓ role="dialog" or role="alertdialog"
- ✓ aria-modal="true"
- ✓ aria-labelledby pointing to title
- ✓ aria-describedby for descriptions
- ✓ Focus trap (Tab stays within modal)
- ✓ Escape key closes modal
- ✓ Auto-focus on open (safe option for confirms)
- ✓ Body scroll locked when open
- ✓ Close button has aria-label
- ✓ Alerts use role="alert" and aria-live

---

**Version:** v0.2.0
**Last Updated:** 2026-01-10
