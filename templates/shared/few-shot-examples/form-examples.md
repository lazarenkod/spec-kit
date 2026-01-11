# Form Examples (Few-Shot)

Complete form patterns with validation, accessibility, and error handling.

## Example 1: Login Form

```tsx
export function LoginForm() {
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setIsLoading(true);
    // Validation and submit logic
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <Input
        label="Email"
        type="email"
        name="email"
        required
        error={errors.email}
        helperText="We'll never share your email"
      />
      <PasswordInput
        label="Password"
        name="password"
        required
        error={errors.password}
      />
      <div className="flex items-center justify-between">
        <label className="flex items-center gap-2">
          <input type="checkbox" name="remember" className="h-4 w-4" />
          <span className="text-sm">Remember me</span>
        </label>
        <Link href="/forgot" className="text-sm text-primary hover:underline">
          Forgot password?
        </Link>
      </div>
      <PrimaryButton type="submit" isLoading={isLoading} className="w-full">
        Sign In
      </PrimaryButton>
    </form>
  );
}
```

**Why This Works**: Semantic form, proper validation, loading state, accessible labels

## Example 2: Registration Form with Validation

```tsx
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';

const schema = z.object({
  name: z.string().min(2, 'Name must be at least 2 characters'),
  email: z.string().email('Invalid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
  confirmPassword: z.string()
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ["confirmPassword"]
});

export function RegistrationForm() {
  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm({
    resolver: zodResolver(schema)
  });

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <Input
        label="Full Name"
        {...register('name')}
        error={errors.name?.message}
      />
      <Input
        label="Email"
        type="email"
        {...register('email')}
        error={errors.email?.message}
      />
      <PasswordInput
        label="Password"
        {...register('password')}
        error={errors.password?.message}
      />
      <PasswordInput
        label="Confirm Password"
        {...register('confirmPassword')}
        error={errors.confirmPassword?.message}
      />
      <PrimaryButton type="submit" isLoading={isSubmitting} className="w-full">
        Create Account
      </PrimaryButton>
    </form>
  );
}
```

**Why This Works**: Schema validation, real-time errors, controlled components

## Example 3: Multi-Step Form

```tsx
export function MultiStepForm() {
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({});

  const steps = [
    { title: 'Personal Info', component: PersonalInfoStep },
    { title: 'Address', component: AddressStep },
    { title: 'Confirmation', component: ConfirmationStep }
  ];

  return (
    <div className="space-y-6">
      {/* Progress indicator */}
      <div className="flex items-center justify-between">
        {steps.map((s, i) => (
          <div key={i} className="flex items-center">
            <div className={cn(
              'h-8 w-8 rounded-full flex items-center justify-center',
              i + 1 < step && 'bg-primary text-primary-foreground',
              i + 1 === step && 'border-2 border-primary',
              i + 1 > step && 'border-2 border-muted'
            )}>
              {i + 1}
            </div>
            <span className="ml-2 text-sm">{s.title}</span>
            {i < steps.length - 1 && (
              <div className="mx-4 h-0.5 w-12 bg-muted" />
            )}
          </div>
        ))}
      </div>

      {/* Current step */}
      <Card>
        <CardHeader>
          <CardTitle>{steps[step - 1].title}</CardTitle>
        </CardHeader>
        <CardContent>
          {React.createElement(steps[step - 1].component, {
            data: formData,
            onNext: (data) => {
              setFormData({ ...formData, ...data });
              setStep(step + 1);
            }
          })}
        </CardContent>
      </Card>
    </div>
  );
}
```

**Why This Works**: Clear progress, data persistence, accessible navigation

## Example 4: Form with File Upload

```tsx
export function FileUploadForm() {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string>('');

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selected = e.target.files?.[0];
    if (selected) {
      setFile(selected);
      setPreview(URL.createObjectURL(selected));
    }
  };

  return (
    <form className="space-y-4">
      <div>
        <label className="block text-sm font-medium mb-2">
          Upload Image
        </label>
        <div className={cn(
          'border-2 border-dashed border-input rounded-lg p-6',
          'hover:border-primary transition-colors cursor-pointer'
        )}>
          <input
            type="file"
            accept="image/*"
            onChange={handleFileChange}
            className="sr-only"
            id="file-upload"
          />
          <label htmlFor="file-upload" className="cursor-pointer">
            {preview ? (
              <img src={preview} alt="Preview" className="max-h-48 mx-auto" />
            ) : (
              <div className="text-center">
                <Upload className="mx-auto h-12 w-12 text-muted-foreground" />
                <p className="mt-2 text-sm text-muted-foreground">
                  Click to upload or drag and drop
                </p>
              </div>
            )}
          </label>
        </div>
      </div>
    </form>
  );
}
```

**Why This Works**: Visual preview, accessible label, drag-drop ready

## Example 5: Search Form with Filters

```tsx
export function SearchWithFiltersForm() {
  const [filters, setFilters] = useState({
    query: '',
    category: 'all',
    dateRange: 'any',
    sortBy: 'relevance'
  });

  return (
    <form className="space-y-4">
      <SearchInput
        value={filters.query}
        onChange={(e) => setFilters({ ...filters, query: e.target.value })}
        placeholder="Search..."
      />

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Select
          label="Category"
          value={filters.category}
          onChange={(value) => setFilters({ ...filters, category: value })}
        >
          <option value="all">All Categories</option>
          <option value="articles">Articles</option>
          <option value="videos">Videos</option>
        </Select>

        <Select
          label="Date Range"
          value={filters.dateRange}
          onChange={(value) => setFilters({ ...filters, dateRange: value })}
        >
          <option value="any">Any Time</option>
          <option value="today">Today</option>
          <option value="week">This Week</option>
        </Select>

        <Select
          label="Sort By"
          value={filters.sortBy}
          onChange={(value) => setFilters({ ...filters, sortBy: value })}
        >
          <option value="relevance">Relevance</option>
          <option value="date">Date</option>
          <option value="popularity">Popularity</option>
        </Select>
      </div>

      <div className="flex gap-2">
        <SecondaryButton onClick={() => setFilters({
          query: '', category: 'all', dateRange: 'any', sortBy: 'relevance'
        })}>
          Clear Filters
        </SecondaryButton>
        <PrimaryButton type="submit">Apply Filters</PrimaryButton>
      </div>
    </form>
  );
}
```

**Why This Works**: Responsive grid, clear actions, state management

---

## Anti-Patterns to Avoid
- ❌ Forms without validation feedback (AP-A11Y-008)
- ❌ Missing loading states on submit (AP-COMP-001)
- ❌ Submit buttons without disabled state during submission
- ❌ Placeholders used as labels (AP-A11Y-008)
- ❌ Form errors without aria-live announcements

---

**Version:** v0.2.0
