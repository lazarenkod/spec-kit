# Wizard Examples (Few-Shot)

## Example 1: Multi-Step Form Wizard with Progress

### Specification
- Purpose: Guide users through multi-step form completion
- States: Current step, completed steps, validation errors per step
- Accessibility: Step indicators, keyboard navigation, form validation

### Code
```tsx
import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Check } from 'lucide-react';

interface Step {
  id: number;
  title: string;
  description: string;
}

const steps: Step[] = [
  { id: 1, title: 'Account', description: 'Create your account' },
  { id: 2, title: 'Profile', description: 'Add personal details' },
  { id: 3, title: 'Preferences', description: 'Set your preferences' },
  { id: 4, title: 'Review', description: 'Review and confirm' },
];

export function FormWizard() {
  const [currentStep, setCurrentStep] = useState(1);
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    fullName: '',
    phone: '',
    notifications: true,
    newsletter: false,
  });

  const isStepComplete = (stepId: number) => stepId < currentStep;
  const isCurrentStep = (stepId: number) => stepId === currentStep;

  const nextStep = () => {
    if (currentStep < steps.length) {
      setCurrentStep(currentStep + 1);
    }
  };

  const prevStep = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
    }
  };

  return (
    <Card className="w-full max-w-2xl mx-auto">
      <CardHeader>
        <CardTitle>Sign Up</CardTitle>
        <CardDescription>Create your account in 4 easy steps</CardDescription>
      </CardHeader>
      <CardContent>
        {/* Progress indicator */}
        <nav aria-label="Progress">
          <ol className="flex items-center w-full mb-8">
            {steps.map((step, index) => (
              <li
                key={step.id}
                className={`flex items-center ${
                  index < steps.length - 1 ? 'flex-1' : ''
                }`}
              >
                <div className="flex flex-col items-center">
                  <div
                    className={`flex items-center justify-center w-10 h-10 rounded-full border-2 ${
                      isStepComplete(step.id)
                        ? 'bg-primary border-primary text-primary-foreground'
                        : isCurrentStep(step.id)
                        ? 'border-primary text-primary'
                        : 'border-muted text-muted-foreground'
                    }`}
                  >
                    {isStepComplete(step.id) ? (
                      <Check className="w-5 h-5" />
                    ) : (
                      <span className="text-sm font-medium">{step.id}</span>
                    )}
                  </div>
                  <div className="mt-2 text-center">
                    <p
                      className={`text-sm font-medium ${
                        isCurrentStep(step.id)
                          ? 'text-foreground'
                          : 'text-muted-foreground'
                      }`}
                    >
                      {step.title}
                    </p>
                  </div>
                </div>
                {index < steps.length - 1 && (
                  <div
                    className={`h-0.5 flex-1 mx-4 ${
                      isStepComplete(step.id + 1)
                        ? 'bg-primary'
                        : 'bg-muted'
                    }`}
                  />
                )}
              </li>
            ))}
          </ol>
        </nav>

        {/* Step content */}
        <div className="space-y-6">
          {currentStep === 1 && (
            <div className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="email">Email</Label>
                <Input
                  id="email"
                  type="email"
                  placeholder="you@example.com"
                  value={formData.email}
                  onChange={(e) =>
                    setFormData({ ...formData, email: e.target.value })
                  }
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="password">Password</Label>
                <Input
                  id="password"
                  type="password"
                  value={formData.password}
                  onChange={(e) =>
                    setFormData({ ...formData, password: e.target.value })
                  }
                />
              </div>
            </div>
          )}

          {currentStep === 2 && (
            <div className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="fullName">Full Name</Label>
                <Input
                  id="fullName"
                  placeholder="John Doe"
                  value={formData.fullName}
                  onChange={(e) =>
                    setFormData({ ...formData, fullName: e.target.value })
                  }
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="phone">Phone Number</Label>
                <Input
                  id="phone"
                  type="tel"
                  placeholder="+1 (555) 000-0000"
                  value={formData.phone}
                  onChange={(e) =>
                    setFormData({ ...formData, phone: e.target.value })
                  }
                />
              </div>
            </div>
          )}

          {currentStep === 3 && (
            <div className="space-y-4">
              {/* Preferences step content */}
              <p>Preferences configuration...</p>
            </div>
          )}

          {currentStep === 4 && (
            <div className="space-y-4">
              <h3 className="font-semibold">Review your information</h3>
              <dl className="space-y-2">
                <div>
                  <dt className="text-sm text-muted-foreground">Email</dt>
                  <dd className="font-medium">{formData.email}</dd>
                </div>
                <div>
                  <dt className="text-sm text-muted-foreground">Full Name</dt>
                  <dd className="font-medium">{formData.fullName}</dd>
                </div>
                <div>
                  <dt className="text-sm text-muted-foreground">Phone</dt>
                  <dd className="font-medium">{formData.phone}</dd>
                </div>
              </dl>
            </div>
          )}
        </div>

        {/* Navigation buttons */}
        <div className="flex justify-between mt-8">
          <Button
            variant="outline"
            onClick={prevStep}
            disabled={currentStep === 1}
          >
            Previous
          </Button>
          <Button
            onClick={nextStep}
            disabled={currentStep === steps.length}
          >
            {currentStep === steps.length ? 'Submit' : 'Next'}
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}
```

