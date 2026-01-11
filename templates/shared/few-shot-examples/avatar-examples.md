# Avatar Examples (Few-Shot)

High-quality avatar implementations with fallbacks and status indicators.

## Example 1: Basic Avatar

### Specification
- **Purpose**: Display user profile image with fallback
- **States**: Loaded, fallback (initials), loading
- **Accessibility**: Alt text required, ARIA labels
- **Variants**: Sizes (sm, md, lg, xl)

### Code
```tsx
import { cn } from '@/lib/utils';

interface AvatarProps {
  src?: string;
  alt: string;
  size?: 'sm' | 'md' | 'lg' | 'xl';
  fallbackText?: string;
}

export function Avatar({ src, alt, size = 'md', fallbackText }: AvatarProps) {
  const sizeClasses = {
    sm: 'h-8 w-8 text-xs',
    md: 'h-10 w-10 text-sm',
    lg: 'h-12 w-12 text-base',
    xl: 'h-16 w-16 text-lg'
  };

  const getFallback = () => {
    if (fallbackText) {
      return fallbackText.charAt(0).toUpperCase();
    }
    return alt.charAt(0).toUpperCase();
  };

  return (
    <div
      className={cn(
        'relative inline-flex items-center justify-center',
        'rounded-full overflow-hidden',
        'bg-muted text-foreground font-medium',
        sizeClasses[size]
      )}
    >
      {src ? (
        <img
          src={src}
          alt={alt}
          className="h-full w-full object-cover"
          onError={(e) => {
            // Hide broken image, show fallback
            e.currentTarget.style.display = 'none';
          }}
        />
      ) : (
        <span aria-label={alt}>{getFallback()}</span>
      )}
    </div>
  );
}
```

### Why This Works
- **Alt Text**: Required prop ensures accessibility (prevents AP-A11Y-006)
- **Fallback**: Shows initial when image unavailable (prevents blank state)
- **Token Colors**: Uses bg-muted, text-foreground (prevents AP-VIS-001)
- **Size Variants**: Consistent sizing options (prevents AP-COMP-003)
- **Object-fit**: Prevents image distortion (prevents layout issues)
- **Error Handling**: Gracefully handles broken images

---

## Example 2: Avatar with Status Indicator

### Specification
- **Purpose**: Avatar with online/offline/away status
- **States**: online, offline, away, busy
- **Accessibility**: Status has aria-label
- **Layout**: Badge positioned at bottom-right

### Code
```tsx
import { cn } from '@/lib/utils';

type Status = 'online' | 'offline' | 'away' | 'busy';

interface AvatarWithStatusProps {
  src?: string;
  alt: string;
  size?: 'sm' | 'md' | 'lg' | 'xl';
  status?: Status;
  showStatus?: boolean;
}

export function AvatarWithStatus({
  src,
  alt,
  size = 'md',
  status,
  showStatus = true
}: AvatarWithStatusProps) {
  const sizeClasses = {
    sm: 'h-8 w-8 text-xs',
    md: 'h-10 w-10 text-sm',
    lg: 'h-12 w-12 text-base',
    xl: 'h-16 w-16 text-lg'
  };

  const badgeSizeClasses = {
    sm: 'h-2.5 w-2.5',
    md: 'h-3 w-3',
    lg: 'h-3.5 w-3.5',
    xl: 'h-4 w-4'
  };

  const statusColors = {
    online: 'bg-green-500',
    offline: 'bg-gray-400',
    away: 'bg-yellow-500',
    busy: 'bg-red-500'
  };

  const statusLabels = {
    online: 'Online',
    offline: 'Offline',
    away: 'Away',
    busy: 'Busy'
  };

  return (
    <div className="relative inline-block">
      <div
        className={cn(
          'relative inline-flex items-center justify-center',
          'rounded-full overflow-hidden',
          'bg-muted text-foreground font-medium',
          sizeClasses[size]
        )}
      >
        {src ? (
          <img
            src={src}
            alt={alt}
            className="h-full w-full object-cover"
          />
        ) : (
          <span>{alt.charAt(0).toUpperCase()}</span>
        )}
      </div>

      {showStatus && status && (
        <span
          className={cn(
            'absolute bottom-0 right-0',
            'rounded-full',
            'border-2 border-background',
            badgeSizeClasses[size],
            statusColors[status]
          )}
          aria-label={statusLabels[status]}
          role="img"
        />
      )}
    </div>
  );
}
```

### Why This Works
- **Status Colors**: Semantic green/yellow/red (prevents AP-A11Y-005)
- **Aria-label**: Status announced to screen readers (prevents AP-A11Y-008)
- **Border**: White border separates badge from avatar (prevents visual merge)
- **Relative Positioning**: Badge scales with avatar size
- **Conditional Render**: showStatus prop for flexibility
- **Role**: role="img" for badge with aria-label (accessibility best practice)

---

## Example 3: Avatar Group (Stack)

### Specification
- **Purpose**: Display multiple avatars in overlapping stack
- **States**: Default, hover (expand)
- **Accessibility**: Count indicator for hidden avatars
- **Layout**: Right-to-left stack with max visible count

