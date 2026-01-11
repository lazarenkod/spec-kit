# Select Examples (Few-Shot)

## Example 1: Basic Select Dropdown

### Specification
- Purpose: Single selection from a list of options
- States: Open, closed, selected, disabled, error
- Accessibility: Keyboard navigation, screen reader support, proper ARIA

### Code
```tsx
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Label } from '@/components/ui/label';

export function BasicSelect() {
  return (
    <div className="space-y-2">
      <Label htmlFor="country">Country</Label>
      <Select>
        <SelectTrigger id="country" className="w-full">
          <SelectValue placeholder="Select a country" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="us">United States</SelectItem>
          <SelectItem value="ca">Canada</SelectItem>
          <SelectItem value="uk">United Kingdom</SelectItem>
          <SelectItem value="de">Germany</SelectItem>
          <SelectItem value="fr">France</SelectItem>
        </SelectContent>
      </Select>
    </div>
  );
}
```

### Why This Works
- Clear label associated with select
- Placeholder text guides user
- Keyboard navigable (arrow keys, enter)
- ARIA attributes built-in
- Consistent styling with design tokens

---

## Example 2: Multi-Select with Tags

### Specification
- Purpose: Select multiple options, display as removable tags
- States: Open, selecting, displaying selected tags
- Accessibility: Tag removal buttons, keyboard navigation

### Code
```tsx
import { useState } from 'react';
import { Check, ChevronsUpDown, X } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
} from '@/components/ui/command';
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/components/ui/popover';
import { cn } from '@/lib/utils';

const skills = [
  { value: 'react', label: 'React' },
  { value: 'typescript', label: 'TypeScript' },
  { value: 'nodejs', label: 'Node.js' },
  { value: 'python', label: 'Python' },
  { value: 'aws', label: 'AWS' },
];

export function MultiSelect() {
  const [open, setOpen] = useState(false);
  const [selectedValues, setSelectedValues] = useState<string[]>([]);

  const toggleSelection = (value: string) => {
    setSelectedValues(prev =>
      prev.includes(value)
        ? prev.filter(v => v !== value)
        : [...prev, value]
    );
  };

  const removeSelection = (value: string) => {
    setSelectedValues(prev => prev.filter(v => v !== value));
  };

  return (
    <div className="space-y-2">
      <Popover open={open} onOpenChange={setOpen}>
        <PopoverTrigger asChild>
          <Button
            variant="outline"
            role="combobox"
            aria-expanded={open}
            className="w-full justify-between"
          >
            <span className="flex gap-2 flex-wrap">
              {selectedValues.length > 0 ? (
                selectedValues.map(value => {
                  const skill = skills.find(s => s.value === value);
                  return (
                    <Badge key={value} variant="secondary" className="gap-1">
                      {skill?.label}
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          removeSelection(value);
                        }}
                        className="hover:bg-accent rounded-sm"
                      >
                        <X className="h-3 w-3" />
                      </button>
                    </Badge>
                  );
                })
              ) : (
                'Select skills...'
              )}
            </span>
            <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
          </Button>
        </PopoverTrigger>
        <PopoverContent className="w-full p-0">
          <Command>
            <CommandInput placeholder="Search skills..." />
            <CommandEmpty>No skill found.</CommandEmpty>
            <CommandGroup>
              {skills.map(skill => (
                <CommandItem
                  key={skill.value}
                  value={skill.value}
                  onSelect={() => toggleSelection(skill.value)}
                >
                  <Check
                    className={cn(
                      'mr-2 h-4 w-4',
                      selectedValues.includes(skill.value)
                        ? 'opacity-100'
                        : 'opacity-0'
                    )}
                  />
                  {skill.label}
                </CommandItem>
              ))}
            </CommandGroup>
          </Command>
        </PopoverContent>
      </Popover>
    </div>
  );
}
```

### Why This Works
- Selected items shown as removable badges
- Search/filter functionality
- Checkmarks indicate selected items
- Click badge X to remove individual selections
- Popover closes after selection (optional)

---

## Example 3: Grouped Select Options

### Specification
- Purpose: Organize options into logical groups
- States: Open with visible groups, keyboard navigation through groups
- Accessibility: Group labels, semantic markup