### Why This Works
- Visual progress indicator with checkmarks for completed steps
- Step titles and numbers for orientation
- Progress line shows completion visually
- Previous/Next buttons with appropriate disabled states
- Step content isolated in conditional blocks
- Review step shows all data before submission

---

## Example 2: Vertical Stepper Wizard

### Specification
- Purpose: Side-by-side navigation for complex multi-step workflows
- States: Active, completed, upcoming, error per step
- Accessibility: Step navigation, form field validation

### Code
```tsx
import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Check, Circle } from 'lucide-react';
import { cn } from '@/lib/utils';

interface VerticalStep {
  id: number;
  label: string;
  content: React.ReactNode;
}

export function VerticalWizard() {
  const [currentStep, setCurrentStep] = useState(0);
  const [completedSteps, setCompletedSteps] = useState<Set<number>>(new Set());

  const steps: VerticalStep[] = [
    {
      id: 0,
      label: 'Company Information',
      content: <div>Company form fields...</div>,
    },
    {
      id: 1,
      label: 'Contact Details',
      content: <div>Contact form fields...</div>,
    },
    {
      id: 2,
      label: 'Billing Information',
      content: <div>Billing form fields...</div>,
    },
    {
      id: 3,
      label: 'Confirmation',
      content: <div>Confirmation summary...</div>,
    },
  ];

  const completeStep = (stepId: number) => {
    setCompletedSteps(prev => new Set(prev).add(stepId));
    if (stepId < steps.length - 1) {
      setCurrentStep(stepId + 1);
    }
  };

  return (
    <div className="flex gap-6 max-w-4xl mx-auto">
      {/* Vertical stepper nav */}
      <nav className="w-64 flex-shrink-0">
        <ol className="space-y-2">
          {steps.map((step, index) => {
            const isActive = currentStep === step.id;
            const isCompleted = completedSteps.has(step.id);
            const isUpcoming = step.id > currentStep;

            return (
              <li key={step.id}>
                <button
                  onClick={() => {
                    if (isCompleted || !isUpcoming) {
                      setCurrentStep(step.id);
                    }
                  }}
                  disabled={isUpcoming}
                  className={cn(
                    'flex items-center gap-3 w-full p-3 rounded-lg text-left transition-colors',
                    isActive && 'bg-primary text-primary-foreground',
                    isCompleted && !isActive && 'hover:bg-accent',
                    isUpcoming && 'opacity-50 cursor-not-allowed'
                  )}
                >
                  <div
                    className={cn(
                      'flex items-center justify-center w-8 h-8 rounded-full border-2',
                      isCompleted && 'bg-primary border-primary text-primary-foreground',
                      isActive && !isCompleted && 'border-primary-foreground',
                      isUpcoming && 'border-muted-foreground'
                    )}
                  >
                    {isCompleted ? (
                      <Check className="w-4 h-4" />
                    ) : (
                      <Circle className="w-4 h-4" />
                    )}
                  </div>
                  <span className="text-sm font-medium">{step.label}</span>
                </button>

                {index < steps.length - 1 && (
                  <div
                    className={cn(
                      'ml-7 h-8 w-0.5',
                      isCompleted ? 'bg-primary' : 'bg-muted'
                    )}
                  />
                )}
              </li>
            );
          })}
        </ol>
      </nav>

      {/* Step content */}
      <Card className="flex-1">
        <CardContent className="p-6">
          <h2 className="text-2xl font-bold mb-6">
            {steps[currentStep].label}
          </h2>
          <div className="mb-8">{steps[currentStep].content}</div>

          <div className="flex justify-end gap-2">
            {currentStep > 0 && (
              <Button
                variant="outline"
                onClick={() => setCurrentStep(currentStep - 1)}
              >
                Back
              </Button>
            )}
            <Button onClick={() => completeStep(currentStep)}>
              {currentStep === steps.length - 1 ? 'Finish' : 'Continue'}
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
```

### Why This Works
- Vertical navigation for better space utilization
- Click completed steps to go back and edit
- Upcoming steps are disabled but visible
- Visual connector lines between steps
- Highlighted active step with primary color
- Completed steps marked with checkmark