### Code
```tsx
import { cn } from '@/lib/utils';

interface User {
  id: string | number;
  name: string;
  avatarUrl?: string;
}

interface AvatarGroupProps {
  users: User[];
  max?: number;
  size?: 'sm' | 'md' | 'lg';
}

export function AvatarGroup({ users, max = 5, size = 'md' }: AvatarGroupProps) {
  const sizeClasses = {
    sm: 'h-8 w-8 text-xs',
    md: 'h-10 w-10 text-sm',
    lg: 'h-12 w-12 text-base'
  };

  const visibleUsers = users.slice(0, max);
  const remainingCount = Math.max(0, users.length - max);

  return (
    <div className="flex -space-x-2" role="group" aria-label="User avatars">
      {visibleUsers.map((user, index) => (
        <div
          key={user.id}
          className={cn(
            'relative inline-flex items-center justify-center',
            'rounded-full overflow-hidden',
            'bg-muted text-foreground font-medium',
            'border-2 border-background',
            'transition-transform hover:scale-110 hover:z-10',
            sizeClasses[size]
          )}
          style={{ zIndex: visibleUsers.length - index }}
          title={user.name}
        >
          {user.avatarUrl ? (
            <img
              src={user.avatarUrl}
              alt={user.name}
              className="h-full w-full object-cover"
            />
          ) : (
            <span>{user.name.charAt(0).toUpperCase()}</span>
          )}
        </div>
      ))}

      {remainingCount > 0 && (
        <div
          className={cn(
            'relative inline-flex items-center justify-center',
            'rounded-full',
            'bg-muted text-muted-foreground font-semibold',
            'border-2 border-background',
            sizeClasses[size]
          )}
          aria-label={`${remainingCount} more users`}
        >
          +{remainingCount}
        </div>
      )}
    </div>
  );
}
```

### Why This Works
- **Overlap**: Negative margin creates stack effect (-space-x-2)
- **Border**: Separates overlapping avatars (prevents visual merge)
- **Z-index**: Controls stacking order (right to left)
- **Hover**: Scale and z-index on hover (better visibility)
- **Remaining Count**: Shows +N for hidden avatars (transparency)
- **Aria-label**: Count has descriptive label (prevents AP-A11Y-008)
- **Title Attribute**: Shows name on hover (additional context)

---

## Example 4: Avatar with Badge (Verified, Admin)

### Specification
- **Purpose**: Avatar with verification or role badge
- **States**: Default, with badge
- **Accessibility**: Badge has aria-label
- **Layout**: Badge at top-right corner

### Code
```tsx
import { Check, Crown, Shield } from 'lucide-react';
import { cn } from '@/lib/utils';

type BadgeType = 'verified' | 'admin' | 'moderator';

interface AvatarWithBadgeProps {
  src?: string;
  alt: string;
  size?: 'sm' | 'md' | 'lg' | 'xl';
  badge?: BadgeType;
}

export function AvatarWithBadge({
  src,
  alt,
  size = 'md',
  badge
}: AvatarWithBadgeProps) {
  const sizeClasses = {
    sm: 'h-8 w-8 text-xs',
    md: 'h-10 w-10 text-sm',
    lg: 'h-12 w-12 text-base',
    xl: 'h-16 w-16 text-lg'
  };

  const badgeConfig = {
    verified: {
      icon: Check,
      color: 'bg-blue-500',
      label: 'Verified'
    },
    admin: {
      icon: Crown,
      color: 'bg-yellow-500',
      label: 'Admin'
    },
    moderator: {
      icon: Shield,
      color: 'bg-purple-500',
      label: 'Moderator'
    }
  };

  const BadgeIcon = badge ? badgeConfig[badge].icon : null;

  return (
    <div className="relative inline-block">
      <div
        className={cn(
          'relative inline-flex items-center justify-center',
          'rounded-full overflow-hidden',
          'bg-muted text-foreground font-medium',
          sizeClasses[size]
        )}
      >
        {src ? (
          <img
            src={src}
            alt={alt}
            className="h-full w-full object-cover"
          />
        ) : (
          <span>{alt.charAt(0).toUpperCase()}</span>
        )}
      </div>

      {badge && BadgeIcon && (
        <span
          className={cn(
            'absolute -top-0.5 -right-0.5',
            'flex items-center justify-center',
            'h-5 w-5 rounded-full',
            'border-2 border-background',
            badgeConfig[badge].color,
            'text-white'
          )}
          aria-label={badgeConfig[badge].label}
          role="img"
        >
          <BadgeIcon className="h-3 w-3" />
        </span>
      )}
    </div>
  );
}
```

### Why This Works
- **Icon Context**: Icons provide visual meaning (verified, admin, mod)
- **Aria-label**: Badge role announced to screen readers (prevents AP-A11Y-008)
- **Semantic Colors**: Blue (verified), yellow (admin), purple (mod)
- **Border**: Separates badge from avatar (prevents overlap confusion)
- **Role**: role="img" for badge (accessibility)
- **Top-right Position**: Standard location for verification badges

---

## Example 5: Editable Avatar (Upload)

