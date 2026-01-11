# Toast Examples (Few-Shot)

## Example 1: Basic Toast Notifications

### Specification
- Purpose: Show temporary feedback messages
- States: Success, error, warning, info, loading
- Accessibility: ARIA live region, keyboard dismissible, screen reader announcements

### Code
```tsx
import { useToast } from '@/components/ui/use-toast';
import { Button } from '@/components/ui/button';
import { CheckCircle2, XCircle, AlertCircle, Info } from 'lucide-react';

export function ToastDemo() {
  const { toast } = useToast();

  return (
    <div className="flex flex-wrap gap-2">
      <Button
        onClick={() => {
          toast({
            title: 'Success',
            description: 'Your changes have been saved.',
            variant: 'default',
          });
        }}
      >
        Show Success
      </Button>

      <Button
        variant="destructive"
        onClick={() => {
          toast({
            title: 'Error',
            description: 'Something went wrong. Please try again.',
            variant: 'destructive',
          });
        }}
      >
        Show Error
      </Button>

      <Button
        variant="outline"
        onClick={() => {
          toast({
            title: 'Warning',
            description: 'This action cannot be undone.',
            variant: 'warning',
          });
        }}
      >
        Show Warning
      </Button>

      <Button
        variant="outline"
        onClick={() => {
          toast({
            title: 'Info',
            description: 'New features are available in settings.',
            variant: 'info',
          });
        }}
      >
        Show Info
      </Button>
    </div>
  );
}
```

### Why This Works
- Clear title + description structure
- Color-coded variants for different message types
- Automatically dismisses after timeout (default 5s)
- Non-blocking, appears in corner
- ARIA live region for accessibility

---

## Example 2: Toast with Actions

### Specification
- Purpose: Toast with actionable button (undo, view, etc.)
- States: Visible with action, dismissed, action triggered
- Accessibility: Keyboard accessible action button

### Code
```tsx
import { useToast } from '@/components/ui/use-toast';
import { Button } from '@/components/ui/button';
import { ToastAction } from '@/components/ui/toast';

export function ActionToast() {
  const { toast } = useToast();

  const handleDelete = () => {
    // Perform delete
    toast({
      title: 'Item deleted',
      description: 'The item has been removed from your list.',
      action: (
        <ToastAction
          altText="Undo delete"
          onClick={() => {
            // Undo delete logic
            console.log('Undo delete');
          }}
        >
          Undo
        </ToastAction>
      ),
    });
  };

  const handleSave = () => {
    toast({
      title: 'Draft saved',
      description: 'Your changes have been saved as a draft.',
      action: (
        <ToastAction
          altText="View draft"
          onClick={() => {
            // Navigate to draft
            console.log('View draft');
          }}
        >
          View
        </ToastAction>
      ),
    });
  };

  return (
    <div className="flex gap-2">
      <Button onClick={handleDelete} variant="destructive">
        Delete Item
      </Button>
      <Button onClick={handleSave}>Save Draft</Button>
    </div>
  );
}
```

### Why This Works
- Action button clearly labeled
- Alt text for accessibility
- Action dismisses toast after execution
- Common patterns: Undo, View, Retry
- Prominent action button styling

---

## Example 3: Loading Toast with Progress

### Specification
- Purpose: Show ongoing operation with progress updates
- States: Loading, completed, failed
- Accessibility: Progress announcements, status updates

### Code
```tsx
import { useState } from 'react';
import { useToast } from '@/components/ui/use-toast';
import { Button } from '@/components/ui/button';
import { Loader2 } from 'lucide-react';

export function LoadingToast() {
  const { toast } = useToast();
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    setLoading(true);

    const { id, dismiss } = toast({
      title: (
        <div className="flex items-center gap-2">
          <Loader2 className="h-4 w-4 animate-spin" />
          <span>Uploading file...</span>
        </div>
      ),
      description: '0% complete',
      duration: Infinity, // Don't auto-dismiss
    });

    // Simulate upload progress
    for (let i = 0; i <= 100; i += 10) {
      await new Promise(resolve => setTimeout(resolve, 200));

      toast({
        id, // Update existing toast
        title: (
          <div className="flex items-center gap-2">
            <Loader2 className="h-4 w-4 animate-spin" />
            <span>Uploading file...</span>
          </div>
        ),
        description: `${i}% complete`,
        duration: Infinity,
      });
    }

    // Show completion
    toast({
      id,
      title: 'Upload complete',
      description: 'Your file has been uploaded successfully.',
      duration: 3000,
    });

    setLoading(false);
  };

  return (
    <Button onClick={handleUpload} disabled={loading}>
      Upload File
    </Button>
  );
}
```