---

## Example 3: Wizard with Branch Logic

### Specification
- Purpose: Conditional steps based on user selections
- States: Dynamic step flow, skip/show steps based on input
- Accessibility: Clear navigation, announce step changes

### Code
```tsx
import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

type UserType = 'individual' | 'business' | null;

export function BranchingWizard() {
  const [step, setStep] = useState(1);
  const [userType, setUserType] = useState<UserType>(null);

  // Dynamic step calculation based on user type
  const getSteps = () => {
    const baseSteps = [
      { id: 1, title: 'Account Type' },
      { id: 2, title: 'Basic Info' },
    ];

    if (userType === 'business') {
      return [
        ...baseSteps,
        { id: 3, title: 'Business Details' },
        { id: 4, title: 'Tax Information' },
        { id: 5, title: 'Review' },
      ];
    }

    return [
      ...baseSteps,
      { id: 3, title: 'Personal Details' },
      { id: 4, title: 'Review' },
    ];
  };

  const steps = getSteps();
  const currentStepInfo = steps.find(s => s.id === step);

  return (
    <Card className="max-w-2xl mx-auto">
      <CardHeader>
        <CardTitle>{currentStepInfo?.title}</CardTitle>
        <p className="text-sm text-muted-foreground">
          Step {step} of {steps.length}
        </p>
      </CardHeader>
      <CardContent>
        <div className="space-y-6">
          {step === 1 && (
            <RadioGroup
              value={userType || ''}
              onValueChange={(value) => setUserType(value as UserType)}
            >
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="individual" id="individual" />
                <Label htmlFor="individual">
                  Individual Account
                  <p className="text-sm text-muted-foreground">
                    For personal use
                  </p>
                </Label>
              </div>
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="business" id="business" />
                <Label htmlFor="business">
                  Business Account
                  <p className="text-sm text-muted-foreground">
                    For companies and organizations
                  </p>
                </Label>
              </div>
            </RadioGroup>
          )}

          {step === 2 && (
            <div>Basic information form...</div>
          )}

          {step === 3 && userType === 'business' && (
            <div>Business details form...</div>
          )}

          {step === 3 && userType === 'individual' && (
            <div>Personal details form...</div>
          )}

          {step === 4 && userType === 'business' && (
            <div>Tax information form...</div>
          )}

          {((step === 4 && userType === 'individual') ||
            (step === 5 && userType === 'business')) && (
            <div>Review and submit...</div>
          )}
        </div>

        <div className="flex justify-between mt-8">
          <Button
            variant="outline"
            onClick={() => setStep(step - 1)}
            disabled={step === 1}
          >
            Back
          </Button>
          <Button
            onClick={() => setStep(step + 1)}
            disabled={step === 1 && !userType}
          >
            {step === steps.length ? 'Submit' : 'Continue'}
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}
```

### Why This Works
- Dynamic step count based on user selection
- Conditional step rendering based on branch logic
- Clear choice presentation with descriptions
- Progress indicator adapts to selected path
- Back button respects branching logic

---

## Example 4: Wizard with Field Validation

### Specification
- Purpose: Validate each step before allowing progression
- States: Valid step, invalid with errors, submitting
- Accessibility: Error messages, field-level validation