### Code
```tsx
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';

export function GroupedSelect() {
  return (
    <Select>
      <SelectTrigger className="w-full">
        <SelectValue placeholder="Select a fruit" />
      </SelectTrigger>
      <SelectContent>
        <SelectGroup>
          <SelectLabel>Fruits</SelectLabel>
          <SelectItem value="apple">Apple</SelectItem>
          <SelectItem value="banana">Banana</SelectItem>
          <SelectItem value="orange">Orange</SelectItem>
        </SelectGroup>
        <SelectGroup>
          <SelectLabel>Vegetables</SelectLabel>
          <SelectItem value="carrot">Carrot</SelectItem>
          <SelectItem value="broccoli">Broccoli</SelectItem>
          <SelectItem value="spinach">Spinach</SelectItem>
        </SelectGroup>
        <SelectGroup>
          <SelectLabel>Proteins</SelectLabel>
          <SelectItem value="chicken">Chicken</SelectItem>
          <SelectItem value="beef">Beef</SelectItem>
          <SelectItem value="tofu">Tofu</SelectItem>
        </SelectGroup>
      </SelectContent>
    </Select>
  );
}
```

### Why This Works
- Clear visual separation between groups
- Group labels provide context
- Semantic HTML structure
- Keyboard navigation respects groups
- Maintains single selection pattern

---

## Example 4: Select with Icons and Descriptions

### Specification
- Purpose: Rich select options with icons and supplementary text
- States: Open, selected with icon display
- Accessibility: Description text announced by screen readers

### Code
```tsx
import { useState } from 'react';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { CreditCard, Smartphone, Wallet } from 'lucide-react';

const paymentMethods = [
  {
    value: 'card',
    label: 'Credit Card',
    description: 'Pay with Visa, Mastercard, or Amex',
    icon: CreditCard,
  },
  {
    value: 'paypal',
    label: 'PayPal',
    description: 'Fast and secure checkout',
    icon: Wallet,
  },
  {
    value: 'apple-pay',
    label: 'Apple Pay',
    description: 'One-tap payment on Apple devices',
    icon: Smartphone,
  },
];

export function RichSelect() {
  const [selected, setSelected] = useState('card');
  const selectedMethod = paymentMethods.find(m => m.value === selected);
  const SelectedIcon = selectedMethod?.icon || CreditCard;

  return (
    <Select value={selected} onValueChange={setSelected}>
      <SelectTrigger className="w-full">
        <div className="flex items-center gap-2">
          <SelectedIcon className="h-4 w-4" />
          <SelectValue />
        </div>
      </SelectTrigger>
      <SelectContent>
        {paymentMethods.map(method => {
          const Icon = method.icon;
          return (
            <SelectItem key={method.value} value={method.value}>
              <div className="flex items-start gap-3">
                <Icon className="h-4 w-4 mt-0.5" />
                <div className="space-y-0.5">
                  <p className="font-medium">{method.label}</p>
                  <p className="text-xs text-muted-foreground">
                    {method.description}
                  </p>
                </div>
              </div>
            </SelectItem>
          );
        })}
      </SelectContent>
    </Select>
  );
}
```

### Why This Works
- Icon provides visual cue
- Description text aids decision-making
- Selected value shows icon in trigger
- Rich content in dropdown options
- Maintains accessibility with proper structure

---

## Example 5: Searchable Select (Combobox)

### Specification
- Purpose: Large option sets with search/filter capability
- States: Searching, filtered results, no results
- Accessibility: Search input, filtered results announced

### Code
```tsx
import { useState } from 'react';
import { Check, ChevronsUpDown } from 'lucide-react';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
} from '@/components/ui/command';
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/components/ui/popover';

const countries = [
  { value: 'us', label: 'United States' },
  { value: 'uk', label: 'United Kingdom' },
  { value: 'ca', label: 'Canada' },
  { value: 'au', label: 'Australia' },
  { value: 'de', label: 'Germany' },
  { value: 'fr', label: 'France' },
  { value: 'jp', label: 'Japan' },
  { value: 'cn', label: 'China' },
  // ... many more countries
];

export function SearchableSelect() {
  const [open, setOpen] = useState(false);
  const [value, setValue] = useState('');

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <Button
          variant="outline"
          role="combobox"
          aria-expanded={open}
          className="w-full justify-between"
        >
          {value
            ? countries.find(country => country.value === value)?.label
            : 'Select country...'}
          <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-full p-0">
        <Command>
          <CommandInput placeholder="Search country..." />
          <CommandEmpty>No country found.</CommandEmpty>
          <CommandGroup className="max-h-64 overflow-auto">
            {countries.map(country => (
              <CommandItem
                key={country.value}
                value={country.value}
                onSelect={(currentValue) => {
                  setValue(currentValue === value ? '' : currentValue);
                  setOpen(false);
                }}
              >
                <Check
                  className={cn(
                    'mr-2 h-4 w-4',
                    value === country.value ? 'opacity-100' : 'opacity-0'
                  )}
                />
                {country.label}
              </CommandItem>
            ))}
          </CommandGroup>
        </Command>
      </PopoverContent>
    </Popover>
  );
}
```

### Why This Works
- Instant search filtering
- Handles large option sets (100s of items)
- Checkmark shows selected item
- No results message when filter doesn't match
- Max height with scroll for long lists
- Closes on selection