### Why This Works
- Spinner icon indicates loading
- Progress percentage updates in real-time
- Same toast ID for in-place updates
- Infinite duration during loading
- Completion message with auto-dismiss

---

## Example 4: Rich Toast with Custom Content

### Specification
- Purpose: Toast with images, avatars, or custom layout
- States: Visible with rich content, dismissible
- Accessibility: All content announced by screen readers

### Code
```tsx
import { useToast } from '@/components/ui/use-toast';
import { Button } from '@/components/ui/button';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';

export function RichToast() {
  const { toast } = useToast();

  const showNotification = () => {
    toast({
      title: null, // Use custom title
      description: (
        <div className="flex items-start gap-3">
          <Avatar>
            <AvatarImage src="https://github.com/shadcn.png" />
            <AvatarFallback>SC</AvatarFallback>
          </Avatar>
          <div className="flex-1 space-y-1">
            <p className="text-sm font-semibold">Sarah Connor</p>
            <p className="text-sm text-muted-foreground">
              Mentioned you in a comment
            </p>
            <p className="text-xs text-muted-foreground">2 minutes ago</p>
          </div>
        </div>
      ),
    });
  };

  const showImageToast = () => {
    toast({
      description: (
        <div className="space-y-2">
          <div className="aspect-video w-full overflow-hidden rounded-md">
            <img
              src="https://images.unsplash.com/photo-1506905925346-21bda4d32df4"
              alt="Mountain landscape"
              className="h-full w-full object-cover"
            />
          </div>
          <p className="text-sm font-medium">New photo uploaded</p>
          <p className="text-xs text-muted-foreground">
            Mountain trip - August 2024
          </p>
        </div>
      ),
      className: 'w-80',
    });
  };

  return (
    <div className="flex gap-2">
      <Button onClick={showNotification}>Show Mention</Button>
      <Button onClick={showImageToast}>Show Photo</Button>
    </div>
  );
}
```

### Why This Works
- Avatar for user mentions
- Image previews for visual content
- Custom layout with flexbox
- Semantic content structure
- Wider toast (w-80) for rich content

---

## Example 5: Toast with Multiple Actions

### Specification
- Purpose: Present multiple choices in a toast
- States: Visible with action buttons, dismissed, action selected
- Accessibility: All actions keyboard accessible

### Code
```tsx
import { useToast } from '@/components/ui/use-toast';
import { Button } from '@/components/ui/button';

export function MultiActionToast() {
  const { toast } = useToast();

  const showUpdateNotification = () => {
    toast({
      title: 'Update Available',
      description: 'A new version of the app is ready to install.',
      action: (
        <div className="flex gap-2">
          <Button
            size="sm"
            onClick={() => {
              console.log('Update now');
            }}
          >
            Update Now
          </Button>
          <Button
            size="sm"
            variant="outline"
            onClick={() => {
              console.log('Later');
            }}
          >
            Later
          </Button>
        </div>
      ),
      duration: Infinity, // Require user action
    });
  };

  const showPermissionRequest = () => {
    toast({
      title: 'Enable Notifications',
      description: 'Get notified about important updates and messages.',
      action: (
        <div className="flex flex-col gap-2 w-full">
          <Button
            size="sm"
            onClick={() => {
              console.log('Allow notifications');
            }}
            className="w-full"
          >
            Allow
          </Button>
          <Button
            size="sm"
            variant="ghost"
            onClick={() => {
              console.log('Deny notifications');
            }}
            className="w-full"
          >
            Not Now
          </Button>
        </div>
      ),
      duration: Infinity,
    });
  };

  return (
    <div className="flex gap-2">
      <Button onClick={showUpdateNotification}>Show Update</Button>
      <Button onClick={showPermissionRequest}>Request Permission</Button>
    </div>
  );
}
```

### Why This Works
- Multiple action buttons for choices
- Primary + secondary button styling
- Infinite duration requires user interaction
- Stack vertically for many actions
- Clear labeling for each action