### Code
```tsx
import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { Button } from '@/components/ui/button';
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

const step1Schema = z.object({
  email: z.string().email('Invalid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
});

const step2Schema = z.object({
  firstName: z.string().min(2, 'First name required'),
  lastName: z.string().min(2, 'Last name required'),
  phone: z.string().regex(/^\+?[1-9]\d{1,14}$/, 'Invalid phone number'),
});

type Step1Data = z.infer<typeof step1Schema>;
type Step2Data = z.infer<typeof step2Schema>;

export function ValidatedWizard() {
  const [currentStep, setCurrentStep] = useState(1);
  const [step1Data, setStep1Data] = useState<Step1Data | null>(null);

  const form1 = useForm<Step1Data>({
    resolver: zodResolver(step1Schema),
    defaultValues: step1Data || { email: '', password: '' },
  });

  const form2 = useForm<Step2Data>({
    resolver: zodResolver(step2Schema),
    defaultValues: { firstName: '', lastName: '', phone: '' },
  });

  const onStep1Submit = (data: Step1Data) => {
    setStep1Data(data);
    setCurrentStep(2);
  };

  const onStep2Submit = (data: Step2Data) => {
    console.log('Final submission:', { ...step1Data, ...data });
    // Handle final submission
  };

  return (
    <Card className="max-w-md mx-auto">
      <CardHeader>
        <CardTitle>
          {currentStep === 1 ? 'Account Credentials' : 'Personal Information'}
        </CardTitle>
      </CardHeader>
      <CardContent>
        {currentStep === 1 ? (
          <Form {...form1}>
            <form onSubmit={form1.handleSubmit(onStep1Submit)} className="space-y-4">
              <FormField
                control={form1.control}
                name="email"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Email</FormLabel>
                    <FormControl>
                      <Input placeholder="you@example.com" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form1.control}
                name="password"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Password</FormLabel>
                    <FormControl>
                      <Input type="password" {...field} />
                    </FormControl>
                    <FormDescription>
                      At least 8 characters
                    </FormDescription>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <Button type="submit" className="w-full">
                Continue
              </Button>
            </form>
          </Form>
        ) : (
          <Form {...form2}>
            <form onSubmit={form2.handleSubmit(onStep2Submit)} className="space-y-4">
              <FormField
                control={form2.control}
                name="firstName"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>First Name</FormLabel>
                    <FormControl>
                      <Input {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form2.control}
                name="lastName"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Last Name</FormLabel>
                    <FormControl>
                      <Input {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form2.control}
                name="phone"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Phone Number</FormLabel>
                    <FormControl>
                      <Input placeholder="+1 555 000 0000" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <div className="flex gap-2">
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => setCurrentStep(1)}
                  className="flex-1"
                >
                  Back
                </Button>
                <Button type="submit" className="flex-1">
                  Submit
                </Button>
              </div>
            </form>
          </Form>
        )}
      </CardContent>
    </Card>
  );
}
```

### Why This Works
- Zod schema validation per step
- React Hook Form for field management
- Inline error messages below fields
- Form can't progress without valid data
- Previous step data persisted and editable
- Field-level validation on blur

---

## Example 5: Wizard with Save Draft

### Specification
- Purpose: Allow users to save progress and resume later
- States: Editing, saving draft, draft saved, loading draft
- Accessibility: Save status announcements, auto-save indicator

### Code
```tsx
import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Save, Check } from 'lucide-react';
import { useDebounce } from '@/hooks/use-debounce';

export function DraftableWizard() {
  const [currentStep, setCurrentStep] = useState(1);
  const [formData, setFormData] = useState({
    step1: { name: '', email: '' },
    step2: { company: '', role: '' },
    step3: { preferences: [] },
  });
  const [saveStatus, setSaveStatus] = useState<'saved' | 'saving' | 'unsaved'>('saved');

  // Debounce form data changes
  const debouncedFormData = useDebounce(formData, 1000);

  useEffect(() => {
    // Auto-save draft on data change
    const saveDraft = async () => {
      setSaveStatus('saving');
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 500));
      localStorage.setItem('wizard-draft', JSON.stringify(debouncedFormData));
      setSaveStatus('saved');
    };

    saveDraft();
  }, [debouncedFormData]);

  useEffect(() => {
    // Load draft on mount
    const draft = localStorage.getItem('wizard-draft');
    if (draft) {
      setFormData(JSON.parse(draft));
    }
  }, []);

  return (
    <Card className="max-w-2xl mx-auto">
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle>Application Form</CardTitle>
          <Badge variant={saveStatus === 'saved' ? 'default' : 'secondary'}>
            {saveStatus === 'saved' && <Check className="w-3 h-3 mr-1" />}
            {saveStatus === 'saving' && <Save className="w-3 h-3 mr-1 animate-pulse" />}
            {saveStatus === 'saved' ? 'Draft Saved' : 'Saving...'}
          </Badge>
        </div>
      </CardHeader>
      <CardContent>
        {/* Step content */}
        <div className="space-y-4 mb-6">
          <p className="text-sm text-muted-foreground">
            Your progress is automatically saved.
          </p>
          {/* Form fields here */}
        </div>

        {/* Navigation */}
        <div className="flex justify-between">
          <Button
            variant="outline"
            onClick={() => setCurrentStep(currentStep - 1)}
            disabled={currentStep === 1}
          >
            Previous
          </Button>
          <div className="flex gap-2">
            <Button
              variant="outline"
              onClick={() => {
                localStorage.removeItem('wizard-draft');
                setFormData({
                  step1: { name: '', email: '' },
                  step2: { company: '', role: '' },
                  step3: { preferences: [] },
                });
              }}
            >
              Clear Draft
            </Button>
            <Button onClick={() => setCurrentStep(currentStep + 1)}>
              {currentStep === 3 ? 'Submit' : 'Next'}
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
```

### Why This Works
- Auto-save with debounce (1s after typing stops)
- Save status badge shows saving/saved state
- Draft loaded automatically on mount
- Clear draft option for starting fresh
- localStorage persistence across sessions
- Unobtrusive save indicator