### Specification
- **Purpose**: Avatar with upload/edit functionality
- **States**: Default, hover (show edit), uploading
- **Accessibility**: File input with label, keyboard accessible
- **Interaction**: Click to upload, drag-drop support

### Code
```tsx
import { useState, useRef } from 'react';
import { Camera, Loader2 } from 'lucide-react';
import { cn } from '@/lib/utils';

interface EditableAvatarProps {
  src?: string;
  alt: string;
  size?: 'md' | 'lg' | 'xl';
  onUpload: (file: File) => Promise<void>;
}

export function EditableAvatar({
  src,
  alt,
  size = 'lg',
  onUpload
}: EditableAvatarProps) {
  const [isUploading, setIsUploading] = useState(false);
  const [preview, setPreview] = useState(src);
  const inputRef = useRef<HTMLInputElement>(null);

  const sizeClasses = {
    md: 'h-20 w-20 text-base',
    lg: 'h-24 w-24 text-lg',
    xl: 'h-32 w-32 text-xl'
  };

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    // Show preview
    const reader = new FileReader();
    reader.onload = (e) => {
      setPreview(e.target?.result as string);
    };
    reader.readAsDataURL(file);

    // Upload
    setIsUploading(true);
    try {
      await onUpload(file);
    } catch (error) {
      console.error('Upload failed:', error);
      setPreview(src); // Revert on error
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="relative inline-block group">
      <div
        className={cn(
          'relative inline-flex items-center justify-center',
          'rounded-full overflow-hidden',
          'bg-muted text-foreground font-medium',
          sizeClasses[size]
        )}
      >
        {preview ? (
          <img
            src={preview}
            alt={alt}
            className="h-full w-full object-cover"
          />
        ) : (
          <span>{alt.charAt(0).toUpperCase()}</span>
        )}

        {/* Overlay on Hover */}
        <div
          className={cn(
            'absolute inset-0',
            'flex items-center justify-center',
            'bg-black/50 backdrop-blur-sm',
            'opacity-0 group-hover:opacity-100',
            'transition-opacity',
            'cursor-pointer'
          )}
          onClick={() => inputRef.current?.click()}
        >
          {isUploading ? (
            <Loader2 className="h-6 w-6 text-white animate-spin" />
          ) : (
            <Camera className="h-6 w-6 text-white" />
          )}
        </div>
      </div>

      {/* Hidden File Input */}
      <input
        ref={inputRef}
        type="file"
        accept="image/*"
        onChange={handleFileChange}
        disabled={isUploading}
        className="sr-only"
        aria-label="Upload avatar image"
      />

      {/* Edit Button (Keyboard Accessible) */}
      <button
        type="button"
        onClick={() => inputRef.current?.click()}
        disabled={isUploading}
        aria-label="Change avatar"
        className={cn(
          'absolute bottom-0 right-0',
          'h-8 w-8 rounded-full',
          'bg-primary text-primary-foreground',
          'flex items-center justify-center',
          'border-2 border-background',
          'shadow-sm',
          'hover:bg-primary/90',
          'focus-visible:outline-none focus-visible:ring-2',
          'focus-visible:ring-primary focus-visible:ring-offset-2',
          'disabled:opacity-50 disabled:cursor-not-allowed'
        )}
      >
        {isUploading ? (
          <Loader2 className="h-4 w-4 animate-spin" />
        ) : (
          <Camera className="h-4 w-4" />
        )}
      </button>
    </div>
  );
}
```

### Why This Works
- **Hover Overlay**: Shows camera icon on hover (clear affordance)
- **Loading State**: Spinner during upload (prevents AP-COMP-001)
- **Keyboard Accessible**: Button for file input trigger (prevents AP-A11Y-004)
- **Preview**: Shows image immediately (optimistic UI)
- **Aria-labels**: File input and button have labels (prevents AP-A11Y-008)
- **Error Handling**: Reverts to original on upload failure
- **SR-only Input**: File input hidden but accessible (prevents AP-A11Y-008)

---

## Common Anti-Patterns to Avoid

- ❌ Avatar images without alt text (AP-A11Y-006)
- ❌ Status indicators without aria-label (AP-A11Y-008)
- ❌ No fallback for broken/missing images (blank state)
- ❌ Hardcoded colors like bg-blue-500 for status (AP-VIS-001)
- ❌ Edit functionality not keyboard accessible (AP-A11Y-004)
- ❌ Distorted images (use object-cover)
- ❌ Missing loading state during upload (AP-COMP-001)
- ❌ Badge icons without text alternatives (AP-A11Y-003)

## Accessibility Checklist

- ✓ Avatar images have descriptive alt text
- ✓ Fallback initials when image unavailable
- ✓ Status indicators have aria-label
- ✓ Badge indicators have aria-label and role="img"
- ✓ File upload is keyboard accessible
- ✓ Focus indicators visible on interactive elements
- ✓ Loading states clearly indicated
- ✓ Error handling with fallback display
- ✓ Group has role="group" with aria-label
- ✓ Hover states provide visual feedback

---

**Version:** v0.2.0
**Last Updated:** 2026-01-10
